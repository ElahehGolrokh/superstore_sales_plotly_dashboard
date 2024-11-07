import dash_mantine_components as dmc
import plotly.express as px
import pandas as pd

from dash import Dash, html, dcc, callback, Output, Input

from .sections import create_overview_section, create_segment_section, create_category_section, create_region_section
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
        # Chang the content based on the selected tab
        @app.callback(
            Output(component_id='tabs-content', component_property='children'),
            Input(component_id='tabs', component_property='value')
        )
        def update_tab_contents(tab):
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

        # Overview tab, linechart callbacks
        @app.callback(
            Output(component_id='sales-state-chart', component_property='figure'),
            Input(component_id='state-dropdown', component_property='value')
        )
        def update_sales_state(*col_chosen):
            partition = self.df[self.df['State'].isin(col_chosen)]
            partition = partition.groupby(['Year', 'Month'], as_index=False)['Sales'].sum()
            fig = px.line(partition,
                        x="Month",
                        y="Sales",
                        color="Year",
                        hover_name="Year",
                        line_shape="spline",
                        render_mode="svg",
                        markers=True)
            return fig

        # Segment tab, first row callbacks
        @app.callback(
            [Output(component_id='segment-category-pie-chart', component_property='figure'),
             Output(component_id='sales-segment-category-chart', component_property='figure'),],
            Input(component_id='category-segment-dropdown', component_property='value')
        )
        def update_segment_category(*col_chosen):
            # partition = self.df.groupby(['Segment'], as_index=False)[['Row_ID', 'Category']].count()
            color_palette1 = pd.Series(get_color_palette(self.df['Segment'].unique()))
            partition = self.df[self.df['Category'].isin(col_chosen[0])]
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
        
        # Category tab, first row callbacks
        @app.callback(
            [Output(component_id='category-category-pie-chart', component_property='figure'),
             Output(component_id='sales-category-category-chart', component_property='figure'),],
            Input(component_id='category-category-radioitem', component_property='value')
        )
        def update_category_shipmode(col_chosen):
            print(col_chosen)
            # partition = self.df.groupby(['Segment'], as_index=False)[['Row_ID', 'Category']].count()
            # color_palette1 = pd.Series(get_color_palette(self.df['Segment'].unique()))
            partition = self.df[self.df['Category']==col_chosen]
            print('partition = ', partition)
            # partition.loc[partition['Sub_Category'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
            fig1 = px.pie(partition,
                          names='Sub_Category',
                          title='Sahres of each sub-category',
                          color_discrete_sequence=px.colors.sequential.Viridis)
            fig1.update_layout(title=f"Sub_Category Shares for {col_chosen}",)
            partition = self.df[self.df['Category']==col_chosen]
            partition = partition.groupby(['Year', 'Month'], as_index=False)['Sales'].sum()
            fig2 = px.line(partition,
                        x="Month",
                        y="Sales",
                        color="Year",
                        hover_name="Year",
                        line_shape="spline",
                        render_mode="svg",
                        markers=True)
            fig2.update_layout(title=f"Monthly sales for {col_chosen}",)
            return fig1, fig2
        
        # Category tab, second row callbacks
        @app.callback(
            [Output(component_id='subcategory-sales-chart', component_property='figure'),
             Output(component_id='category-shipmode-segment-chart', component_property='figure')],
            Input(component_id='category-category-radioitem', component_property='value')
        )
        def update_category_shipmode(col_chosen):
            partition = self.df[self.df['Category']==col_chosen]
            sales = []
            for sub_cat in partition['Sub_Category'].unique():
                sales.append(int(partition[partition['Sub_Category']==sub_cat]['Sales'].sum()/1000))
            partition1 = partition.groupby('Sub_Category', as_index=False)['Sales'].sum()
            fig1 = px.bar(partition1,
                          y='Sub_Category',
                          x='Sales',
                          text='Sales',
                          color_discrete_sequence=px.colors.sequential.Viridis)
            fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
            fig1.update_layout(title=f"Sales of each sub_category for {col_chosen}",)

            color_palette = get_color_palette(self.df['Ship_Mode'].unique())
            partition2 = partition.groupby(by=["Segment", "Ship_Mode"]).size().reset_index(name="counts")
            fig2 = px.bar(data_frame=partition2,
                          x="Segment",
                          y="counts",
                          color="Ship_Mode",
                          barmode="group",
                          color_discrete_map=color_palette)
            fig2.update_layout(title=f"Ship mode Shares of each segment for {col_chosen}",)
            return fig1, fig2
        
        # region tab, first row callbacks
        @app.callback(
            [Output(component_id='region-region-pie-chart', component_property='figure'),
             Output(component_id='sales-region-region-chart', component_property='figure'),],
            Input(component_id='region-region-checklist', component_property='value')
        )
        def update_region_first(*col_chosen):
            partition = self.df[self.df['Region'].isin(col_chosen[0])]
            fig1 = px.pie(partition,
                          names='Region',
                          title='Sahres of each Region',
                          color_discrete_sequence=px.colors.sequential.Viridis)
            partition = partition.groupby(['Year', 'Month'], as_index=False)['Sales'].sum()
            fig2 = px.line(partition,
                        x="Month",
                        y="Sales",
                        color="Year",
                        hover_name="Year",
                        line_shape="spline",
                        render_mode="svg",
                        markers=True)
            fig2.update_layout(title=f"Monthly sales for {col_chosen}",)
            return fig1, fig2
        
        # Region tab, second row callbacks
        @app.callback(
            Output(component_id='region-shipmode-segment-chart', component_property='figure'),
            Input(component_id='region-region-checklist', component_property='value')
        )
        def update_region_second(*col_chosen):
            partition = self.df[self.df['Region'].isin(col_chosen[0])]
            fig = px.choropleth(data_frame=partition,
                                locationmode="USA-states",
                                locations='State_Abbrev',
                                color='Sales',
                                color_continuous_scale="Viridis",
                                scope="usa",
                                labels={'unemp':'unemployment rate'}
                                )
            return fig
