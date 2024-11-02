import numpy as np
import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input


def create_overview_section(df: pd.DataFrame) -> html.Div:
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
    return first_subsection