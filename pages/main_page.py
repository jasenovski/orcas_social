import streamlit as st
import os
from PIL import Image
from models.carregar_pickles import users_wallets

def selecionar_pagina(pages, image_filename="logo_orcas_2.jpeg"):
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.image(image=Image.open(os.path.join("images", image_filename)), width=100)
    col2.title("Orcas")

    pagina = st.sidebar.selectbox(
        label="Selecione a página",
        options=pages.keys(),
        index=0
    )

    users = users_wallets["nm_user"].drop_duplicates().to_list()
    users.remove("Bova")
    users.remove("Orcas")

    nm_users = None
    if pagina in ["Desempenhos", "Ranking de usuários"]:
        nm_users = st.sidebar.multiselect(label="Selecione os usuários", options=users)
    
    return pagina, nm_users