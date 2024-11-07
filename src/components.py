from typing import Any, Dict, Hashable, List
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

    Returns:
        html.Div to put in the ``app.layout``
    """
    if not value:
        value=[options[0]]
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
                 style: dict = None,
                 figure={}) -> html.Div:
    return html.Div(
        children=[dcc.Graph(figure=figure, id='{}-chart'.format(id_prefix), style=style),],
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
        className=f"{id_prefix}-radioitem",
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
        className=f"{id_prefix}-checklist",
    )
