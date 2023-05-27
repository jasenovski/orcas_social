import streamlit as st
import pandas as pd
from models.gerar_ranking import gerar_ranking_usuarios
from models.gerar_df_carteira import gerar_df_carteira_usuario
from models.gerar_acumulados import gerar_acumulados_usuarios
from models.carregar_pickles import users_pushes, orcas_pushes, data_dominios, df_prices, ranking_users, df_tickers_br, users_wallets

def ranking_usuarios(nm_users):

    acumulados_usuarios = gerar_acumulados_usuarios(users_wallets, nm_users)

    st.text("")
    st.subheader("Ranking de usuários")
    group_semana = ranking_users.groupby(["week"])
    group_mes = ranking_users.groupby(["month"])
    semanas = group_semana.groups.keys()
    meses = group_mes.groups.keys()
    columns = st.columns(2)
    tipo_ranking = columns[0].selectbox(label="Selecione o tipo de ranking", options=["Semanal", "Mensal"], index=1)
    selecionado = columns[1].selectbox(label="Selecione o mes:" if tipo_ranking == "Mensal" else "Selecione a semana:", 
                        options=meses if tipo_ranking == "Mensal" else semanas, 
                        index=len(meses) - 1 if tipo_ranking == "Mensal" else len(semanas) - 1)

    df_ranking = gerar_ranking_usuarios(tipo_ranking, selecionado, group_mes, group_semana)
    st.table(df_ranking[["Posicao", "Usuário", "Retorno"]])

    st.text("")
    st.subheader("Selecione um usuário para conferir a carteira atual")
    options = nm_users
    options.remove("Bova")
    nm_user = st.selectbox(
        label="",
        options=options,
        index=0
    )

    df_mostrar = gerar_df_carteira_usuario(nm_user, users_pushes, orcas_pushes, data_dominios, df_prices, df_tickers_br)
    st.dataframe(df_mostrar[["Ação", "Nome", "Data Compra", "Preco Compra", "Preco Atual", "Var %"]])

    last_variation_user = acumulados_usuarios[acumulados_usuarios["Usuário"] == nm_user]["retorno_carteira"].iloc[-1]
    last_date_user = pd.to_datetime(acumulados_usuarios[acumulados_usuarios["Usuário"] == nm_user]["Data"].iloc[-1]).strftime("%d/%m/%Y")
    first_date_user = pd.to_datetime(acumulados_usuarios[acumulados_usuarios["Usuário"] == nm_user]["Data"].iloc[1]).strftime("%d/%m/%Y")

    qtd_pushes_orcas = len(orcas_pushes[orcas_pushes["data_venda"].isnull()])
    st.info(f"O usuário {nm_user} possui uma carteira com {len(df_mostrar)}/{qtd_pushes_orcas} ({100 * len(df_mostrar)/qtd_pushes_orcas:.2f}%) pushes Orcas, com data de início em {first_date_user} até {last_date_user}.")
    if last_variation_user < 0:
        st.error(f"Na última cotação registrada ({last_date_user}), o usuário {nm_user} obteve um retorno negativo de {100 * last_variation_user:.2f}%")
    else:
        st.success(f"Na última cotação registrada ({last_date_user}), o usuário {nm_user} obteve um retorno positivo de {100 * last_variation_user:.2f}%")