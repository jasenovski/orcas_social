import pandas as pd
import os

users_pushes = pd.read_pickle(os.path.join("pickles", "users_pushes.pkl"))

users_wallets = pd.read_pickle(os.path.join("pickles", "tb_user_wallets.pkl"))
users_wallets["dt_referencia"] = pd.to_datetime(users_wallets["dt_referencia"])

orcas_pushes = pd.read_pickle(os.path.join("pickles", "orcas_pushes.pkl"))[["id_acao", "data_compra", "data_venda", "preco_compra"]]

data_dominios = pd.read_pickle(os.path.join("pickles", "data_dominios_acoes.pkl"))

ranking_users = pd.read_pickle(os.path.join("pickles", "ranking_usuarios.pkl"))

df_tickers_br = pd.read_pickle(os.path.join("pickles", "df_tickers_br.pkl"))