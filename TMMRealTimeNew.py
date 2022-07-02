import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import pandas as pd
from datetime import date, timedelta
import datetime
import math
import statistics
from furl import furl

treeID = 'TS001'
slopeID = 'SA2322'

def loadDf6(treeID,slopeID):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    df6 = pd.read_csv("DataCumulated2.csv")
    df6 = df6.sort_values('rs2Time')
    df6 = df6.loc[df6['slopeID'] == slopeID]
    df6 = df6.loc[df6['treeID'] == treeID]
    df6['rs2Time'] = pd.to_datetime(df6['rs2Time'])
    df6 = df6.drop('rs2Mean', 1)
    df6 = df6.drop('rs2STD', 1)
    df6 = df6.drop('rs2ComX', 1)
    df6 = df6.drop('rs2ComY', 1)
    df6 = df6.drop('rs2ComZ', 1)
    df6 = df6.drop_duplicates(subset='rs2Time', keep="first")
    current_time = datetime.datetime.now()
    previous_time = current_time - timedelta(hours=24)
    df6 = df6.loc[df6['rs2Time'] >= previous_time]
    return df6

def loadDf5(treeID,slopeID, hours):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    df5 = pd.read_csv("DataCumulated2.csv")
    df5 = df5.sort_values('rs2Time')
    df5 = df5.loc[df5['slopeID'] == slopeID]
    df5 = df5.loc[df5['treeID'] == treeID]
    df5 = df5.drop('rs2ComX', 1)
    df5 = df5.drop('rs2ComY', 1)
    df5 = df5.drop('rs2ComZ', 1)
    df5 = df5.drop('rawx', 1)
    df5 = df5.drop('rawy', 1)
    df5 = df5.drop('rawz', 1)
    df5['rs2Time'] = pd.to_datetime(df5['rs2Time'])
    current_time = datetime.datetime.now()
    previous_time = current_time - timedelta(hours=hours)
    df5 = df5.loc[df5['rs2Time'] >= previous_time]
    return df5

def loadDf2(treeID,slopeID):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    df2 = pd.read_csv("DataCumulated2.csv")
    df2 = df2.sort_values('rs2Time')
    df2 = df2.loc[df2['slopeID'] == slopeID]
    df2 = df2.loc[df2['treeID'] == treeID]
    current_time = datetime.datetime.now()
    previous_time = current_time - timedelta(weeks=12)
    df2['MeanDiff'] = df2.rs2Mean.diff()
    df2['Angle'] = df2.apply(lambda row: math.degrees(math.atan2(row.rs2ComY, row.rs2ComX)), axis=1)
    df2[['MeanDiff', 'Angle']] = df2[['MeanDiff', 'Angle']].fillna(value=0)
    # means = df2['rs2Mean'].to_list()
    # meanDiff = list()
    # meanDiff.append(0)
    # for i in range(1, len(means)):
    #     temp = means[i] - means[i-1]
    #     meanDiff.append(temp)
    # Y = df2['rs2ComY'].to_list()
    # X = df2['rs2ComX'].to_list()
    # angle = list()
    # for i in range(0, len(Y)):
    #     x = X[i]
    #     y = Y[i]
    #     if x >= -1000 and x <= 1000:
    #         if y >= -1000 and y <= 1000:
    #             angle.append(math.degrees(math.atan2(y, x)))
    #         else:
    #             angle.append(0)
    #     else:
    #         angle.append(0)
    # df2 = df2.assign(MeanDiff=pd.Series(meanDiff).values)
    # df2 = df2.assign(Angle=pd.Series(angle).values)
    df2['rs2Time'] = pd.to_datetime(df2['rs2Time'])
    df2 = df2.loc[df2['rs2Time'] >= previous_time]
    return df2

