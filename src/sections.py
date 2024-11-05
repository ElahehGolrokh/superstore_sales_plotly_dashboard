import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px

from dash import Dash, html, dcc, callback, Output, Input

from .components import create_dropdown, create_chart

def create_overview_section(df: pd.DataFrame) -> list[html.Div]:
    total_customers = len(df['Customer_ID'].unique())
    total_products = len(df['Product_ID'])
    total_sales = np.round(df['Sales'].sum()/1000000)
    first_subsection = html.Div([
        html.Div([f'Total Customers = {total_customers}'],
                 className='total-boxes'),
        html.Div([f'Total Products = {total_products}'],
                 className='total-boxes'),
        html.Div([f'Total Sales = {total_sales}M $'],
                 className='total-boxes'),
    ], className='first-overview-subsection')

    second_subsection = html.Div([create_dropdown(df['City'].unique(),
                                                  'Select city',
                                                  'city'),
                                  create_chart('sales-city')])
        
    return [first_subsection, second_subsection]


def create_segment_section(df: pd.DataFrame) -> list[html.Div]:
    first_subsection = html.Div(create_dropdown(df['Category'].unique(),
                                  'Select category',
                                  'category-segment'))
    second_subsection = dmc.Grid([
            dmc.Col(create_chart('segment-category-pie'),
                    className='segment-charts',
                    span=4),
            dmc.Col(create_chart('sales-segment-category'),
                    className='segment-charts',
                    span='auto'),
    ], className='segment-subsection')
    third_subsection = html.Div(create_dropdown(df['Ship_Mode'].unique(),
                                  'Select ship Mode',
                                  'shipmode-segment'))
    forth_subsection = dmc.Grid([
            dmc.Col(create_chart('segment-shipmode-count'),
                    className='segment-charts',
                    span=4),
            dmc.Col(create_chart('sales-segment-shipmode'),
                    className='segment-charts',
                    span='auto'),
    ], className='segment-subsection')
    
        
    return [first_subsection, second_subsection, third_subsection, forth_subsection]
