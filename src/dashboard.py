from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

def get_app():
    app = Dash()

    app.layout = [
        html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    ]
    return app