def loadDf(treeID,slopeID):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    current_time = datetime.datetime.now()
    previous_time = current_time - timedelta(weeks=12)
    df1 = pd.read_csv("Tasks_info.csv")
    for i in range(0, len(df1)):
        df1['Start'][i] = datetime.datetime.strptime(df1['Start'][i], '%d/%m/%Y').date()
    for i in range(0, len(df1)):
        df1['Finish'][i] = datetime.datetime.strptime(df1['Finish'][i], '%d/%m/%Y').date()
    df1['slopeID'] = df1['slopeID'].fillna(slopeID)
    df1['treeID'] = df1['treeID'].fillna(treeID)
    df1 = df1.loc[(df1['slopeID'] == slopeID) | (df1['slopeID'] == 'ALL'),:]
    df1 = df1.loc[(df1['treeID'] == treeID)| (df1['treeID'] == 'ALL'),:]
    df1['Start'] = pd.to_datetime(df1['Start'])
    df1['Finish'] = pd.to_datetime(df1['Finish'])
    df1 = df1.loc[df1['Finish'] >= previous_time]
    df1 = df1.sort_values('Finish')
    return df1

def loadDf4(df2):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    current_time = datetime.datetime.now() - timedelta(hours=6)
    previous_time = current_time - timedelta(hours=24)
    df2['rs2Time'] = pd.to_datetime(df2['rs2Time'])
    df4 = df2.loc[df2['rs2Time'] >= previous_time]
    return df4

def loadDf3(df1):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    current_time = datetime.datetime.now() - timedelta(hours=6)
    previous_time = current_time - timedelta(hours=24)
    df1['Start'] = pd.to_datetime(df1['Start'])
    df1['Finish'] = pd.to_datetime(df1['Finish'])
    df3 = df1.loc[df1['Finish'] >= previous_time]
    return df3

def drawFigNone():
    figNone = go.Figure().add_annotation(x=2, y=2,text="No Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
    return figNone

def drawFigure5(df5):
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    from plotly.subplots import make_subplots
    STD = df5['rs2STD'].to_list()
    MeanDiff = df5['rs2Mean'].to_list()
    Time = df5['rs2Time'].to_list()
    colors = ['#7a0504', (0.2, 0.7, 0.3), 'rgb(210, 60, 180)', 'rgb(180, 120, 10)']
    YLow = list()
    YHigh = list()
    for i in range(0, len(MeanDiff)):
        YLow.append(MeanDiff[i] - STD[i])
        YHigh.append(MeanDiff[i] + STD[i])
    figs5 = make_subplots(
        rows=1, cols=1,
        shared_xaxes=False,
        subplot_titles =(),
        specs=[[{}]]
    )
    fig = go.Figure([
        go.Scatter(
            x=Time,
            y=MeanDiff,
            line=dict(color='rgb(0,100,80)'),
            mode='lines',
            name="R2"
        ),
        go.Scatter(
            x=Time + Time[::-1],  # x, then x reversed
            y=YHigh + YLow[::-1],  # upper, then lower reversed
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        )
    ])
    for trace in fig.data:
        figs5.add_trace(trace, row=1, col=1)
    return figs5

def drawFigs1(Nodata1,Nodata2,df4,df3,figNone):
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    from plotly.subplots import make_subplots
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    colors = ['#7a0504', (0.2, 0.7, 0.3), 'rgb(210, 60, 180)']
    figs1 = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles =('Range of Fluctuation','', 'Timeline of Works and Events'),
        specs=[[{"rowspan": 2}], [{}], [{}]]
    )
    if Nodata1 == 0:
        STD = df4['rs2STD'].to_list()
        MeanDiff = df4['MeanDiff'].to_list()
        Time = df4['rs2Time'].to_list()
        YLow = list()
        YHigh = list()
        for i in range(0, len(MeanDiff)):
            YLow.append(MeanDiff[i] - STD[i])
            YHigh.append(MeanDiff[i] + STD[i])
        fig = go.Figure([
                go.Scatter(
                    x=Time,
                    y=MeanDiff,
                    line=dict(color='rgb(0,100,80)'),
                    mode='lines',
                    name="Mean Levels of Fluctuation"
                ),
                go.Scatter(
                    x=Time+Time[::-1], # x, then x reversed
                    y=YHigh+YLow[::-1], # upper, then lower reversed
                    fill='toself',
                    fillcolor='rgba(0,100,80,0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip",
                    showlegend=False
                )
            ])
        for trace in fig.data:
            figs1.add_trace(trace, row=1, col=1)
    else:
        for trace in figNone.data:
            figs1.add_trace(trace, row=1, col=1)
    if Nodata2 == 0:
        figg = ff.create_gantt(df3, colors=colors, index_col='Events', reverse_colors=True, show_colorbar=True)
        for trace in figg.data:
            figs1.add_trace(trace, row=3, col=1)
    else:
        for trace in figNone.data:
            figs1.add_trace(trace, row=1, col=1)
    figs1.update_layout(font = {"size": 15})
    figs1.update_yaxes(range=[-0.5, 0.5], row=1, col=1)
    #figs.update_yaxes(range=[1,8], row=1, col=1)
    figs1.update_yaxes(visible=False, showticklabels=False,row=3, col=1)
    return figs1

