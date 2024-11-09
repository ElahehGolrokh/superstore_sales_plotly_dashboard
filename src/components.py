import pandas as pd
import plotly
import plotly.express as px
from typing import List, Union
from dash import dcc, html


def create_dropdown(options: List,
                    label: str,
                    id_prefix: str,
                    multi: bool = True,
                    value: str = None) -> html.Div:
    """Creates a good-looking dropdown

    Args:
        options: drop-down's options
        label: drop-down's label
        id_prefix: will be used in drop-down's id -> id of the drop-down
        component will be {id_prefix}-dropdown
        multi: whether to get multiple values
        value: default value

    Returns:
        html.Div to put in the ``app.layout``
    """
    if not value:
        value = [options[0]]
    return html.Div(
        children=[
            html.Label(
                label,
                id=f"{id_prefix}-label",
            ),
            dcc.Dropdown(
                options=options,
                id=f"{id_prefix}-dropdown",
                value=value,
                searchable=False,
                clearable=False,
                multi=multi
            ),
        ],
        style={"padding": 10, "flex": 1},
    )


def create_chart(id_prefix: str,
                 style: dict = {'height': '90%'},
                 figure={}) -> html.Div:
    """Returns html.Div including the dcc graph to
    put in the ``app.layout``

    Args:
        id_prefix: will be used in chart's id -> id of the
        graph will be {id_prefix}-chart
        style: css style of the graph
        figure: plotly.express chart which could be created
                staticly or via callbacks
    """
    return html.Div(
        children=[dcc.Graph(figure=figure, id='{}-chart'.format(id_prefix),
                            style=style),],
        style={'height': '40vh'}
    )


def create_radioitem(options: List,
                     label: str,
                     id_prefix: str,) -> html.Div:
    """Creates a good-looking radio item

    Args:
        options: RadioItems's options
        label: RadioItems's label
        id_prefix: will be used in RadioItems's id -> id of the RadioItems
        component will be {id_prefix}-radioitem

    Returns:
        html.Div to put in the ``app.layout``
    """
    return html.Div(
        children=[
            html.Label(
                label,
                id=f"{id_prefix}-label",
                style={'font-weight': 'bold',
                       'font-size': '1.3rem',
                       'margin-bottom': '1.5rem'}
            ),
            dcc.RadioItems(
                options=options,
                id=f"{id_prefix}-radioitem",
                value=options[0],
            ),
        ],
        className="custom-radioitem",
    )


def create_checklist(options: List,
                     label: str,
                     id_prefix: str,) -> html.Div:
    """Creates a good-looking checklist

    Args:
        options: checklist's options
        label: checklist's label
        id_prefix: will be used in checklist's id -> id of the checklist
        component will be {id_prefix}-checklist

    Returns:
        html.Div to put in the ``app.layout``
    """
    return html.Div(
        children=[
            html.Label(
                label,
                id=f"{id_prefix}-label",
                style={'font-weight': 'bold',
                       'font-size': '1.3rem',
                       'margin-bottom': '1.5rem'}
            ),
            dcc.Checklist(
                options=options,
                id=f"{id_prefix}-checklist",
                value=[options[0]],
            ),
        ],
        className="custom-checklist",
    )


def create_total_sales_figure(df: pd.DataFrame,
                              title: str,
                              col: str = None,
                              col_chosen: Union[str, List] = None,
                              partitioning: bool = False) -> plotly.graph_objs._figure.Figure:
    """
    Creates line chart of monthly sales in each year for the specified
    df or a part of it.

    Args:
        df: could be the whole df or a part of it
        title: title of the graph,
        col: the column which you want to filter the data based on some
             condition on it,
        col_chosen: the value (or list of values) of the condition's column
                    which you want to keep
        partitioning: whether to consider a part of the initial df

    Returns:
        plotly graph including the line chart of the monthly sales
    """
    if partitioning:
        if type(col_chosen) is list:
            partition = df[df[col].isin(col_chosen)]
        else:
            partition = df[df[col] == col_chosen]
    else:
        partition = df.copy()
    partition = partition.groupby(['Year', 'Month'],
                                  as_index=False)['Sales'].sum()
    fig = px.line(partition,
                  x="Month",
                  y="Sales",
                  color="Year",
                  hover_name="Year",
                  line_shape="spline",
                  render_mode="svg",
                  markers=True)
    fig.update_layout(title=title)
    return fig


