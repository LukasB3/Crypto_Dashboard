import dash
import plotly.express as px
from dash import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Output, Input

# importieren der anderen *.py
from crypto_API import historical_df, avg_df, crypto_data_df

# Hauptprogramm mit Dashboard

# 6.APP-Layout

app = dash.Dash(__name__)

docker = True
server = app.server

app.layout = html.Div([
    html.H1('Crypto-Informationen für das Jahr 2023', style={'textAlign': 'center'}),
    dcc.Dropdown(id='Währung', placeholder='Bitte Crypto auswählen',
                 options=[{'label': x, 'value': x}
                          for x in sorted(historical_df.Währung.unique())],
                 style={'width': '40%'}
                 ),
    dash_table.DataTable(
        id='Table-Daten',
        columns=[
            {'name': 'Rang', 'id': 'market_cap_rank'},
            {'name': 'Aktueller Preis ($)', 'id': 'current_price'},
            {'name': 'Preis Änderung 24h (%)', 'id': 'price_change_percentage_24h'},
            {'name': '24h High ($)', 'id': 'high_24h'},
            {'name': '24h Low ($)', 'id': 'low_24h'},
            {'name': 'Market-Cap ($)', 'id': 'market_cap'},
            {'name': 'All Time High ($)', 'id': 'ath'},
            {'name': 'All Time High Veränderung (%)', 'id': 'ath_change_percentage'},
            {'name': 'All Time High Datum', 'id': 'ath_date', 'type': 'datetime'}

        ],


    ),
    dash_table.DataTable(
        id='Table-Average',
        columns=[
            {'name': 'Preis ø pro Tag', 'id': 'USD'},
            {'name': 'Gehandelte Coins ø pro Tag', 'id': 'Volume'},
            {'name': 'Trades ø pro Tag', 'id': 'Anzahl'}

        ],
        style_table={'width': '38%'},


    ),
    html.Div(children=[
        dcc.Graph(id='Preis-Graph',
                  figure={},
                  style={'width': '50%', 'display': 'inline-block'}
                  ),
        dcc.Graph(id='Trend-Graph',
                  figure={},
                  style={'width': '50%', 'display': 'inline-block'}
                  )
    ]),

    html.Div(children=[
        dcc.Graph(id='Volume-Graph',
                  figure={},
                  style={'width': '50%', 'display': 'inline-block'}
                  ),
        dcc.Graph(id='Anzahl-Graph',
                  figure={},
                  style={'width': '50%', 'display': 'inline-block'}
                  )
    ]),

])


@app.callback(
    Output(component_id='Table-Daten', component_property='data'),
    Output(component_id='Table-Average', component_property='data'),
    Output(component_id='Preis-Graph', component_property='figure'),
    Output(component_id='Trend-Graph', component_property='figure'),
    Output(component_id='Volume-Graph', component_property='figure'),
    Output(component_id='Anzahl-Graph', component_property='figure'),
    Input(component_id='Währung', component_property='value')
)
def generate(Währung):
    df1 = crypto_data_df[crypto_data_df.Währung == Währung]
    df2 = historical_df[historical_df.Währung == Währung]
    df3 = avg_df[avg_df.Währung == Währung]
    fig = px.line(data_frame=df2, x='Datum', y='USD', title='Preis in USD', color_discrete_sequence=['black'])
    fig1 = px.bar(data_frame=df2, x='Datum', y='Volume', title='Anzahl gehandelter Coins')
    fig2 = px.bar(data_frame=df2, x='Datum', y='Anzahl', title='Anzahl Trades')
    fig3 = px.scatter(df2, x='Datum', y='USD', title='Trend', trendline="ols", color_discrete_sequence=['black'],
                      trendline_color_override="blue")
    

    return df1.to_dict('records'), df3.to_dict('records'), fig, fig3, fig1, fig2


# Initiierung über Docker
if __name__ == "__main__":
    if docker:
        app.run_server(debug=True, host="0.0.0.0", port=8080, use_reloader=False)
    else:
        app.run_server(host='0.0.0.0', debug=True)