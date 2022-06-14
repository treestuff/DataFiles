from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import datetime
import numpy as np

slopeID = 0
sensorID = 0

df = pd.read_csv('pivotFlexBarrier.csv')
a,b,c,d,e = df.iloc[0], df.iloc[1], df.iloc[2], df.iloc[3], df.iloc[4]
df2 = df
df2.iloc[0] = d
df2.iloc[1] = a
df2.iloc[2] = c
df2.iloc[3] = e
df2.iloc[4] = b
SensorIDs = df['deviceID'].tolist()
for i in range(0, len(SensorIDs)):
    SensorIDs[i] = int(SensorIDs[i])
SensorIDs = [str(i) for i in SensorIDs]
df = df.drop('Unnamed: 0', 1)
df = df.drop('deviceID', 1)
z = df.to_numpy()

dates = list(df)
for i, date in enumerate(dates):
    dates[i] = datetime.date.fromisoformat(date)
dates = np.array(dates)

def reloadData():
    df = pd.read_csv('pivotFlexBarrier.csv')
    a, b, c, d, e = df.iloc[0], df.iloc[1], df.iloc[2], df.iloc[3], df.iloc[4]
    df2 = df
    df2.iloc[0] = d
    df2.iloc[1] = a
    df2.iloc[2] = c
    df2.iloc[3] = e
    df2.iloc[4] = b
    SensorIDs = df['deviceID'].tolist()
    for i in range(0, len(SensorIDs)):
        SensorIDs[i] = int(SensorIDs[i])
    SensorIDs = [str(i) for i in SensorIDs]
    df = df.drop('Unnamed: 0', 1)
    df = df.drop('deviceID', 1)
    z = df.to_numpy()

    dates = list(df)
    for i, date in enumerate(dates):
        dates[i] = datetime.date.fromisoformat(date)
    dates = np.array(dates)
    return SensorIDs, dates, z

# base = datetime.datetime.today()
# dates = base - np.arange(90) * datetime.timedelta(days=1)
# for i in range(0, len(dates)):
#      dates[i] = dates[i].date()
#
# dfWork = pd.DataFrame([
#     dict(Task="Job A", Start=dates[len(dates)-2], Finish=dates[len(dates)-1],Description='JobA'),
#     dict(Task="Job B", Start=dates[len(dates)-10], Finish=dates[len(dates)-8],Description='JobB'),
#     dict(Task="Job C", Start=dates[0], Finish=dates[1],Description='JobC')
# ])
dfWork = pd.read_csv('Task_Info_Flex.csv')
for i in range(0, len(dfWork)):
    dfWork['Start'][i] = datetime.datetime.strptime(dfWork['Start'][i], '%d/%m/%Y').date()
for i in range(0, len(dfWork)):
    dfWork['Finish'][i] = datetime.datetime.strptime(dfWork['Finish'][i], '%d/%m/%Y').date()
dfWork['SlopeID'] = dfWork['SlopeID'].fillna(slopeID)
dfWork['SensorID'] = dfWork['SensorID'].fillna(sensorID)
dfWork = dfWork.loc[(dfWork['SlopeID'] == slopeID) | (dfWork['SlopeID'] == 'ALL'), :]
dfWork = dfWork.loc[(dfWork['SensorID'] == sensorID) | (dfWork['SensorID'] == 'ALL'), :]
def reloadWork(slopeID, sensorID):
    dfWork = pd.read_csv('Task_Info_Flex.csv')
    for i in range(0, len(dfWork)):
        dfWork['Start'][i] = datetime.datetime.strptime(dfWork['Start'][i], '%d/%m/%Y').date()
    for i in range(0, len(dfWork)):
        dfWork['Finish'][i] = datetime.datetime.strptime(dfWork['Finish'][i], '%d/%m/%Y').date()
    dfWork['SlopeID'] = dfWork['SlopeID'].fillna(slopeID)
    dfWork['SensorID'] = dfWork['SensorID'].fillna(sensorID)
    dfWork = dfWork.loc[(dfWork['SlopeID'] == slopeID) | (dfWork['SlopeID'] == 'ALL'), :]
    dfWork = dfWork.loc[(dfWork['SensorID'] == sensorID) | (dfWork['SensorID'] == 'ALL'), :]
    return dfWork
