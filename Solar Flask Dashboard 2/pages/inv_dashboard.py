import pandas as pd
import dash
from dash import dcc, html, callback
from datetime import datetime as dt
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/inv_dashboard', name="Inverter Dashboard 📊")

####################### DATASET #############################
inv_df = pd.read_excel("33 MW Charanka.xlsx", sheet_name='Inv Wise')
unique_inverters = inv_df['Inv Name'].unique()
inv_df['Date'] = pd.to_datetime(inv_df['Date'])
unique_dates = inv_df['Date'].dt.date.unique()

layout = html.Div([
    html.Div([
        html.Label('Select Start Date'),
        dcc.DatePickerSingle(
        id='start-date-picker',
        min_date_allowed=min(unique_dates),  # Set minimum allowed date
        max_date_allowed=max(unique_dates),  # Set maximum allowed date
        initial_visible_month=min(unique_dates),  # Set initial month to display
        date=min(unique_dates),  # Set initial selected date
        
        )
    ], style={'display': 'inline-block', 'width': '30%'}),
    html.Div([
        html.Label('Select End Date'),
        dcc.DatePickerSingle(
        id='end-date-picker',
        min_date_allowed=min(unique_dates),  # Set minimum allowed date
        max_date_allowed=max(unique_dates),  # Set maximum allowed date
        initial_visible_month=max(unique_dates),  # Set initial month to display
        date=max(unique_dates)  # Set initial selected date
    )], style={'display': 'inline-block', 'width': '30%'}),
    html.Div([
        html.Label('Select Inverter'),
        dcc.Dropdown(
        id='inverter-dropdown',
        multi=True,
        options=[{'label': inv, 'value': inv} for inv in unique_inverters],
        value=unique_inverters[0],  # Default value
        placeholder="Select an Inverter"
    )
    ], style={'display': 'inline-block', 'width': '30%'}),

    html.Div([
        dcc.Graph(id='graph1')
    ]),
    html.Div([
        dcc.Graph(id='graph2')
    ]),
    html.Div([
        dcc.Graph(id='graph3')
    ])

    ])