def create_group_barcharts(df: pd.DataFrame,
                           grouped_cols: List,
                           title: str,
                           col: str = None,
                           col_chosen: Union[str, List] = None,
                           partitioning: bool = True,
                           color_palette: dict = None) -> list[html.Div]:
    """
    Creates grouped bar chart.

    Args:
        df: cold be the whole df or a part of it
        grouped_cols: a list of the columns you want to implement the
                      groupby method on them
        title: title of the graph
        col: the column which you want to filter the data based on some
             condition on it
        col_chosen: the value (or list of values) of the condition's column
                    which you want to keep
        partitioning: whether to consider a part of the initial df
        color_palette: the color palette of the graph

    Returns:
        plotly graph including the grouped bar chart
    """
    if partitioning:
        if type(col_chosen) is list:
            partition = df[df[col].isin(col_chosen)]
        else:
            partition = df[df[col] == col_chosen]
    else:
        partition = df.copy()
    partition = partition.groupby(grouped_cols).size().reset_index(name="counts")
    fig = px.bar(data_frame=partition,
                 x="Segment",
                 y="counts",
                 color="Ship_Mode",
                 barmode="group",
                 color_discrete_map=color_palette)
    fig.update_layout(title=title)
    return fig


def create_barchart_withsales(df: pd.DataFrame,
                              grouped_col: str,
                              title: str,
                              col: str = None,
                              col_chosen: str = None,
                              partitioning: bool = True,
                              color_palette: Union[List, pd.Series] = px.colors.sequential.Viridis) -> list[html.Div]:
    """
    Creates bar chart with specifying sales of each bar.

    Args:
        df: cold be the whole df or a part of it
        grouped_cols: the column you want to calculate sum of sales on each
                      one of its unique values. the calculated values will
                      be printed on the corresponding bars on the chart
        title: title of the graph
        col: the column which you want to filter the data based on some
             condition on it
        col_chosen: the value (or list of values) of the condition's column
                    which you want to keep
        partitioning: whether to consider a part of the initial df
        color_palette: the color palette of the graph

    Returns:
        plotly graph including the bar chart
    """
    if partitioning:
        partition = df[df[col] == col_chosen]
    else:
        partition = df.copy()
    sales = []
    for el in partition[grouped_col].unique():
        sales.append(int(partition[partition[grouped_col] == el]['Sales'].sum()/1000))
    partition = partition.groupby(grouped_col, as_index=False)['Sales'].sum()
    fig = px.bar(partition,
                 y=grouped_col,
                 x='Sales',
                 text='Sales',
                 color_discrete_sequence=color_palette)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(title=title)
    return fig


def create_piechart(df: pd.DataFrame,
                    names: str,
                    title: str,
                    color_palette: Union[List, pd.Series],
                    col: str = None,
                    col_chosen: Union[str, List] = None,
                    partitioning: bool = True,
                    hole: float = 0) -> list[html.Div]:
    """
    Creates pie chart

    Args:
        df: cold be the whole df or a part of it
        names: specifies the column which you want to have the pie chart of it
        title: title of the graph
        color_palette: the color palette of the graph
        col: the column which you want to filter the data based on some
             condition on it
        col_chosen: the value (or list of values) of the condition's column
                    which you want to keep
        partitioning: whether to consider a part of the initial df
        hole: the percentage of the pie that you want the hole to take

    Returns:
        plotly graph including the bar chart
    """
    if partitioning:
        if type(col_chosen) is list:
            partition = df[df[col].isin(col_chosen)]
        else:
            partition = df[df[col] == col_chosen]
    else:
        partition = df.copy()
    fig = px.pie(partition,
                 names=partition[names],
                 hole=hole,
                 color_discrete_sequence=color_palette,
                 title=title)
    return fig
