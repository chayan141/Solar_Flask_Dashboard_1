import pandas as pd
import dash
from dash import html, dash_table, dcc
import plotly.graph_objects as go

dash.register_page(__name__, path='/inv_wise_data', name=" Inv Wise Dataset 📋")

####################### LOAD DATASET #############################
inv_df = pd.read_excel("33 MW Charanka.xlsx",sheet_name='Inv Wise')

# Define columns to convert to percentages
columns_to_convert = ['Plant Availability','Grid Availability','Inv PR%','Inv PLF%','Targeted PR %']

# Convert specific columns to percentages
for col in columns_to_convert:
    inv_df[col] = (inv_df[col] / inv_df[col].sum()) * 100

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    dash_table.DataTable(data=inv_df.to_dict('records'),
                         page_size=20,
                         style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
                         style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
                        ),
])