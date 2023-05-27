import streamlit as st

def gerar_metrics(new_df, nm_users):
    deltas = {}
    for nm_user in nm_users:
        retorno_user = new_df[new_df["Usuário"] == nm_user].reset_index(drop=True)["Retorno Acumulado"].iloc[-1]
#         if "Bova" in users_wallets["nm_user"].drop_duplicates().values:
        retorno_bova = new_df[new_df["Usuário"] == "Bova"].reset_index(drop=True)["Retorno Acumulado"].iloc[-1]
        delta = f"{100 * ((retorno_user - 1) / (retorno_bova - 1)):.2f}%"
        deltas[nm_user] = {"delta": delta, 
                           "retorno_user": f"{(100 * (retorno_user - 1)):.2f}%"}
    
    return deltas