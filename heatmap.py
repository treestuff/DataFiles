from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import datetime
import numpy as np

df = pd.read_csv('pivotFlexBarrier.csv')
SensorIDs = df['deviceID'].tolist()
SensorIDs = [str(i) for i in SensorIDs]
df = df.drop('Unnamed: 0', 1)
df = df.drop('deviceID', 1)
z = df.to_numpy()

dates = list(df)
for i, date in enumerate(dates):
    dates[i] = datetime.date.fromisoformat(date)
dates = np.array(dates)

# base = datetime.datetime.today()
# dates = base - np.arange(90) * datetime.timedelta(days=1)
# for i in range(0, len(dates)):
#      dates[i] = dates[i].date()

dfWork = pd.DataFrame([
    dict(Task="Job A", Start=dates[len(dates)-2], Finish=dates[len(dates)-1],Description='JobA'),
    dict(Task="Job B", Start=dates[len(dates)-10], Finish=dates[len(dates)-8],Description='JobB'),
    dict(Task="Job C", Start=dates[0], Finish=dates[1],Description='JobC')
])
Color = ['rgb(0, 0, 0)','rgb(0, 0, 0)','rgb(0, 0, 0)']
Jobs = ['JobA','JobB','JobC']
app = Dash(__name__)

app.layout = html.Div([
    html.H4('TCK928 - Monitoring Slope No.: 11SE-D/ND9', style={'font-size': '40px', 'textAlign': 'center'}),
    dcc.Graph(id="graph", responsive=True),
    dcc.Interval(id="trigger", interval=1000),  # trigger to invoke data refresh attempt, defaults to once per second
])

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
    labels = SensorIDs
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
        colorscale='Viridis', colorbar_y=0.7,colorbar_len=0.6))
    figg = ff.create_gantt(dfWork, colors=Color, group_tasks=True, index_col='Task', reverse_colors=False, show_colorbar=False)
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
    return fig

app.run_server(debug=True)

