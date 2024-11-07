import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px

from dash import html

from .components import create_dropdown, create_chart, create_radioitem, create_checklist

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

    second_subsection = html.Div([create_dropdown(df['State'].unique(),
                                                  'Select state',
                                                  'state',
                                                  multi=False,
                                                  value=df['State'].unique()[0]),
                                  create_chart('sales-state')])
        
    return [first_subsection, second_subsection]


def create_segment_section(df: pd.DataFrame) -> list[html.Div]:
    first_subsection = html.Div(create_dropdown(df['Category'].unique(),
                                  'Select category',
                                  'category-segment'))
    second_subsection = dmc.Grid([
            dmc.Col(create_chart('segment-category-pie',
                                  style={'height': '90%'}),
                    className='segment-charts',
                    span=4),
            dmc.Col(create_chart('sales-segment-category',
                                  style={'height': '90%'}),
                    className='segment-charts',
                    span='auto'),
    ], className='segment-subsection')
    third_subsection = html.Div(create_dropdown(df['Ship_Mode'].unique(),
                                  'Select ship Mode',
                                  'shipmode-segment'))
    forth_subsection = dmc.Grid([
            dmc.Col(create_chart('segment-shipmode-count',
                                 style={'height': '90%'}),
                    className='segment-charts',
                    span=4),
            dmc.Col(create_chart('sales-segment-shipmode',
                                 style={'height': '90%'}),
                    className='segment-charts',
                    span='auto'),
    ], className='segment-subsection')
    
        
    return [first_subsection, second_subsection, third_subsection, forth_subsection]


def create_category_section(df: pd.DataFrame) -> list[html.Div]:

    first_subsection = dmc.Grid([
        dmc.Col(create_radioitem(df['Category'].unique(),
                                  'Select category:',
                                  'category-category'),
                    span=2),
        dmc.Col(create_chart('category-category-pie',
                                  style={'height': '90%'}),
                    className='category-charts',
                    span=4),
        dmc.Col(create_chart('sales-category-category',
                                  style={'height': '90%'}),
                    className='category-charts',
                    span='auto'),
    ], className='category-subsection')
    second_subsection = dmc.Grid([
            dmc.Col(create_chart('subcategory-sales',
                                 style={'height': '90%'}),
                    className='category-charts',
                    span=6),
            dmc.Col(create_chart('category-shipmode-segment',
                                 style={'height': '90%'}),
                    className='category-charts',
                    span='auto'),
    ], className='category-subsection')
    
        
    return [first_subsection, second_subsection]


def create_region_section(df: pd.DataFrame) -> list[html.Div]:

    first_subsection = dmc.Grid([
        dmc.Col(create_checklist(df['Region'].unique(),
                                  'Select region:',
                                  'region-region'),
                    span=2),
        dmc.Col(create_chart('region-region-pie',
                                  style={'height': '90%'}),
                    className='region-charts',
                    span=4),
        dmc.Col(create_chart('sales-region-region',
                                  style={'height': '90%'}),
                    className='region-charts',
                    span='auto'),
    ], className='region-subsection')
    second_subsection = dmc.Grid([
            dmc.Col(create_chart('subregion-sales',
                                 style={'height': '90%'},
                                 figure=create_region_sales_figure(df)),
                    className='region-charts',
                    span=6),
            dmc.Col(create_chart('region-shipmode-segment',
                                 style={'height': '90%'}),
                    className='region-charts',
                    span='auto'),
    ], className='region-subsection')
    
        
    return [first_subsection, second_subsection]


def create_region_sales_figure(df: pd.DataFrame) -> list[html.Div]:
    sales = []
    for region in df['Region'].unique():
        sales.append(int(df[df['Region']==region]['Sales'].sum()/1000))
    df = df.groupby('Region', as_index=False)['Sales'].sum()
    region_sales_figure = px.bar(df,
                    y='Region',
                    x='Sales',
                    text='Sales',
                    color_discrete_sequence=px.colors.sequential.Viridis)
    region_sales_figure.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    region_sales_figure.update_layout(title=f"Sales of each sub_category for",)
    return region_sales_figure