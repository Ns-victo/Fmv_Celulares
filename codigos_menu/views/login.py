import flet as ft
from flet import Row
from flet_route import Basket, Params


def tela_login(page: ft.Page, params= Params, basket=Basket):
    page.title = 'Fmv Celulares - Login'
    page.bgcolor = ft.colors.BLUE_400

    logo = ft.Container(
        margin=ft.margin.only(right=150),
        content=ft.Row(
            controls=[
                ft.Image(
                    src='img/logo.jpeg',
                    width=150,
                    height=150,
                )
            ]
        )
    )
    def login(e):
        usuario = entrada_nome.value
        senha = entrada_senha.value

        if usuario == 'fabiano' and senha == '12345':
            print('Login permitido')
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Bem-vindo, {usuario}")))
            page.go("/")  # Redireciona para o menu após o login
        else:
            print('Login incorreto')
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Login incorreto")))

    entrada_nome = ft.TextField(label="Digite o seu nome.", width=350, bgcolor=ft.colors.WHITE70)
    entrada_senha = ft.TextField(label="Digite sua senha.", width=350, bgcolor=ft.colors.WHITE70, password=True)
    bnt_salvar = ft.ElevatedButton('Entrar', on_click=login),


    



    
    page.add(
        logo,
        entrada_nome,
        entrada_senha,
        bnt_salvar
    )



    
    
ft.app(target=tela_login)
