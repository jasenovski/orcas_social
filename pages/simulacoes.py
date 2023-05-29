import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

from models.carregar_pickles import df_prices
from models.gerar_grafico_acao import gerar_df_prices_filtrado

def simulacoes():
    st.subheader("Selecione a quantia de investimento para simulação")
    valor_investimento = st.slider(label="", min_value=1000, max_value=100000, value=10000, step=500)

    st.text("")

    options = sorted(df_prices["nm_acao"].drop_duplicates().to_list())
    options.remove("bova11")
    st.text("")
    st.subheader("Selecione as ações para a simulação")
    nm_acoes = st.multiselect(label="",
                        options=options)
    
    nm_acoes.append("bova11")

    colunas = st.columns(2)
    data_inicial = pd.to_datetime(colunas[0].date_input(label="Data inicial", value=datetime.date(2023, 1, 1)))
    data_final = pd.to_datetime(colunas[1].date_input(label="Data final", value=datetime.date.today()))

    if data_inicial > data_final:
        st.error("Data inicial não pode ser maior que a data final")
        return

    df_prices_filtrado = gerar_df_prices_filtrado(nm_acoes, data_inicial, data_final)

    fig = px.line(df_prices_filtrado, x='Date', y='Retorno Acumulado', color="nm_acao")
    st.plotly_chart(fig)

    for nm_acao in nm_acoes:
        retorno_acumulado = df_prices_filtrado[df_prices_filtrado["nm_acao"] == nm_acao]["Retorno Acumulado"].iloc[-1]
        retorno_final = retorno_acumulado - 1

        data_compra = df_prices_filtrado[df_prices_filtrado["nm_acao"] == nm_acao]["Date"].iloc[0]
        data_venda = df_prices_filtrado[df_prices_filtrado["nm_acao"] == nm_acao]["Date"].iloc[-1]

        duracao = (data_venda - data_compra).days
        retorno_anual = ((retorno_acumulado) ** (1 / (duracao / 365))) - 1

        valor_referencia = float(valor_investimento)
        texto = f"Se você tivesse investido R\$ {valor_referencia:,.2f} em {data_compra.strftime('%d/%m/%Y')} na ação {nm_acao}," \
                f" hoje ({data_venda.strftime('%d/%m/%Y')}) você teria um retorno de {100 * retorno_final:.2f}% ({100 * retorno_anual:.2f}% aa.) " \
                f" Resultando no valor final de R$ {valor_referencia * retorno_acumulado:,.2f}"
        
        if retorno_acumulado > 1:
            st.success(texto)
        else:
            st.error(texto)
