import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import pandas as pd
from datetime import date, timedelta
import datetime
import math
import statistics
from furl import furl

treeID = 'TS008'
slopeID = 'SA1745'

def loadDf2(treeID,slopeID):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    df2 = pd.read_csv("DataCumulated2.csv")
    df2 = df2.sort_values('rs2Time')
    df2 = df2.loc[df2['slopeID'] == slopeID]
    df2 = df2.loc[df2['treeID'] == treeID]
    current_time = datetime.datetime.now()
    previous_time = current_time - timedelta(weeks=12)
    means = df2['rs2Mean'].to_list()
    meanDiff = list()
    meanDiff.append(0)
    for i in range(1, len(means)):
        temp = means[i] - means[i-1]
        meanDiff.append(temp)
    Y = df2['rs2ComY'].to_list()
    X = df2['rs2ComX'].to_list()
    angle = list()
    for i in range(0, len(Y)):
        x = X[i]
        y = Y[i]
        if x >= -1000 and x <= 1000:
            if y >= -1000 and y <= 1000:
                angle.append(math.degrees(math.atan2(y, x)))
            else:
                angle.append(0)
        else:
            angle.append(0)
    df2 = df2.assign(MeanDiff=pd.Series(meanDiff).values)
    df2 = df2.assign(Angle=pd.Series(angle).values)
    df2['rs2Time'] = pd.to_datetime(df2['rs2Time'])
    df2 = df2.loc[df2['rs2Time'] >= previous_time]
    return df2

def loadDf(treeID,slopeID):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    current_time = datetime.datetime.now()
    previous_time = current_time - timedelta(weeks=12)
    df = pd.read_csv("Tasks_info.csv")
    for i in range(0, len(df)):
        df['Start'][i] = datetime.datetime.strptime(df['Start'][i], '%d/%m/%Y').date()
    for i in range(0, len(df)):
        df['Finish'][i] = datetime.datetime.strptime(df['Finish'][i], '%d/%m/%Y').date()
    df['slopeID'] = df['slopeID'].fillna(slopeID)
    df['treeID'] = df['treeID'].fillna(treeID)
    df = df.loc[(df['slopeID'] == slopeID) | (df['slopeID'] == 'ALL'),:]
    df = df.loc[(df['treeID'] == treeID)| (df['treeID'] == 'ALL'),:]
    df['Start'] = pd.to_datetime(df['Start'])
    df['Finish'] = pd.to_datetime(df['Finish'])
    df = df.loc[df['Finish'] >= previous_time]
    df = df.sort_values('Finish')
    return df

def loadDf4(df2):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    current_time = datetime.datetime.now() + timedelta(hours=-6)
    previous_time = current_time - timedelta(hours=24)
    df2['rs2Time'] = pd.to_datetime(df2['rs2Time'])
    df4 = df2.loc[df2['rs2Time'] >= previous_time]
    return df4

def loadDf3(df):
    import pandas as pd
    from datetime import date, timedelta
    import datetime
    import math
    import statistics
    current_time = datetime.datetime.now()
    previous_time = current_time - timedelta(hours=24)
    df['Start'] = pd.to_datetime(df['Start'])
    df['Finish'] = pd.to_datetime(df['Finish'])
    df3 = df.loc[df['Finish'] >= previous_time]
    return df3

def drawFigNone():
    figNone = go.Figure().add_annotation(x=2, y=2,text="No Data to Display",font=dict(family="sans serif",size=25,color="crimson"),showarrow=False,yshift=10)
    return figNone

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
    figs = make_subplots(
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
            figs.add_trace(trace, row=1, col=1)
    else:
        for trace in figNone.data:
            figs.add_trace(trace, row=1, col=1)
    if Nodata2 == 0:
        figg = ff.create_gantt(df3, colors=colors, index_col='Events', reverse_colors=True, show_colorbar=True)
        for trace in figg.data:
            figs.add_trace(trace, row=3, col=1)
    else:
        for trace in figNone.data:
            figs.add_trace(trace, row=1, col=1)
    figs.update_layout(font = {"size": 30})
    figs.update_yaxes(range=[-0.5, 0.5], row=1, col=1)
    figs.update_yaxes(visible=False, showticklabels=False,row=3, col=1)
    return figs

def drawFigs2(Nodata1,Nodata2,df2,df,figNone):
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
        figg = ff.create_gantt(df, colors=colors, index_col='Events', reverse_colors=True, show_colorbar=True)
        for trace in figg.data:
            figs2.add_trace(trace, row=3, col=1)
    else:
        for trace in figNone.data:
            figs2.add_trace(trace, row=1, col=1)
    figs2.update_layout(font = {"size": 30})
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
        font={"size": 30},
        polar={
            "angularaxis": {"showline": False, "tickcolor": "white", "rotation": 90, "direction": "clockwise",
                        "tickmode": "array", "tickvals": [0, 45, 90, 135, 180, 225, 270, 315],
                        "ticktext": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]}
             },
        showlegend=False,
    )
    fig3.update_polars(radialaxis_showticklabels=False)
    return fig3

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df2 = loadDf2(treeID,slopeID)
df = loadDf(treeID,slopeID)
df4 = loadDf4(df2)
df3 = loadDf3(df)
figNone = drawFigNone()
Nodata1 = 0
if df4.empty:
    Nodata1 = 1
Nodata2 = 0
if df3.empty:
    Nodata2 = 1
figs = drawFigs1(Nodata1,Nodata2,df4,df3,figNone)
Nodata1 = 0
if df2.empty:
    Nodata1 = 1
Nodata2 = 0
if df.empty:
    Nodata2 = 1
figs2 = drawFigs2(Nodata1,Nodata2,df2,df,figNone)
fig3 = drawFigure3(df2)
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
            figure=figs
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
])
@app.callback(Output('graph1', 'figure'),
              Input('interval-component1', 'n_intervals'))
def update_graph1_live(n):
    df2 = loadDf2(treeID,slopeID)
    df = loadDf(treeID,slopeID)
    df4 = loadDf4(df2)
    df3 = loadDf3(df)
    figNone = drawFigNone()
    Nodata1 = 0
    if df4.empty:
        Nodata1 = 1
    Nodata2 = 0
    if df3.empty:
        Nodata2 = 1
    figs = drawFigs1(Nodata1, Nodata2, df4, df3, figNone)
    print(treeID)
    print(slopeID)
    return figs

@app.callback(Output('graph2', 'figure'),
              Input('interval-component2', 'n_intervals'))
def update_graph2_live(n):
    df2 = loadDf2(treeID,slopeID)
    df = loadDf(treeID,slopeID)
    figs2 = drawFigs2(Nodata1,Nodata2,df2,df,figNone)
    return figs2

@app.callback(Output('graph3', 'figure'),
              Input('interval-component3', 'n_intervals'))
def update_graph3_live(n):
    df2 = loadDf2(treeID,slopeID)
    fig3 = drawFigure3(df2)
    return fig3

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