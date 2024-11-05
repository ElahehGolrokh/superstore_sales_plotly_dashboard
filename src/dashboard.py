import dash_mantine_components as dmc
import numpy as np
import plotly.express as px
import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input

from .sections import create_overview_section, create_segment_section
from .utils import get_color_palette


def get_app(df: pd.DataFrame) -> Dash:
    # Initialize the app
    app = Dash(__name__, serve_locally=True, suppress_callback_exceptions=True)

    # App layout
    app.layout = html.Div([
        html.Div(html.H1(children='Superstore Sales Analysis', style={'textAlign': 'center'}),
                    style={'background-color': '#133E87',
                            'color': '#F3F3E0',
                            'padding': 10,
                            'border-radius': '0.5rem',
                            'margin-bottom': 5,}),
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
       
    Methods
    -------
        add_callbacks()
        update_error_graph()

    """
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
    
    def add_callbacks(self, app: Dash):
        """Adds callbacks to different parts of the app
        Args:
            app: Dash app
        """
        @app.callback(
            Output(component_id='category-chart', component_property='figure'),
            Input(component_id='category-dropdown', component_property='value')
        )
        def update_graph(*col_chosen):
            # print(col_chosen)
            partition = self.df[self.df['Category'].isin(col_chosen[0])]
            # print(partition.head())
            fig = px.histogram(partition, x='Segment', y='Sales', histfunc='avg')
            return fig
        
        # Chang the content based on the selected tab
        @app.callback(
            Output(component_id='tabs-content', component_property='children'),
            Input(component_id='tabs', component_property='value')
        )
        def update_tab_contents(tab):
            if tab == 'tab-overview':
                overview_content = html.Div([
                                html.Div(create_overview_section(self.df))
                            ], id='overview-content')
                return overview_content
            elif tab == 'tab-region':
                return html.Div([
                    html.H3('tab region')
                ])
            elif tab == 'tab-segment':
                segment_content = html.Div([
                                html.Div(create_segment_section(self.df))
                            ])
                return segment_content
            elif tab == 'tab-category':
                return html.Div([
                    html.H3('tab category')
                ])

        # Overview tab, linechart callbacks
        @app.callback(
            Output(component_id='sales-city-chart', component_property='figure'),
            Input(component_id='city-dropdown', component_property='value')
        )
        def update_sales_city(*col_chosen):
            # print(col_chosen)
            partition = self.df.groupby(['Order_Date', 'City'], as_index=False)['Sales'].sum()
            partition = partition[partition['City'].isin(col_chosen[0])]
            # print('partition = ', partition)
            fig = px.line(partition,
                        x="Order_Date",
                        y="Sales",
                        color="City",
                        hover_name="City",
                        line_shape="spline",
                        render_mode="svg")
            return fig

        # Segment tab, first row callbacks
        @app.callback(
            [Output(component_id='segment-category-pie-chart', component_property='figure'),
             Output(component_id='sales-segment-category-chart', component_property='figure'),],
            Input(component_id='category-segment-dropdown', component_property='value')
        )
        def update_segment_category(*col_chosen):
            # print(col_chosen)
            # partition = self.df.groupby(['Segment'], as_index=False)[['Row_ID', 'Category']].count()
            color_palette1 = pd.Series(get_color_palette(self.df['Segment'].unique()))
            partition = self.df[self.df['Category'].isin(col_chosen[0])]
            # print('partition = ', partition)
            fig1 = px.pie(self.df,
                         names=partition['Segment'],
                         hole=.3,
                         color_discrete_sequence=color_palette1)
            fig1.update_layout(title="Segment Shares for selected categories",)
            partition = partition.groupby(['Month', 'Segment'], as_index=False)['Sales'].sum()
            fig2 = px.line(partition,
                        x="Month",
                        y="Sales",
                        color="Segment",
                        hover_name="Segment",
                        line_shape="spline",
                        render_mode="svg")
            fig2.update_layout(title="Segment Sales for selected categories",)
            return fig1, fig2
        
        # Segment tab, second row callbacks
        @app.callback(
            [Output(component_id='segment-shipmode-count-chart', component_property='figure'),
             Output(component_id='sales-segment-shipmode-chart', component_property='figure'),],
            Input(component_id='shipmode-segment-dropdown', component_property='value')
        )
        def update_segment_shipmode(*col_chosen):
            color_palette1 = get_color_palette(self.df['Ship_Mode'].unique())
            partition = self.df[self.df['Ship_Mode'].isin(col_chosen[0])]
            partition1 = partition.groupby(by=["Segment", "Ship_Mode"]).size().reset_index(name="counts")
            fig1 = px.bar(data_frame=partition1,
                          x="Segment",
                          y="counts",
                          color="Ship_Mode",
                          barmode="group",
                          color_discrete_map=color_palette1)
            fig1.update_layout(title="Segment Shares for selected ship modes",)
            partition2 = partition.groupby(['Month', 'Segment'], as_index=False)['Sales'].sum()
            fig2 = px.line(partition2,
                        x="Month",
                        y="Sales",
                        color="Segment",
                        hover_name="Segment",
                        line_shape="spline",
                        render_mode="svg")
            fig2.update_layout(title="Segment Sales for selected ship modes",)
            return fig1, fig2