def drawFigs2(Nodata1,Nodata2,df2,df1,figNone):
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    from plotly.subplots import make_subplots
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    colors = ['#7a0504', (0.2, 0.7, 0.3), 'rgb(210, 60, 180)', 'rgb(180, 120, 10)']
    figs2 = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles =('Range of Fluctuation','', 'Timeline of Works and Events'),
        specs=[[{"rowspan": 2}], [{}], [{}]]
    )
    if Nodata1 == 0:
        STD = df2['rs2STD'].to_list()
        MeanDiff = df2['MeanDiff'].to_list()
        Time = df2['rs2Time'].to_list()
        YLow = list()
        YHigh = list()
        for i in range(0, len(MeanDiff)):
            YLow.append(MeanDiff[i] - STD[i])
            YHigh.append(MeanDiff[i] + STD[i])
        fig = go.Figure([
                go.Scatter(
                    x=Time,
                    y=MeanDiff,
                    line=dict(color='rgb(0,100,80)'),
                    mode='lines',
                    name="Mean Levels of Fluctuation"
                ),
                go.Scatter(
                    x=Time+Time[::-1], # x, then x reversed
                    y=YHigh+YLow[::-1], # upper, then lower reversed
                    fill='toself',
                    fillcolor='rgba(0,100,80,0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip",
                    showlegend=False
                )
            ])
        for trace in fig.data:
            figs2.add_trace(trace, row=1, col=1)
    else:
        for trace in figNone.data:
            figs2.add_trace(trace, row=1, col=1)
    if Nodata2 == 0:
        figg = ff.create_gantt(df1, colors=colors, index_col='Events', reverse_colors=True, show_colorbar=True)
        for trace in figg.data:
            figs2.add_trace(trace, row=3, col=1)
    else:
        for trace in figNone.data:
            figs2.add_trace(trace, row=1, col=1)
    figs2.update_layout(font = {"size": 15})
    figs2.update_yaxes(range=[-0.5, 0.5], row=1, col=1)
    figs2.update_yaxes(visible=False, showticklabels=False,row=3, col=1)
    return figs2

def drawFigure3(df2):
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    from plotly.subplots import make_subplots
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    r = df2['MeanDiff'].to_list()
    theta = df2['Angle'].to_list()
    radius = [0, statistics.mean(r) * 0.65, statistics.mean(r) * 0.65, 0]
    theta = [i for i in theta if i != 0]
    #theta = [abs(x) for x in theta
    direction = [0, min(theta), max(theta), 0]
    radius = [0, 1, 1, 0]
    fig3 = go.Figure(go.Scatterpolar(
        r=radius,
        theta=direction,
        mode="lines",
        fill="toself",
        fillcolor="#084E8A",
        line={"color": "rgba(32, 32, 32, .6)", "width": 1},
        opacity=0.8
    ))
    fig3.update_layout(
        font={"size": 15},
        polar={
            "angularaxis": {"showline": False, "tickcolor": "white", "rotation": 90, "direction": "clockwise",
                        "tickmode": "array", "tickvals": [0, 45, 90, 135, 180, 225, 270, 315],
                        "ticktext": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]}
             },
        showlegend=False,
    )
    fig3.update_polars(radialaxis_showticklabels=False)
    return fig3

