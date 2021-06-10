import dash
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import time
# from get_shopee_comments import get_shopee_comments_in_pickle_file
# export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
#source venv/bin/activate
from rq.exceptions import NoSuchJobError
from rq.job import Job
from .core import conn,queue,app
from .tasks import slow_loop
from dash.dependencies import Input, Output, State
import uuid
import redis
from rq import Queue
import os
from collections import namedtuple
import flask
import base64
import datetime
import io
import pickle5 as pickle
Result = namedtuple(
    "Result", ["result", "progress", "collapse_is_open", "finished_data"]
)
# source venv/bin/activate
# data = pd.read_csv("avocado.csv")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)

# external_stylesheets = [
#     {
#         "href": "//db.onlinewebfonts.com/c/7e0f75fa1eb5ee523ae2961d4e7a11a6?family=Noway"
#         "family=text/css",
#         "rel": "stylesheet",
#     },
    
#     dbc.themes.BOOTSTRAP
# ]

# external_scripts = [
#     {'src': 'assets/custom.js'},
 
# ]
# app = dash.Dash(server=flask.Flask(__name__), \
#                 external_stylesheets=external_stylesheets,\
#                 external_scripts=external_scripts,)

# queue=Queue(connection=conn)

context_module=html.Div(children=[
                         
                        #Header
                        html.H1(children="Natural Language AI",
                                style={'font-size':'100',}),
                        
                        html.H4(children="Derive insights from unstructured text using LTRACK2.0",
                                style={'font-weight':'200','font-size':'65'}),
                        html.Div( dbc.Button("Try it for free",disabled=True, className="custom_button",href="#nlp_demo",),
                                 style={"padding-top":"20px","padding-bottom":"20px"},
                                 className="wrap"),
                        ##Introduction
                        html.Section(
                            id="introduction",
                            children=[
                                html.H2(children="Insightful text analysis",
                                        style={'font-weight':'400'}),
                                dbc.Row([
                                dbc.Col(html.P(children="Natural Language uses machine learning to reveal the structure and meaning of text. You can extract \
                                information about people, places, and events, and better understand social media sentiment and customer conversations. \
                                Natural Language AI enables you to analyze text and also integrate it with your document storage on Cloud Storage.",
                                style={'line-height':'28px','font-weight':'400','color':'#5f6368'}),),
                                dbc.Col(
                                    html.Img(src="assets/Pic1.png",
                                                 style={"width":'450px','height':'350px','padding-right':'100px','padding-bottom':'100px'}),
                                                 style={"width":'500px','height':'400px'}),
                                ],
                                style={'display':'flex',"justify-content": "space-evenly"}
                                )
                            ],
                            style={"padding-top":"50px"}
                        ),
                        ##DELIDER
                        html.Div(
                         style={"width":"60px","height":"3px","display":"block","background":"#d183a5"}
                        ),
                        ##Overview
                        html.Section(
                            id="request-response",
                            children=[
                                dbc.Row([
                                        dbc.Col([
                                        html.H3(children="AutoML"),
                                        
                                        html.P(children="Train your own high-quality machine learning custom models to classify, extract, and detect sentiment with minimum effort and machine learning expertise using Vertex AI for natural language, powered by AutoML. You can use the AutoML UI to upload your training data and test your custom model without a single line of code.",
                                        style={'line-height':'28px','font-weight':'400','color':'#5f6368'}),
                                        ],),
                        
                                        dbc.Col([
                                        html.H3(children="Natural Language API"),
                                        
                                        html.P(children="The powerful pre-trained models of the Natural Language API empowers developers to easily apply natural language understanding (NLU) to their applications with features including sentiment analysis, entity analysis, entity sentiment analysis, content classification, and syntax analysis.",
                                        style={'line-height':'28px','font-weight':'400','color':'#5f6368'}),
                                        ],),

                                        dbc.Col([
                                        html.H3(children="Insights from customers"),
                                        
                                        html.P(children="Use entity analysis to find and label fields within a document — including emails, chat, and social media — and then sentiment analysis to understand customer opinions to find actionable product and UX insights.",
                                        style={'line-height':'28px','font-weight':'400','color':'#5f6368'}),
                                        ],),
                                        ],
                                    className="horizontal")
                                ],
                                style={"padding-top":"30px"}
                        ),

                        ##Demo
                        html.Section(
                            id="nlp_demo",
                            children=[
                                html.H2(children="Natural Language API demo",
                                        style={"text-align":"center","font-size":"40px"}),
                                dbc.InputGroup(
                                    [dbc.InputGroupAddon("Try the API", addon_type="prepend", style={"text-align":"center","font-weight":"50px"}), 
                                    dbc.Input(id="text",placeholder="Enter text to be analyzed...",type="url")],
                                    size="lg",
                                    style={"padding-top":"50px"}),
                                html.Br(),
                                html.Div(dbc.Button("Analyse", id="summit_button",outline=True, className="simple_button",n_clicks=0),
                                 style={"padding-top":"20px","padding-bottom":"20px","text-align":"center"}),  
                                # html.Div(dbc.Progress(id="progress_test", color="success",animated=True,className="mb-3",value=25)),
                                dcc.Interval(id="interval", interval=50000),
                                dbc.Spinner(html.Div(id="loading-output")),

                                # dbc.Collapse(dbc.Progress(id="progress", color="success",animated=True,className="mb-3",value=15), id="collapse"),
                                # html.Br(),
                                # html.P(id="output"),

                                dcc.Upload(
                                        id='upload-data',
                                        children=html.Div([
                                            'Drag and Drop or ',
                                            html.A('Select Files')
                                        ]),
                                        style={
                                            'width': '100%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },
                                    ),
                                    html.Div(id='output-data-upload'),
                                html.Div([
                                    dbc.Button(
                                        "*Support Language",
                                        id="collapse-button",
                                        outline=True, 
                                        color="primary", 
                                        className="mr-1",
                                    ),
                                    dbc.Collapse(
                                        dbc.Card(dbc.CardBody("This content is hidden in the collapse")),
                                        id="collapse_",
                                    ),
                                ],
                                    style={"padding-top":"30px"})
                            ]
                        ),
                    ],
                    ),

scrolling_bar= html.Nav(
                    className="section-nav",
                    children=[
                        html.Listing(
                            children="NATURAL LANGUAGE API",
                            style={'font-family':"'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"}
                        ),
                        html.Ol(
                            children=[
                                
                                html.Listing(
                                    html.A(href="#introduction",
                                        children="Introduction")
                                ),
                                html.Listing(
                                    html.A(href="#request-response",
                                        children="Benefits")
                                ),
                                html.Listing(
                                    html.A(href="#nlp_demo",
                                        children="Natural Language API demo")
                                ),
                            html.Listing(
                                    html.A(href="#links",
                                    children="Links",
                                    className="")
                                    ),
                                html.Listing(
                                    html.A(href="#expanders",
                                    children="Expanders",
                                    className="")
                                    ),
                            ],
                        ),
                    ],
                    style={"padding-left":'80px','position':'sticky'})
                
horizontal_display=html.Div(
    dbc.Row([
        dbc.Col(scrolling_bar,width=3),
        dbc.Col(context_module)
       ],
        className="horizontal"
    )
)

app.layout = html.Div(
    children=[
        html.Div([
            dbc.Row([
                dbc.Col(html.H2(children="LTrack2.0",style={"padding-left":"95px"}),md=8),
                dbc.Col(dbc.Nav(
                    [          ##place to generate output
                        dcc.Store(id="submitted-store"),
                        dcc.Store(id="finished-store"),
                        # html.Div(
                        dbc.NavLink("Contact", disabled=True, href="#",style={"font-family":"sans-serif","font-size":"18px",}),
                        dbc.NavLink("About",disabled=True, href="#",style={"font-family":"sans-serif","font-size":"18px"}),
                        dbc.NavLink("Terms",disabled=True,href="#",style={"font-family":"sans-serif","font-size":"18px"}),
                    ]),style={"justify-content": "space-evenly"},
                    )
                ],
                justify="between",),],
            className="header",
           ),

        html.Div(
            horizontal_display,
        )
    ],
)
##
# current_file_name=""
# def parse_contents(contents, filename):
#     global current_file_name
#     content_type, content_string = contents.split(',')
#     decoded = base64.b64decode(content_string)
#     try:
#         current_file_name=filename
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#             pickle.dump(df,open(f"storage_folder/{filename}.pickle","wb"))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])

# @app.callback(Output('output-data-upload', 'children'),
#               Input('upload-data', 'contents'),
#               State('upload-data', 'filename'),
#               State('upload-data', 'last_modified'))
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children

#Percentage Update
previous_click=0
@app.callback(
    Output("loading-output", "children"),
    [Input("summit_button", "n_clicks")],
    [State("text", "value")],
)
def submit(n_clicks, text):
    """
    Submit a job to the queue, log the id in submitted-store
    """
    global previous_click
    if text:
        if previous_click!=n_clicks:
            slow_loop(text)
    return  dbc.Alert("This is a primary alert", color="primary"),

# @app.callback(
#     [
#         Output("output", "children"),
#         Output("progress", "value"),
#         Output("collapse", "is_open"),
#         Output("finished-store", "data"),
#     ],
#     [Input("interval", "n_intervals")],
#     [State("submitted-store", "data")],
# )
# def retrieve_output(n, submitted):
#     """
#     Periodically check the most recently submitted job to see if it has
#     completed.
#     """
#     if n and submitted:
#         try:
#             job = Job.fetch(submitted["id"], connection=conn)
#             if job.get_status() == "finished":
#                 # job is finished, return result, and store id
#                 return Result(
#                     result=job.result,
#                     progress=100,
#                     collapse_is_open=False,
#                     finished_data={"id": submitted["id"]},
#                 )

#             # job is still running, get progress and update progress bar
#             progress = job.meta.get("progress", 0)
#             return Result(
#                 result=f"Processing - {progress:.1f}% complete",
#                 progress=progress,
#                 collapse_is_open=True,
#                 finished_data=dash.no_update,
#             )
#         except NoSuchJobError:
#             # something went wrong, display a simple error message
#             return Result(
#                 result="Error: result not found...",
#                 progress=None,
#                 collapse_is_open=False,
#                 finished_data=dash.no_update,
#             )
#     # nothing submitted yet, return nothing.
#     return Result(
#         result=None, progress=None, collapse_is_open=False, finished_data={}
#     )

# @app.callback(
#     Output("interval", "disabled"),
#     [Input("submitted-store", "data"), Input("finished-store", "data")],
# )
# def disable_interval(submitted, finished):
#     if submitted:
#         if finished and submitted["id"] == finished["id"]:
#             # most recently submitted job has finished, no need for interval
#             return True
#         # most recent job has not yet finished, keep interval going
#         return False
#     # no jobs submitted yet, disable interval
#     return True 

@app.callback(
    Output("collapse_", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [dash.dependencies.State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# if __name__ == "__main__":
#     app.run_server(debug=True, host=os.getenv("APP_HOST", "127.0.0.1"))