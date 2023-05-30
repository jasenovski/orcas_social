import pandas as pd

def gerar_df_prices_filtrado(country, df_prices, nm_acoes, data_inicial, data_final):

    if country == "br":
        bova = pd.read_pickle("pickles/prices_bova.pkl")
        df_prices = pd.concat([df_prices, bova], axis=0)
        df_prices = df_prices.sort_values(by=["nm_acao", "Date"]).reset_index(drop=True)
        nm_acoes.append("bova11")
    elif country == "us":
        sp500 = pd.read_pickle("pickles/prices_sp500.pkl")
        df_prices = pd.concat([df_prices, sp500], axis=0)
        df_prices = df_prices.sort_values(by=["nm_acao", "Date"]).reset_index(drop=True)
        nm_acoes.append("sp500")
    
    df_prices_filtrado = df_prices[(df_prices["nm_acao"].isin(nm_acoes)) & (df_prices["Date"] >= data_inicial) & (df_prices["Date"] <= data_final)]
    # df_prices_filtrado = df_prices_filtrado.sort_values(by=["nm_acao", "Date"]).reset_index(drop=True)

    pd.options.mode.chained_assignment = None

    # get pct_change for each stock and add to new column
    # df_prices_filtrado['pct_change'] = df_prices_filtrado.groupby('nm_acao')['Close'].pct_change()

    acumulados = []
    for nm_acao, group in df_prices_filtrado.groupby("nm_acao"):
        acumulado = list((1 + group["pct_change"]).cumprod().fillna(1).values)
        acumulados.extend(acumulado)

    df_prices_filtrado["Retorno Acumulado"] = acumulados

    return df_prices_filtrado