def drawFigure6(df6):
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    from plotly.subplots import make_subplots
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    rawx = df6['rawx'].to_list()
    rawy = df6['rawy'].to_list()
    rawz = df6['rawz'].to_list()
    Time = df6['rs2Time'].to_list()
    colors = ['#7a0504', (0.2, 0.7, 0.3), 'rgb(210, 60, 180)', 'rgb(180, 120, 10)']
    figs6 = make_subplots(
        rows=1, cols=1,
        shared_xaxes=False,
        subplot_titles=(),
        specs=[[{}]]
    )
    fig = go.Figure([
        go.Scatter(
            x=Time,
            y=rawx,
            line=dict(color='rgb(255,0,0)'),
            mode='lines',
            name="Maximum X"
        ),
        go.Scatter(
            x=Time,
            y=rawy,
            line=dict(color='rgb(0,255,0)'),
            mode='lines',
            name="Maximum Y"
        ),
        go.Scatter(
            x=Time,
            y=rawz,
            line=dict(color='rgb(0,0,255)'),
            mode='lines',
            name="Maximum Z"
        ),
    ])
    for trace in fig.data:
        figs6.add_trace(trace, row=1, col=1)
    return figs6

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df2 = loadDf2(treeID,slopeID)
df1 = loadDf(treeID,slopeID)
df4 = loadDf4(df2)
df3 = loadDf3(df1)
df5 = loadDf5(treeID,slopeID,24)
df6 = loadDf6(treeID,slopeID)
figNone = drawFigNone()
Nodata1 = 0
if df4.empty:
    Nodata1 = 1
Nodata2 = 0
if df3.empty:
    Nodata2 = 1
figs1 = drawFigs1(Nodata1,Nodata2,df4,df3,figNone)
Nodata1 = 0
if df2.empty:
    Nodata1 = 1
Nodata2 = 0
if df1.empty:
    Nodata2 = 1
figs2 = drawFigs2(Nodata1,Nodata2,df2,df1,figNone)
fig3 = drawFigure3(df2)
figs5 = drawFigure5(df5)
figs6 = drawFigure6(df6)
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        # represents the URL bar, doesn't render anything
        dcc.Location(id='url', refresh=True),

        # content will be rendered in this element
        html.Div(id='content'),
    ]),
    html.Div([
        html.H1(children='Range of Fluctuation and Timeline of Works in the Past 24 Hours',style={'font-size': '40px','textAlign': 'center'}),

        dcc.Graph(
            id='graph1',
            figure=figs1
        ),
        dcc.Interval(
            id='interval-component1',
            interval=1000 * 1000,  # in milliseconds
            n_intervals=0
        )
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Range of Fluctuation and Timeline of Works in the Past 3 Months',style={'font-size': '40px','textAlign': 'center'}),

        dcc.Graph(
            id='graph2',
            figure=figs2
        ),
        dcc.Interval(
            id='interval-component2',
            interval=1000 * 1000,  # in milliseconds
            n_intervals=0
        )
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Direction of Movements',style={'font-size': '40px','textAlign': 'center'}),

        dcc.Graph(
            id='graph3',
            figure=fig3
        ),
        dcc.Interval(
            id='interval-component3',
            interval=1000 * 1000,  # in milliseconds
            n_intervals=0
        )
    ]),
    html.Div([
        html.H1(children='Mean Levels of Movements in the Past 24 Hours',
                style={'font-size': '40px', 'textAlign': 'center'}),

        dcc.Graph(
            id='graph5',
            figure=figs5
        ),
        dcc.Dropdown(
            id='fig_dropdown',
            options=[{'label': '24 Hours', 'value': '24H'},{'label': '48 Hours', 'value': '48H'}],
            value='24 Hours'
        ),
        dcc.Interval(
            id='interval-component5',
            interval=1000 * 1000,  # in milliseconds
            n_intervals=0
        )
    ]),
    html.Div([
        html.H1(children='Maximum Movements of the Axises in the Past 24 Hours',
                style={'font-size': '40px', 'textAlign': 'center'}),

        dcc.Graph(
            id='graph6',
            figure=figs6
        ),
        dcc.Interval(
            id='interval-component6',
            interval=1000 * 1000,  # in milliseconds
            n_intervals=0
        )
    ]),
])
@app.callback(Output('graph1', 'figure'),
              Input('interval-component1', 'n_intervals'))
