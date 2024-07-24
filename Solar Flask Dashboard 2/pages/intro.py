import dash
from dash import html

dash.register_page(__name__, path='/', name="Introduction 😃")

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Div(children=[
        html.H2("33MW Charanka Dataset Overview"),
        "It is a solar groundmount site located in Charanka Gujrat.",
        html.Br(),html.Br(),
        "Here is Two Sheets in the dataset. First sheet is Plant wise dataset which have 24 features.",
        html.Br(), html.Br(),
        "And the next sheet is Inverter wise dataset which have 18 features.",
    ]),
], className="bg-light p-4 m-2")