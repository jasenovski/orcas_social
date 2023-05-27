
def gerar_ranking_usuarios(tipo_ranking, selecionado, group_mes, group_semana):


    if tipo_ranking == "Mensal":
        df_ranking = group_mes.get_group(selecionado)
    else:
        df_ranking = group_semana.get_group(selecionado)

    df_ranking = df_ranking[df_ranking["nm_user"] != "Bova"]
    df_ranking = df_ranking[["nm_user", "retorno_carteira"]].sort_values(by="retorno_carteira", ascending=False).reset_index(drop=True)
    df_ranking["retorno_carteira"] = df_ranking["retorno_carteira"].apply(lambda x: f"{100 * x:.2f}%")
    df_ranking["Posicao"] = list(map(lambda x: f"{x}º", range(1, len(df_ranking) + 1)))

    return df_ranking.rename(columns={"nm_user": "Usuário", "retorno_carteira": "Retorno"})