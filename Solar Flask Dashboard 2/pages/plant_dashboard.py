import pandas as pd
import dash
from dash import dcc, html, callback
from datetime import datetime as dt
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/plant_dashboard', name="Plant Dashboard 📈")

####################### DATASET #############################
plant_df = pd.read_excel("33 MW Charanka.xlsx",sheet_name='Plant Wise')

plant_df['Date'] = pd.to_datetime(plant_df['Date'])
unique_dates = plant_df['Date'].dt.date.unique()

plant_df['Base Gen. (KWh)'] = (plant_df['Target Generation']/plant_df['Target GTI KWh/m²'])/plant_df['Actual GTI KWh/m²']

layout=  html.Div([
    html.Div([
        html.Label('Select Start Date'),
        dcc.DatePickerSingle(
        id='start-date-picker',
        min_date_allowed=min(unique_dates),  # Set minimum allowed date
        max_date_allowed=max(unique_dates),  # Set maximum allowed date
        initial_visible_month=min(unique_dates),  # Set initial month to display
        date=min(unique_dates),  # Set initial selected date
        
        ),dcc.Graph(id='graph_1')
    ], style={'display': 'inline-block', 'width': '30%'}),
    html.Div([
        html.Label('Select End Date'),
        dcc.DatePickerSingle(
        id='end-date-picker',
        min_date_allowed=min(unique_dates),  # Set minimum allowed date
        max_date_allowed=max(unique_dates),  # Set maximum allowed date
        initial_visible_month=max(unique_dates),  # Set initial month to display
        date=max(unique_dates)  # Set initial selected date
    ),dcc.Graph(id='graph_2')], style={'display': 'inline-block', 'width': '30%'})])


####################### CALLBACKS ################################
@callback(
    [dash.dependencies.Output('graph_1', 'figure'),
     dash.dependencies.Output('graph_2', 'figure')],
    [dash.dependencies.Input('start-date-picker', 'date'),
     dash.dependencies.Input('end-date-picker', 'date')]
)

def update_graphs(start_date_str, end_date_str):
    start_date = dt.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = dt.strptime(end_date_str, '%Y-%m-%d').date()
    filtered_df = plant_df[(plant_df['Date'].dt.date >= start_date) & (plant_df['Date'].dt.date <= end_date)]

    filtered_df1 = filtered_df.groupby('Date').agg({'Plant PR%': 'mean', 'Plant PLF%': 'mean','Specific Yield':'mean','Target Generation':'sum','Target GTI KWh/m²':'sum',
                                                    'Shortfall (Net-Target)':'sum','Base Gen.':'sum','Shortfall (Net-Base)':'sum','Generation Loss in MWh':'sum',
                                                    'Actual GTI KWh/m²':'sum','Target GTI KWh/m²':'sum','GHI (KWh/m2)':'sum','Target GHI (KWh/m2)':'sum','Temp. Corrected PR%':'mean','Generation':'sum'}).reset_index()
    
    # Calculate the sums for Value1, Value2, and Value3 separately
    value1 = filtered_df1['Plant PR%'].mean()
    value2 = filtered_df1['Plant PLF%'].mean()
    value3 = filtered_df1['Specific Yield'].mean()

    # Create a DataFrame for the sums
    sums_df = pd.DataFrame({
        'Category': ['Plant PR%', 'Plant PLF%', 'Specific Yield'],
        'Total': [value1*100, value2*100, value3 ]
    })

    fig1 = px.bar(sums_df, x='Category', y='Total', labels={'Category': 'Category', 'Total': 'Total Value'},
             title='Plant Wise Data Parameters')
    
    value_1 = filtered_df1['Generation'].sum()
    value_2 = filtered_df1['Target Generation'].sum()
    value_3 = filtered_df1['Shortfall (Net-Target)'].sum()
    
    sums_df2 = pd.DataFrame({
        'Category1': ['Generation', 'Target Generation', 'Shortfall (Net-Target)'],
        'Total1': [value_1, value_2, value_3 ]
    })

    fig2 = px.bar(sums_df2, x='Category1', y='Total1', labels={'Category1': 'Category', 'Total1': 'Total Value'},
             title='Plant Wise Data Parameters')
    
    return fig1,fig2




