import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output
import plotly.figure_factory as ff
from flask import Flask
import dash_bootstrap_components as dbc
from datetime import datetime,time
import dash_auth
#Load dataset
df = pd.read_csv(r"https://raw.githubusercontent.com/Jamemetals/daily/main/csq_matlab.csv?token=GHSAT0AAAAAACAITNMTYLEWHGLM7OR5IFOAZA6THKQ")
df['Time'] = pd.to_datetime(df['Time'])
df["Time"] = df["Time"] + pd.Timedelta(days = 76)

#Define function
def kW_each_power_meter_day(df):
    kW = px.area(df,x="Time",y=["DP-CH-1 MAIN (kW)",'DP-CH-2 MAIN (kW)','DP-CH-3 MAIN (kW)','DP-CH-4 MAIN (kW)','DP-CH-5 MAIN (kW)'])
    kW.update_layout(
        title='kW from each Power Meter',
        xaxis_title='Time',
        yaxis_title='kW'
    )
    return kW
def compare_kW_TR_day(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Total kWh"],
                        mode='lines+markers',
                        name="Total kW"))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Total TRh"],
                        mode='lines+markers',
                        name="Total TR"))
    fig.update_layout(title_text="kW and TR all day",
                      xaxis_title='Time'
                    )
    return fig
def pie_plot_kW_TR_day(df):
    pie1 = pd.DataFrame({"DP-CH-1" : [df["DP-CH-1 MAIN (kW)"].sum()],
                        "DP-CH-2(Chiller1,2)" : [df["DP-CH-2 MAIN (kW)"].sum()],
                        "DP-CH-3(Chiller3,4)" : [df["DP-CH-3 MAIN (kW)"].sum()],
                        "DP-CH-4(Chiller5,6)" : [df["DP-CH-4 MAIN (kW)"].sum()],
                        "DP-CH-5(Chiller7)" : [df["DP-CH-5 MAIN (kW)"].sum()]
                            })
    pie2 = pd.DataFrame({"BTU1" : [df['BTU Meter 1 (TR)'].sum()],
                        "BTU2" : [df['BTU Meter 2 (TR)'].sum()],
                        "BTU4" : [df['BTU Meter 4 (TR)'].sum()],
                        "BTU5" : [df['BTU Meter 5 (TR)'].sum()],
                            })
    DPCH_BTU = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    DPCH = go.Pie(labels=pie1.columns , values=pie1.loc[0].tolist(), textinfo='percent',insidetextorientation='radial',marker= dict(colors = px.colors.qualitative.Plotly))
    BTU = go.Pie(labels=pie2.columns, values=pie2.loc[0].tolist(), textinfo='percent',insidetextorientation='radial',marker= dict(colors = px.colors.qualitative.Plotly_r)
                                )
    DPCH_BTU.add_trace(DPCH,1,1)
    DPCH_BTU.add_trace(BTU,1,2)
    DPCH_BTU.update_traces(hole=.4, hoverinfo="label+percent+name")
    DPCH_BTU.update_layout(
        title_text="Total kW all day and Total TR all day, 20 Mar 2023",
        annotations=[dict(text='kW', x=0.19, y=0.5, font_size=20, showarrow=False),
                    dict(text='TR', x=0.80, y=0.5, font_size=20, showarrow=False)])
    return DPCH_BTU
def create_box_plot_day(df):
    df['Type_of_Peak'] = df['Time'].apply(lambda x: 'On-Peak' if pd.to_datetime('20/3/2023 8:45') < x < pd.to_datetime('20/3/2023 22:00') else 'Off-Peak')
    fig = go.Figure()
    fig.add_trace(go.Box(
        y=df["DP-CH-1 MAIN (kW)"],
        
        name="DP-CH-1 MAIN (kW)",
  
    ))
    fig.add_trace(go.Box(
        y=df["DP-CH-2 MAIN (kW)"],
        
        name="DP-CH-2 MAIN (kW)",
    
    ))
    fig.add_trace(go.Box(
        y=df["DP-CH-3 MAIN (kW)"],
        
        name="DP-CH-3 MAIN (kW)",
    
    ))
    fig.add_trace(go.Box(
        y=df["DP-CH-4 MAIN (kW)"],
        
        name="DP-CH-4 MAIN (kW)",
    
    ))
    fig.add_trace(go.Box(
        y=df["DP-CH-5 MAIN (kW)"],
        
        name="DP-CH-5 MAIN (kW)",
        
    ))
    fig.update_layout(
        title = 'Box plot of kW  from each Power Meter',
        yaxis_title='kW',
        boxmode='group' # group together boxes of the different traces for each value of x
    )
    return fig
def summary_day(df):

    data_matrix = [[' ', "DP-CH-1 MAIN (kW)",'DP-CH-2 MAIN (kW)','DP-CH-3 MAIN (kW)','DP-CH-4 MAIN (kW)','DP-CH-5 MAIN (kW)'],
               ['kW_mean', df["DP-CH-1 MAIN (kW)"].mean(),df["DP-CH-2 MAIN (kW)"].mean(),df["DP-CH-3 MAIN (kW)"].mean(),df["DP-CH-4 MAIN (kW)"].mean(),df["DP-CH-5 MAIN (kW)"].mean()],
               ['Max_kW', df["DP-CH-1 MAIN (kW)"].max(),df["DP-CH-2 MAIN (kW)"].max(),df["DP-CH-3 MAIN (kW)"].max(),df["DP-CH-4 MAIN (kW)"].max(),df["DP-CH-5 MAIN (kW)"].max()],
               ['Total kW', df["DP-CH-1 MAIN (kW)"].sum(),df["DP-CH-2 MAIN (kW)"].sum(),df["DP-CH-3 MAIN (kW)"].sum(),df["DP-CH-4 MAIN (kW)"].sum(),df["DP-CH-5 MAIN (kW)"].sum()]
               ]
    colorscale = [[0, '#4d004c'],[.5, '#f2e5ff'],[1, '#ffffff']]
    summary_day = ff.create_table(data_matrix, index=True)
    return summary_day
#Initiate the App
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])
server = app.server
auth = dash_auth.BasicAuth(app, {'james':'jamemetals123'})
#Build the components
#Design app layout
app.layout = html.Div(
    [
        dbc.Row([
            html.H1('Power and BTU meter Data Visualization Dashboard (20 Mar 2023)',style={'color':'blue','text-align':'center'})
        ]),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=kW_each_power_meter_day(df), style={'width': '96vh', 'height': '50vh'})]
            ), dbc.Col(
                [dcc.Graph(figure=compare_kW_TR_day(df), style={'width': '94vh', 'height': '50vh'})]
            )]
        ),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=pie_plot_kW_TR_day(df))]
            ), dbc.Col(
                [dcc.Graph(figure=create_box_plot_day(df))]
            )]
        ),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=summary_day(df))]
            )]
        ),
    ]
)
#Run the app
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
