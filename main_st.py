from pages.main_page import selecionar_pagina
from pages.desempenhos import desempenhos
from pages.ranking_usuarios import ranking_usuarios
from pages.simulacoes import simulacoes

from models.remove_footer_hamburger import remove_footer_hamburger

pages = {"Desempenhos": desempenhos,
         "Ranking de usuários": ranking_usuarios,
         "Simulações": simulacoes}

def main():
    pagina, selection = selecionar_pagina(pages)
    remove_footer_hamburger()

    if pagina == "Desempenhos":
        pages[pagina](nm_users=selection)
    elif pagina == "Ranking de usuários":
        pages[pagina](nm_users=selection)
    elif pagina == "Simulações":
        pages[pagina](country=selection)

if __name__ == "__main__":
    main()