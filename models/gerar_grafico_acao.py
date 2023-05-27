import pandas as pd
from models.carregar_pickles import df_prices

def gerar_df_prices_filtrado(nm_acoes, data_inicial, data_final):
    df_prices_filtrado = df_prices[(df_prices["nm_acao"].isin(nm_acoes)) & (df_prices["Date"] >= data_inicial) & (df_prices["Date"] <= data_final)]
    df_prices_filtrado = df_prices_filtrado.sort_values(by=["nm_acao", "Date"]).reset_index(drop=True)

    pd.options.mode.chained_assignment = None

    # get pct_change for each stock and add to new column
    df_prices_filtrado['pct_change'] = df_prices_filtrado.groupby('nm_acao')['Close'].pct_change()

    acumulados = []
    for nm_acao, group in df_prices_filtrado.groupby("nm_acao"):
        acumulado = list((1 + group["pct_change"]).cumprod().values)
        acumulados.extend(acumulado)

    df_prices_filtrado["Retorno Acumulado"] = acumulados

    return df_prices_filtrado