import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

from dash import Dash, html, dcc, Output, Input

from .components import create_total_sales_figure, create_group_barcharts, \
                        create_barchart_withsales, create_piechart
from .sections import create_overview_section, create_segment_section, \
                      create_category_section, create_region_section
from .utils import get_color_palette


def get_app() -> Dash:
    """
    Creates the app and adds its layout.

    Examples:
        >>> app = get_app()
        >>> Controller(df).add_callbacks(app)
        >>> app.run(debug=True)

    Note:
        - you have to add the app's callbacks before running the app:
            ``add_callbacks(app)``

    Returns:
        a dash app that can be run using ``app.run()``
    """
    # Initialize the app
    app = Dash(__name__, serve_locally=True, suppress_callback_exceptions=True)

    # App layout
    app.layout = html.Div([
        html.Div(html.H1(children='Superstore Sales Analysis',
                         style={'textAlign': 'center'}),
                 style={'background-color': '#133E87',
                        'color': '#F3F3E0',
                        'padding': 10,
                        'border-radius': '0.5rem',
                        'margin-bottom': 5}),
        dmc.Grid([
            dmc.Col([
                html.Div([dcc.Tabs(id="tabs",
                                   value='tab-overview',
                                   children=[
                                       dcc.Tab(label='Overview',
                                               value='tab-overview',
                                               className='custom-tab',
                                               selected_className='custom-tab--selected'),
                                       dcc.Tab(label='Region-Based Analysis',
                                               value='tab-region',
                                               className='custom-tab',
                                               selected_className='custom-tab--selected'),
                                       dcc.Tab(label='Segment-Based Analysis',
                                               value='tab-segment',
                                               className='custom-tab',
                                               selected_className='custom-tab--selected'),
                                       dcc.Tab(label='Category-Based Analysis',
                                               value='tab-category',
                                               className='custom-tab',
                                               selected_className='custom-tab--selected'),
                                    ],
                                   className='tabs',
                                   ),
                          ],
                         style={'background-color': '#133E87',
                                'height': '100vh',
                                'border-radius': '0.5rem',
                                'padding': '2rem'})
            ], span=3),

            dmc.Col([
                html.Div(children=[],
                         style={'background-color': '#F3F3E0',
                                'height': '100vh',
                                'border-radius': '0.5rem',
                                'padding': '2rem'},
                         id='tabs-content')
            ], span='auto'),
        ]),
        ], id="layout-content")
    return app


