import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# Lista de 5 ações BR
acoes = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA']

@st.cache_data(ttl=300)  # Atualiza a cada 5 min
def get_cotacoes():
    dados = []
    for acao in acoes:
        ticker = yf.Ticker(acao)
        info = ticker.history(period='1d')
        if not info.empty:
            atual = info.iloc[-1]
            dados.append({
                'Ação': acao.replace('.SA', ''),
                'Preço Atual (R$)': f"R$ {atual['Close']:,.2f}",
                'Variação %': f"{(atual['Close'] / atual['Open'] * 100 - 100):+.2f}%",
                'Volume': f"{int(atual['Volume']):,}",
                'Hora': datetime.now().strftime('%H:%M')
            })
    return pd.DataFrame(dados)

st.title('📈 Cotações das 5 Ações - MVP')

if __name__ == "__main__":
    df = get_cotacoes()
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.caption('Atualizado a cada 5 min | Dados via yfinance')
