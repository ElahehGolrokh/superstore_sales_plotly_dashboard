import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input

from .components import create_dropdown, create_barchart


def get_app(df: pd.DataFrame) -> Dash:

    # Initialize the app
    app = Dash()

    # App layout
    app.layout = html.Div([
        html.Div(html.H1(children='Superstore Sales Analysis', style={'textAlign': 'center'}),
                    style={'background-color': '#133E87',
                            'color': '#F3F3E0',
                            'padding': 10,
                            'border-radius': 8,
                            'margin-bottom': 5}),
        dmc.Grid([
            dmc.Col([
                html.Div(['This is the first column text'], style={'background-color': '#133E87',
                                                                   'height': '100vh',
                                                                   'border-radius': 8})
            ], span=3),

            dmc.Col([
                html.Div(['This is the second column text'], style={'background-color': '#F3F3E0',
                                                                    'height': '100vh',
                                                                    'border-radius': 8})
            ], span='auto'),
        ]),
        create_dropdown(df['Category'].unique(),
                        'Select category',
                        'category'),
        create_barchart('category')])
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
            Output(component_id='category-barchart', component_property='figure'),
            Input(component_id='category-dropdown', component_property='value')
        )
        def update_graph(*col_chosen):
            print(col_chosen)
            partition = self.df[self.df['Category'].isin(col_chosen[0])]
            print(partition.head())
            fig = px.histogram(partition, x='Segment', y='Sales', histfunc='avg')
            return fig