# Color = ['rgb(0, 0, 0)','rgb(0, 0, 0)','rgb(0, 0, 0)']
# Jobs = ['JobA','JobB','JobC']
app = Dash(__name__)

app.layout = html.Div([
        html.H4('TCK928 - Monitoring Slope No.: 11SE-D/ND9', style={'font-size': '40px', 'textAlign': 'center'}),
        dcc.Graph(id="graph", responsive=True),
        dcc.Interval(id="trigger", interval=1000),
        html.H4('Location of the Slope', style={'font-size': '40px', 'textAlign': 'center'}),
        html.Div(html.Img(src=app.get_asset_url('slope.jpg')),style={'width': '70%',  'textAlign': 'center', 'display': 'inline-block'}),
        html.Div([
            html.P("Sensor A SN: 890771058921"),
            html.P("Sensor B SN: 890771058913"),
            html.P("Sensor C SN: 890771058918"),
            html.P("Sensor D SN: 890771059000"),
            html.P("Sensor E SN: 890771058915"),
        ],style={'width': '30%', 'display': 'inline-block'})
])

# html.Img(src=app.get_asset_url('slope.jpg'))
@app.callback(Output("graph", "figure"), Input('trigger', 'interval'))
def filter_heatmap(cols):
    import plotly.graph_objects as go
    import numpy as np
    import plotly.figure_factory as ff
    from plotly.subplots import make_subplots
    import pandas as pd
    # df = pd.read_csv('pivotFlexBarrier.csv')
    # SensorIDs = df['deviceID'].tolist()
    # df = df.drop('Unnamed: 0', 1)
    # df = df.drop('deviceID', 1)
    # z = df.to_numpy()
    slopeID = 0
    sensorID = 0
    SensorIDs, dates, z = reloadData()
    dfWork = reloadWork(slopeID, sensorID)
    labels = SensorIDs
    hovertext = list()
    for yi, yy in enumerate(labels):
        hovertext.append(list())
        for xi, xx in enumerate(dates):
            hovertext[-1].append('Date: {}<br />Sensor ID: {}<br />Maximum Reading: {}'.format(xx, yy, z[yi][xi]))
    hovertextWork = list()
    for i in range(0, len(dfWork)):
        hovertextWork.append(list())
        hovertextWork[-1].append('Date: {}<br />Event: {}<br />'.format(dfWork['Start'][i], dfWork['Description'][i]))
    # for i in range(0, len(z)):
    #     if i == 0 or i == 13 or i == 29:
    #         labels.append('Post -' + str(i))
    #     else:
    #         labels.append('Barrier -' + str(i))
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,specs=[
        [{'rowspan':2}], [None],
        [{}],
    ])
    fig.add_trace(go.Heatmap(
        colorbar={"title": 'Unit of Measure: g'},
        z=z,
        x=dates,
        y=labels,
        colorscale='Viridis', colorbar_y=0.7,colorbar_len=0.6, hoverinfo='text', text=hovertext))
    figg = ff.create_gantt(dfWork, group_tasks=True, index_col='Description', reverse_colors=False, show_colorbar=False)
    figg.update_traces(hovertemplate="Date:%{x}<br>Event:%{y}")
    for trace in figg.data:
        fig.add_trace(trace, row=3, col=1)
    fig.update_layout(title={"text": "Motion Over Time and Works scheduled", "xanchor": "center", "x": 0.53},
                           yaxis={"title": "Barrier Posts", "autorange": "reversed"},
                           width=1800,
                           height=1000,
                           xaxis={"title": 'Time', "tickangle": 45})
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, autosize=False)
    fig.update_yaxes(showticklabels=False, row=3, col=1, tickson='boundaries')
    fig.update_xaxes(tickson='boundaries')
    fig['layout'].update(margin=dict(l=0, r=0, b=0, t=0))
    fig['layout']['yaxis2']['title'] = 'Weather & Work Records'
    fig.update_xaxes(dtick=86400000.0)
    fig.update_layout(font={"size": 13})
    return fig

app.run_server(debug=True)