####################### CALLBACKS ################################
@callback(
    [dash.dependencies.Output('graph1', 'figure'),
     dash.dependencies.Output('graph2', 'figure'),
     dash.dependencies.Output('graph3', 'figure')],
    [dash.dependencies.Input('start-date-picker', 'date'),
     dash.dependencies.Input('end-date-picker', 'date'),
     dash.dependencies.Input('inverter-dropdown', 'value')]
)
def update_graphs(start_date_str, end_date_str,selected_inv):
    start_date = dt.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = dt.strptime(end_date_str, '%Y-%m-%d').date()
    filtered_df = inv_df[(inv_df['Date'].dt.date >= start_date) & (inv_df['Date'].dt.date <= end_date)]
    if selected_inv:  # Check if inverter names are selected
        if isinstance(selected_inv, str):  # Convert single string to a list
            selected_inv = [selected_inv]
        filtered_df = filtered_df[filtered_df['Inv Name'].isin(selected_inv)]
    
    df1 = filtered_df.groupby('Inv Name')[['Inv PR%','Inv PLF%','Targeted PR %','Specific Yield']].mean().reset_index()
    df2 = filtered_df.groupby('Inv Name')['Inv PLF%'].mean().reset_index()
    df3 = filtered_df.groupby('Inv Name')['Specific Yield'].mean().reset_index()

    df1['Inv PR%'] = df1['Inv PR%']*100
    df1['Inv PLF%'] = df1['Inv PLF%']*100
    df1['Targeted PR %'] = df1['Targeted PR %']*100

    # Updating Chart 1
    fig1 = go.Figure()
    threshold = 80  # You can set your desired threshold value

    fig1.add_trace(go.Bar(
        x=df1['Inv Name'],
        y=df1['Inv PR%'],
        name='Inv Wise PR%',
        marker_color=['red' if val < threshold else 'skyblue' for val in df1['Inv PR%']],
        yaxis='y'  # Assign to primary y-axis
    ))

    # Create a line chart
    fig1.add_trace(go.Scatter(
        x=df1['Inv Name'],
        y=df1['Inv PLF%'],
        mode='lines+markers',
        name='Inv Wise PLF%',
        line=dict(color='orange', width=2),
        yaxis='y2'  # Assign to secondary y-axis
    ))
    

    # Update layout
    fig1.update_layout(
        title='Inv Wise PR% & PLF%',
        title_x=0.5,
        xaxis=dict(title='Inv Name'),
        yaxis=dict(title='Inv PR%'),
        yaxis2=dict(
        title='Inv Wise PLF%',
        overlaying='y',
        side='right')
    )

    #----------Method 2 for graph 1 ----------


    # # Create a bar chart trace
    # x_values = df1['Inv Name']
    # y_values_bar = df1['Inv PR%']
    # y_values_line1 = df1['Inv PLF%']
    # y_values_line2 = df1['Targeted PR %']
    # trace_bar = go.Bar(x=x_values, y=y_values_bar, name='Inv PR%')

    # threshold = 0.80  # You can set your desired threshold value

    # # Create traces for bars above and below the threshold
    # trace_above_threshold = go.Bar(
    #     x=x_values[y_values_bar >= threshold],
    #     y=y_values_bar[y_values_bar >= threshold],
    #     name='Above Threshold',
    #     marker=dict(color='green')
    # )

    # trace_below_threshold = go.Bar(
    #     x=x_values[y_values_bar < threshold],
    #     y=y_values_bar[y_values_bar < threshold],
    #     name='Below Threshold',
    #     marker=dict(color='red')
    # )

    # fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    # # Create a line chart trace
    # fig1.add_trace(go.Scatter(x=x_values, y=y_values_line1, mode='lines+markers', name='Inv PR%',line=dict(color='blue')), secondary_y=False)
    # fig1.add_trace(go.Scatter(x=x_values, y=y_values_line2, mode='lines+markers', name='Targeted PR %',line=dict(color='yellow')), secondary_y=True)

    # # Add bar chart trace to the secondary y-axis
    # fig1.add_trace(trace_above_threshold, secondary_y=False)
    # fig1.add_trace(trace_below_threshold, secondary_y=False)

    # # Update the layout
    # fig1.update_layout(xaxis=dict(title='Inv Name',showticklabels=True,tickmode='array', dtick=1),
    #                 legend=dict(x=0.5, y=1.1),
    #                 )

    # # Update the y-axis labels
    # fig1.update_yaxes(title_text="Inv Wise PR%", secondary_y=False)
    # fig1.update_yaxes(title_text="Inv Wise PLF%", secondary_y=True) 



    # # --------Update second graph------------
    fig2 = go.Figure()
    threshold = 18  # You can set your desired threshold value

    fig2.add_trace(go.Bar(
        x=df1['Inv Name'],
        y=df1['Inv PLF%'],
        name='Inv Wise PLF%',
        marker_color=['red' if val < threshold else 'skyblue' for val in df1['Inv PR%']],
        yaxis='y'  # Assign to primary y-axis
    ))

    # Create a line chart
    fig2.add_trace(go.Scatter(
        x=df1['Inv Name'],
        y=df1['Specific Yield'],
        mode='lines+markers',
        name='Inv Wise Specific Yield',
        line=dict(color='orange', width=2),
        yaxis='y2'  # Assign to secondary y-axis
    ))
    
    # Update layout
    fig2.update_layout(
        title='Inv Wise PLF% & Specific Yield',
        title_x=0.5,
        xaxis=dict(title='Inv Name'),
        yaxis=dict(title='Inv PLF%'),
        yaxis2=dict(
        title='Inv Wise ',
        overlaying='y',
        side='right')
    )

    #-----------Update third graph--------------
    fig3 = px.bar(df3, x='Inv Name', y='Specific Yield', title='Inv Wise PLF%')


    return fig1,fig2,fig3