def update_graph1_live(n):
    df2 = loadDf2(treeID,slopeID)
    df1 = loadDf(treeID,slopeID)
    df4 = loadDf4(df2)
    df3 = loadDf3(df1)
    figNone = drawFigNone()
    Nodata1 = 0
    if df4.empty:
        Nodata1 = 1
    Nodata2 = 0
    if df3.empty:
        Nodata2 = 1
    figs1 = drawFigs1(Nodata1, Nodata2, df4, df3, figNone)
    print(treeID)
    print(slopeID)
    return figs1

@app.callback(Output('graph2', 'figure'),
              Input('interval-component2', 'n_intervals'))
def update_graph2_live(n):
    df2 = loadDf2(treeID,slopeID)
    df1 = loadDf(treeID,slopeID)
    figs2 = drawFigs2(Nodata1,Nodata2,df2,df1,figNone)
    return figs2

@app.callback(Output('graph3', 'figure'),
              Input('interval-component3', 'n_intervals'))
def update_graph3_live(n):
    df2 = loadDf2(treeID,slopeID)
    fig3 = drawFigure3(df2)
    return fig3

@app.callback(Output('graph5', 'figure'),
              Input('fig_dropdown', 'value'))
def update_graph5_live(n):
    if n == '24H':
        df5 = loadDf5(treeID,slopeID,24)
    else:
        df5 = loadDf5(treeID, slopeID, 48)
    figs5 = drawFigure5(df5)
    return figs5

@app.callback(Output('graph6', 'figure'),
              Input('interval-component6', 'n_intervals'))
def update_graph6_live(n):
    df6 = loadDf6(treeID,slopeID)
    figs6 = drawFigure6(df6)
    return figs6

# @app.callback(Output('graph5', 'figure'),
#               Input('fig_dropdown', 'value'))
# def update_graph5_fig_dropdown(hours):
#     if hours == '24H':
#         df5 = loadDf5(treeID,slopeID,24)
#     else:
#         df5 = loadDf5(treeID, slopeID, 48)
#     figs5 = drawFigure5(df5)
#     return figs5

@app.callback(Output('content', 'children'),
              [Input('url', 'href')])
def _content(href: str):
    f = furl(href)
    param1= f.args['param1']
    param2= f.args['param2']
    global treeID
    treeID = param1
    global slopeID
    slopeID = param2
    return html.H1(children= 'Tree ID: ' + f'{param1}' + '    Slope ID:' + f'{param2}',style={'textAlign': 'center'})

PORT = 8050
ADDRESS = "0.0.0.0"
if __name__ == '__main__':
    app.run_server(host=ADDRESS,port=PORT, debug=True, threaded=True)
    #app.run_server(debug=True, threaded=True)
# http://127.0.0.1:8050/random?param1=TS001&param2=SA1707
# http://127.0.0.1:8050/random?param1=TS001&param2=SA1706
# http://127.0.0.1:8050/random?param1=TS058&param2=SA1860
# http://127.0.0.1:8050/random?param1=TS001&param2=SA2322
# http://127.0.0.1:8050/random?param1=TS008&param2=SA1745
# http://127.0.0.1:8050/random?param1=TS013&param2=SA1745
# http://127.0.0.1:8050/random?param1=TS015&param2=SA1745
# http://127.0.0.1:8050/random?param1=TS003&param2=SA1652