
import pandas as pd
import os

def gerar_df_carteira_usuario(nm_user, users_pushes, orcas_pushes, data_dominios, df_prices, df_tickers_br):
    if nm_user != "Orcas":
        df_mostrar = users_pushes[(users_pushes["nm_user"] == nm_user) & (users_pushes["dt_saida"].isnull())]# [["nm_acao", "dt_entrada", "preco_entrada"]].reset_index(drop=True)
    else:
        df_mostrar = pd.merge(orcas_pushes, data_dominios, left_on='id_acao', right_on='id', how='left')# [["nm_acao", "data_compra", "preco_compra"]]
        # df_mostrar["preco_compra"] = df_mostrar["preco_compra"].map(lambda preco: f"{preco:.2f}")
        df_mostrar = df_mostrar.rename(columns={"data_compra": "dt_entrada", "preco_compra": "preco_entrada"})
    
    df_mostrar["dt_entrada"] = df_mostrar["dt_entrada"].map(lambda data: pd.to_datetime(data).strftime("%d/%m/%Y"))    
    df_mostrar["preco_entrada"] = df_mostrar["preco_entrada"].map(lambda preco: f"{float(preco):.2f}")

    df_mostrar = pd.merge(df_mostrar, df_tickers_br, left_on='nm_acao', right_on='Code', how='left')# [["nm_acao", "Name", "dt_entrada", "preco_entrada"]]
    # df_mostrar = df_mostrar.rename(columns={"dt_entrada": "Data Compra", "nm_acao": "Ação", "Name": "Nome", "preco_entrada": "Preco Compra"})

    precos_atuais = []
    variacoes_hoje = []
    for i, linha in df_mostrar.iterrows():
        nm_acao = linha["nm_acao"]
        preco_atual = df_prices[df_prices["nm_acao"] == nm_acao]["Close"].iloc[-1]
        variacao_hoje = df_prices[df_prices["nm_acao"] == nm_acao]["pct_change"].iloc[-1]
        precos_atuais.append(f"{preco_atual:.2f}")
        variacoes_hoje.append(f"{100 * variacao_hoje:.2f}%")

    df_mostrar["Preco Atual"] = precos_atuais
    df_mostrar["Var %"] = variacoes_hoje

    return df_mostrar.rename(columns={"dt_entrada": "Data Compra", "nm_acao": "Ação", "Name": "Nome", "preco_entrada": "Preco Compra"})