import dash_mantine_components as dmc
import numpy as np
import pandas as pd

from dash import html

from .components import create_dropdown, create_chart, create_radioitem, \
                        create_checklist, create_total_sales_figure, \
                        create_barchart_withsales
from .utils import get_color_palette


def create_overview_section(df: pd.DataFrame) -> list[html.Div]:
    total_customers = len(df['Customer_ID'].unique())
    total_products = len(df['Product_ID'])
    total_orders = len(df['Order_ID'])
    total_sales = np.round(df['Sales'].sum()/1000000)
    first_subsection = html.Div([
        html.Div([f'Total Customers = {total_customers}'],
                 className='total-boxes'),
        html.Div([f'Total Products = {total_products}'],
                 className='total-boxes'),
        html.Div([f'Total Orders = {total_orders}'],
                 className='total-boxes'),
        html.Div([f'Total Sales = {total_sales}M $'],
                 className='total-boxes'),
    ], className='first-overview-subsection')

    color_palette = pd.Series(get_color_palette(df['Category'].unique()))

    second_subsection = dmc.Grid([
            dmc.Col(create_chart('overview-category-sales',
                                 figure=create_barchart_withsales(df,
                                                                  grouped_col='Category',
                                                                  title="Sales of each category",
                                                                  partitioning=False,
                                                                  color_palette=color_palette)),
                    className='charts',
                    span=6),
            dmc.Col(create_chart('overview-total-sales',
                                 figure=create_total_sales_figure(df,
                                                                  title='Total Sales')),
                    className='charts',
                    span='auto'),
    ], className='category-subsection')

    third_subsection = dmc.Grid([
            dmc.Col(create_chart('overview-segment-sales',
                                 figure=create_barchart_withsales(df,
                                                                  grouped_col='Segment',
                                                                  title="Sales of each segment",
                                                                  partitioning=False,
                                                                  color_palette=color_palette)),
                    className='charts',
                    span=6),
            dmc.Col(create_chart('overview-shipmode-sales',
                                 figure=create_barchart_withsales(df,
                                                                  grouped_col='Ship_Mode',
                                                                  title="Sales of each ship mode",
                                                                  partitioning=False,
                                                                  color_palette=color_palette),),
                    className='charts',
                    span='auto'),
    ], className='category-subsection')
    return [first_subsection, second_subsection, third_subsection]


def create_segment_section(df: pd.DataFrame) -> list[html.Div]:
    first_subsection = html.Div(create_dropdown(df['Category'].unique(),
                                                'Select category',
                                                'category-segment'))
    second_subsection = dmc.Grid([
            dmc.Col(create_chart('segment-category-pie',),
                    className='charts',
                    span=4),
            dmc.Col(create_chart('sales-segment-category',),
                    className='charts',
                    span='auto'),
    ])
    third_subsection = html.Div(create_dropdown(df['Ship_Mode'].unique(),
                                                'Select ship Mode',
                                                'shipmode-segment'))
    forth_subsection = dmc.Grid([
            dmc.Col(create_chart('segment-shipmode-count',),
                    className='charts',
                    span=4),
            dmc.Col(create_chart('sales-segment-shipmode',),
                    className='charts',
                    span='auto'),
    ])
    return [first_subsection,
            second_subsection,
            third_subsection,
            forth_subsection]


def create_category_section(df: pd.DataFrame) -> list[html.Div]:

    first_subsection = dmc.Grid([
        dmc.Col(create_radioitem(df['Category'].unique(),
                                 'Select category:',
                                 'category-category'),
                span=2),
        dmc.Col(create_chart('category-category-pie',),
                className='charts',
                span=4),
        dmc.Col(create_chart('sales-category-category',),
                className='charts',
                span='auto'),
    ], className='category-subsection')
    second_subsection = dmc.Grid([
            dmc.Col(create_chart('subcategory-sales',),
                    className='charts',
                    span=6),
            dmc.Col(create_chart('category-shipmode-segment',),
                    className='charts',
                    span='auto'),
    ], className='category-subsection')
    return [first_subsection, second_subsection]


def create_region_section(df: pd.DataFrame) -> list[html.Div]:

    first_subsection = dmc.Grid([
        dmc.Col(create_checklist(df['Region'].unique(),
                                 'Select region:',
                                 'region-region'),
                span=2),
        dmc.Col(create_chart('region-region-pie',),
                className='charts',
                span=4),
        dmc.Col(create_chart('sales-region-region',),
                className='charts',
                span='auto'),
    ], className='region-subsection')
    second_subsection = dmc.Grid([
            dmc.Col(create_chart('subregion-sales',
                                 figure=create_barchart_withsales(df,
                                                                  grouped_col='Region',
                                                                  title="Sales of each region",
                                                                  partitioning=False)),
                    className='charts',
                    span=6),
            dmc.Col(create_chart('region-shipmode-segment',),
                    className='charts',
                    span='auto'),
    ], className='region-subsection')
    return [first_subsection, second_subsection]
