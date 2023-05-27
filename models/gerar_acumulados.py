import pandas as pd

def gerar_acumulados_usuarios(users_wallets, nm_users):

    nm_users.append("Bova")
    nm_users.append("Orcas")

    df = users_wallets[users_wallets["nm_user"].isin(nm_users)]

    data_filtro = min(df["dt_referencia"])
    grouped = df.groupby(["telegram_id", "nm_user"])
    for (telegram_id, nm_user), group in grouped:
        data_inicial = group["dt_referencia"].iloc[0]
        if data_inicial > data_filtro:
            data_filtro = data_inicial


    new_df = []
    for nm_user in nm_users:

        df_test = df[(df["dt_referencia"] >= data_filtro) & (df["nm_user"] == nm_user)].reset_index(drop=True)

        # set to 0 the first row of df_test in the column "retorno_carteira"
        df_test.loc[0, "retorno_carteira"] = 0

        df_test["retorno_acumulado"] = (1 + df_test["retorno_carteira"]).cumprod()    
        new_df.extend(df_test.to_dict("records"))

    new_df = pd.DataFrame(new_df)
    new_df = new_df.rename(columns={"dt_referencia": "Data", "retorno_acumulado": "Retorno Acumulado", "nm_user": "Usuário"})
    return new_df