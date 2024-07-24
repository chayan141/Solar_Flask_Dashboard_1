import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/inv_wise_data_distribution', name="Inv Wise Data Distribution 📊")

####################### LOAD DATASET #############################
plant_df = pd.read_excel("33 MW Charanka.xlsx",sheet_name='Inv Wise')



####################### HISTOGRAM ###############################
# def create_distribution(col_name="Generation (KWh)"):
#     return px.histogram(data_frame=plant_df, x=col_name, height=600)

####################### WIDGETS ################################
columns = ["Plant Availability", "Grid Availability", "Generation (KWh)", "Irradiation", "Plant PLF%", "Plant PR%", "Specific Yield", "Inv PR%", "Targeted PR %",'Total Generation in KWh']
inverter_options = [{'label': inv, 'value': inv} for inv in plant_df['Inv Name'].unique()]
dd = dcc.Dropdown(id="dist_column", options=columns, value="Generation (KWh)", 
                  placeholder="Select a Numerical Column",clearable=False)
dd2 = dcc.Dropdown(id='inv-drop',options=inverter_options, value=plant_df['Inv Name'].unique()[0],
            placeholder="Select Inverter Names", clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.P("Select Column:"),
    dd,
    html.Br(),
    dd2,
    html.Br(),
    dcc.Graph(id="histogram1")
])

####################### CALLBACKS ################################

# @callback(Output("histogram1", "figure"), [Input("dist_column", "value"),])
# def update_histogram(dist_column):
#     return create_distribution(dist_column)

@callback(
    dash.dependencies.Output('histogram1', 'figure'),
    [dash.dependencies.Input('dist_column', 'value'),
     dash.dependencies.Input('inv-drop', 'value')]
)
def update_histogram(selected_column, selected_inverter):
    filtered_df = plant_df[plant_df['Inv Name'] == selected_inverter]

    fig = px.histogram(filtered_df, x=selected_column, title=f'Distribution of {selected_column} for {selected_inverter}')
    return fig
