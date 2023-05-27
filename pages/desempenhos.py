import streamlit as st
import plotly.express as px
from models.gerar_acumulados import gerar_acumulados_usuarios
from models.gerar_metrics import gerar_metrics
from models.carregar_pickles import users_wallets

def desempenhos(nm_users):
    st.subheader("Desempenhos das carteiras Orcas em comparação com o Ibovespa")

    acumulados_usuarios = gerar_acumulados_usuarios(users_wallets, nm_users)
    fig = px.line(acumulados_usuarios, x='Data', y='Retorno Acumulado', color="Usuário")
    st.plotly_chart(fig)

    deltas = gerar_metrics(acumulados_usuarios, nm_users)
    colunas = st.columns(len(nm_users))
    for coluna, nm_user in zip(colunas, deltas):
        delta = deltas[nm_user]["delta"]
        retorno_user = deltas[nm_user]["retorno_user"]
        coluna.metric(label=f"Retorno acumulado {nm_user}", value=retorno_user, delta=delta)