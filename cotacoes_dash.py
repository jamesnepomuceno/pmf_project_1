import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import yfinance as yf
from datetime import datetime

# Lista ações
acoes = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA']

def get_cotacoes():
    dados = []
    for acao in acoes:
        ticker = yf.Ticker(acao)
        info = ticker.history(period='2d')
        if len(info) >= 2:
            atual = info.iloc[-1]
            anterior = info.iloc[-2]
            dados.append({
                'Ação': acao.replace('.SA', ''),
                'Preço Atual': round(atual['Close'], 2),
                'Variação %': round((atual['Close'] / anterior['Close'] - 1)*100, 2),
                'Volume': int(atual['Volume'])
            })
    return pd.DataFrame(dados)

# App Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('📈 Cotações 5 Ações - Dash Plotly', style={'textAlign': 'center'}),
    
    html.H3('Atualização:', id='atualizacao', style={'textAlign': 'center'}),
    
    dcc.Interval(id='intervalo', interval=3*60*1000, n_intervals=0),  # 3 min
    
    html.H3('Tabela'),
    html.Div(id='tabela'),
    
    html.H3('Gráfico Variação'),
    dcc.Graph(id='grafico')
])

@app.callback(
    [Output('tabela', 'children'), Output('grafico', 'figure'), Output('atualizacao', 'children')],
    [Input('intervalo', 'n_intervals')]
)
def update_data(n):
    df = get_cotacoes()
    hora = datetime.now().strftime('%d/%m %H:%M')
    
    # Tabela
    tabela = dash.dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in df.columns],
        style_cell={'textAlign': 'center'},
        style_data_conditional=[
            {'if': {'filter_query': '{Variação %} > 0'}, 'color': 'green'},
            {'if': {'filter_query': '{Variação %} < 0'}, 'color': 'red'}
        ]
    )
    
    # Gráfico barras
    fig = px.bar(df, x='Ação', y='Variação %', color='Variação %',
                 color_continuous_scale='RdYlGn', title='Variação Diária %')
    
    return tabela, fig, f'{hora} (auto-update 3min)'

if __name__ == '__main__':
    app.run(debug=True, port=8050)