class Controller:
    """
    Adds controls to build the interaction

    ...
    Attributes
    ----------
        df: pandas dataframe

    Methods
    -------
        add_callbacks()

    """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def add_callbacks(self, app: Dash):
        """Adds callbacks to different parts of the app
        Args:
            app: Dash app
        """
        # Chang the content based on the selected tab
        @app.callback(
            Output(component_id='tabs-content', component_property='children'),
            Input(component_id='tabs', component_property='value')
        )
        def _update_tab_contents(tab):
            if tab == 'tab-overview':
                overview_content = html.Div(create_overview_section(self.df))
                return overview_content
            elif tab == 'tab-region':
                region_content = html.Div(create_region_section(self.df),
                                          style={'height': '90%'})
                return region_content
            elif tab == 'tab-segment':
                segment_content = html.Div(create_segment_section(self.df),
                                           style={'height': '90%'})
                return segment_content
            elif tab == 'tab-category':
                category_content = html.Div(create_category_section(self.df),
                                            style={'height': '90%'})
                return category_content

        # Segment tab, first row callbacks
        @app.callback(
            [Output(component_id='segment-category-pie-chart',
                    component_property='figure'),
             Output(component_id='sales-segment-category-chart',
                    component_property='figure'),],
            Input(component_id='category-segment-dropdown',
                  component_property='value')
        )
        def _update_segment_category(*col_chosen):
            color_palette = pd.Series(get_color_palette(self.df['Segment'].unique()))
            fig1 = create_piechart(df=self.df,
                                   names='Segment',
                                   title="Segment Shares for selected categories",
                                   color_palette=color_palette,
                                   col='Category',
                                   col_chosen=col_chosen[0],
                                   hole=.3)
            fig2 = create_total_sales_figure(df=self.df,
                                             col='Category',
                                             col_chosen=col_chosen[0],
                                             partitioning=True,
                                             title="Segment Sales for selected categories")
            return fig1, fig2

        # Segment tab, second row callbacks
        @app.callback(
            [Output(component_id='segment-shipmode-count-chart',
                    component_property='figure'),
             Output(component_id='sales-segment-shipmode-chart',
                    component_property='figure'),],
            Input(component_id='shipmode-segment-dropdown',
                  component_property='value')
        )
        def _update_segment_shipmode(*col_chosen):
            color_palette = get_color_palette(self.df['Ship_Mode'].unique())
            fig1 = create_group_barcharts(self.df,
                                          grouped_cols=["Segment", "Ship_Mode"],
                                          title='Segment Shares for selected ship modes',
                                          col='Ship_Mode',
                                          col_chosen=col_chosen[0],
                                          partitioning=True,
                                          color_palette=color_palette)
            fig2 = create_total_sales_figure(df=self.df,
                                             col='Ship_Mode',
                                             col_chosen=col_chosen[0],
                                             partitioning=True,
                                             title='Segment Sales for selected ship modes')
            return fig1, fig2

        # Category tab, first row callbacks
        @app.callback(
            [Output(component_id='category-category-pie-chart',
                    component_property='figure'),
             Output(component_id='sales-category-category-chart',
                    component_property='figure'),],
            Input(component_id='category-category-radioitem',
                  component_property='value')
        )
        def _update_category_first_row(col_chosen):
            fig1 = create_piechart(df=self.df,
                                   names='Sub_Category',
                                   title='Sahres of each sub-category',
                                   color_palette=px.colors.sequential.Viridis,
                                   col='Category',
                                   col_chosen=col_chosen)
            fig2 = create_total_sales_figure(df=self.df,
                                             col='Category',
                                             col_chosen=col_chosen,
                                             partitioning=True,
                                             title=f"Monthly sales for {col_chosen}")
            return fig1, fig2

        # Category tab, second row callbacks
        @app.callback(
            [Output(component_id='subcategory-sales-chart',
                    component_property='figure'),
             Output(component_id='category-shipmode-segment-chart',
                    component_property='figure')],
            Input(component_id='category-category-radioitem',
                  component_property='value')
        )
        def _update_category_second_row(col_chosen):
            color_palette = pd.Series(get_color_palette(self.df['Category'].unique()))
            fig1 = create_barchart_withsales(df=self.df,
                                             grouped_col='Sub_Category',
                                             title=f"Sales of each sub_category for {col_chosen}",
                                             col='Category',
                                             col_chosen=col_chosen,
                                             color_palette=color_palette)

            color_palette = get_color_palette(self.df['Ship_Mode'].unique())
            fig2 = create_group_barcharts(self.df,
                                          grouped_cols=["Segment", "Ship_Mode"],
                                          title=f"Ship mode Shares of each segment for {col_chosen}",
                                          col='Category',
                                          col_chosen=col_chosen,
                                          partitioning=True,
                                          color_palette=color_palette)
            return fig1, fig2

        # region tab, first row callbacks
        @app.callback(
            [Output(component_id='region-region-pie-chart',
                    component_property='figure'),
             Output(component_id='sales-region-region-chart',
                    component_property='figure'),],
            Input(component_id='region-region-checklist',
                  component_property='value')
        )
        def _update_region_first(*col_chosen):
            fig1 = create_piechart(df=self.df,
                                   names='Region',
                                   title='Sahres of each Region',
                                   color_palette=px.colors.sequential.Viridis,
                                   col='Region',
                                   col_chosen=col_chosen[0])
            fig2 = create_total_sales_figure(df=self.df,
                                             col='Region',
                                             col_chosen=col_chosen[0],
                                             partitioning=True,
                                             title=f"Monthly sales for {col_chosen}")
            return fig1, fig2

        # Region tab, second row callbacks
        @app.callback(
            Output(component_id='region-shipmode-segment-chart',
                   component_property='figure'),
            Input(component_id='region-region-checklist',
                  component_property='value')
        )
        def _update_region_second(*col_chosen):
            partition = self.df[self.df['Region'].isin(col_chosen[0])]
            fig = px.choropleth(data_frame=partition,
                                locationmode="USA-states",
                                locations='State_Abbrev',
                                color='Sales',
                                color_continuous_scale="Viridis",
                                scope="usa",
                                labels={'unemp': 'unemployment rate'}
                                )
            return fig
