import flet as ft
from flet_route import Routing, path
from views.menus import menu
from views.cadastro_cliente2 import cadastrar_cliente
from views.cadastro_produto import cadastro_produto
from views.saida_os import entrega_aparelho
from views.entrada_os import devolver
from views.lista_cliente import lista_cliente
from views.tabela_produtos import produtos_estoque
from views.lista_os import lista_os
from views.os_finalizada import os_finalizada

def rotas(page: ft.Page):
    app_routes = [
        path(url='/', clear=True, view=menu),
        path(url="/cadastro_cliente/cadastrar_cliente", clear=True, view=cadastrar_cliente),
        path(url="/cadastro_produto/produto", clear=True, view=cadastro_produto),
        path(url='/entrega_os/entrega', clear=True, view=entrega_aparelho),
        path(url="/devolucao_os/devolver", clear=True, view=devolver),
        path(url="/lista_cliente/lista", clear=True, view=lista_cliente),
        path(url="/produtos_estoque/produtos", clear=True, view=produtos_estoque),
        path(url="/lista_os/os", clear=True, view=lista_os),
        path(url="os/finalizada/os", clear=True, view=os_finalizada)
    ]

    Routing(page=page, app_routes=app_routes)
    
    # Verifica se o usuário está logado
    if not page.session.get('logged_in'):
        mostrar_login(page)
    else:
        page.go("/")  # Redireciona para o menu se já estiver logado

def mostrar_login(page: ft.Page):
    page.clean()  # Limpa a página anterior
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.GREY_300

    logo = ft.Container(
        content=ft.Image(
            src='img/logo.jpeg',
            width=150,
            height=150,
        ),
        alignment=ft.alignment.center,  # Corrigido para usar ft.alignment
        padding=ft.padding.all(20)  # Adiciona padding ao redor da imagem
    )

    def fazer_login(e):
        usuario = entrada_nome.value
        senha = entrada_senha.value

        if usuario == 'fabiano' and senha == '1234':
            print('Login permitido')
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f'Bem-vindo, {usuario}')))
            page.session.set('logged_in', True)  # Usa o método set
            page.clean()  # Limpa a tela de login
            page.go("/")  # Redireciona para o menu
        else:
            print('Login não autorizado')
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Login não autorizado")))

    # Elementos da interface de login
    entrada_nome = ft.TextField(label="Digite o seu Login:", width=350, bgcolor=ft.colors.WHITE70)
    entrada_senha = ft.TextField(label="Digite sua senha:", width=350, bgcolor=ft.colors.WHITE70, password=True)
    bnt_salvar = ft.ElevatedButton('Entrar',bgcolor=ft.colors.BLUE_600, color='black', on_click=fazer_login)

    # Adiciona os elementos à página
    page.add(logo, entrada_nome, entrada_senha, bnt_salvar)
    

# Inicia o aplicativo
ft.app(target=rotas)
