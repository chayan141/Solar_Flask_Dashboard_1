import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/plant_wise_data_distribution', name="Plant Wise Data Distribution 📊")

####################### LOAD DATASET #############################
plant_df = pd.read_excel("33 MW Charanka.xlsx",sheet_name='Plant Wise')



####################### HISTOGRAM ###############################
def create_distribution(col_name="Generation"):
    return px.histogram(data_frame=plant_df, x=col_name, height=600)

####################### WIDGETS ################################
columns = ["Generation", "Actual GTI KWh/m²", "Plant PR%", "Plant PLF%", "Specific Yield", "Generation Loss in MWh", "GHI (KWh/m2)", "Avg. Module  Temp (Deg. C)", "Temp. Corrected PR%"]
dd = dcc.Dropdown(id="dist_column", options=columns, value="Generation", clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.P("Select Column:"),
    dd,
    dcc.Graph(id="histogram")
])

####################### CALLBACKS ################################
@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
def update_histogram(dist_column1):
    return create_distribution(dist_column1)

