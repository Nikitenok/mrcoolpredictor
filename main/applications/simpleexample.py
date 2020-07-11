import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash

import datetime
from .model import Arima
from dateutil.relativedelta import relativedelta

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('SimpleExample', external_stylesheets=external_stylesheets)


m = Arima()

data = m.get_preds()

if len(data) != 0:

    syms = list(data.keys())

    date_list = [datetime.datetime(2010, 1, 1)
                 + relativedelta(months=i) for i in range(1, 12 * 11)]
    print("11")
    app.layout = html.Div([
        html.H2(id='output-symbol'),
        dcc.RadioItems(
            id='dropdown-symbol',
            options=[{'label': c, 'value': c} for c in syms],
            value=syms[0]
        ),
        dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
        dcc.Slider(
            id='slider-updatemode',
            marks={i: '{}'.format(i) for i in range(len(date_list))},
            max=len(date_list),
            value = len(date_list)-1,
            step=1,
            updatemode='drag',
        ),
    ])
    @app.callback(
        Output('output-symbol', 'children'),
        [Input('dropdown-symbol', 'value')])
    def callback_color(dropdown_symbol):
        return "Stock Price History | %s" % dropdown_symbol

    @app.callback(
                   Output('slider-graph', 'figure'),
                  [Input('slider-updatemode', 'value'),
                   Input('dropdown-symbol', 'value')])
    def display_value(value, symbol):

        x = []
        y = []
        y_f = []
        for i in range(value):
            x.append(data[symbol].iloc[i].date)
        for i in range(value):
            y.append(float(data[symbol].iloc[i].close))
            y_f.append(float(data[symbol].iloc[i].forecast))

        graph = go.Scatter(
            x=x,
            y=y,
            name='history'
        )
        graph_f = go.Scatter(
            x=x,
            y=y_f,
            name='forecast'
        )
        layout = go.Layout(
            paper_bgcolor='#27293d',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(range=[min(x), max(x)]),
            yaxis=dict(range=[min(y), max(y)+max(y)/2]),
            font=dict(color='white'),

        )
        return {'data': [graph, graph_f], 'layout': layout}
else:
    print("22")
    app.layout = html.Div([])