import flet as ft
from flet_route import Params, Basket

def menu(page: ft.Page, params=Params, basket=Basket):
    
    def handle_menu_item_click(e):
        print(f"{e.control.content.value}, on_click")
        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked")))
        appbar_text_ref.current.value = e.control.content.value
        page.update()

    def handle_on_open(e):
        print(f"{e.control.content.value},on_click")

    def handle_on_close(e):
        print(f"{e.control.content.value},on_click")

    def handle_on_hover(e):
        print(f"{e.control.content.value},on_click")

    appbar_text_ref = ft.Ref[ft.Text]()
    
    return ft.View(
        "/",
        bgcolor = ft.colors.GREY_300,
        controls=[
            ft.AppBar(
                title=ft.Text('FMV - Menu', ref=appbar_text_ref),
                center_title=True,
                bgcolor=ft.colors.BLUE_600
            ),
            ft.Row( 
                controls=[
                    ft.MenuBar(
                        expand=True,
                        style=ft.MenuStyle(
                            alignment=ft.alignment.top_left,
                            bgcolor=ft.colors.BLUE_400
                        ),
                        controls=[
                            ft.SubmenuButton(
                                content=ft.Text('Cadastros'),
                                on_open=handle_on_open,
                                on_close=handle_on_close,
                                on_hover=handle_on_hover,
                                controls=[
                                    ft.MenuItemButton(
                                        content=ft.Text('Cadastrar Cliente'),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=lambda _: page.go("/cadastro_cliente/cadastrar_cliente")
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text('Cadastrar Produtos'),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=lambda _:page.go("/cadastro_produto/produto")
                                    ),
                                ]
                            ),
                            ft.SubmenuButton(
                                content=ft.Text('Ordem de Serviço'),
                                on_open=handle_on_open, 
                                on_close=handle_on_close,
                                on_hover=handle_on_hover,
                                controls=[
                                    ft.MenuItemButton(
                                        content=ft.Text('OS Entrada'),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=lambda _:page.go("/devolucao_os/devolver")
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text('OS Saída'),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=lambda _:page.go("/entrega_os/entrega")
                                    ),
                                ]
                            ),
                            ft.SubmenuButton(
                                content=ft.Text('Listas'),
                                on_open=handle_on_open,
                                on_close=handle_on_close,
                                on_hover=handle_on_hover,
                                controls=[
                                    ft.MenuItemButton(
                                        content=ft.Text('Produtos em Estoque'),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=lambda _:page.go('/produtos_estoque/produtos')
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text('Lista de Clientes '),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=lambda _:page.go("/lista_cliente/lista")
                                    ),
                                
                                ]
                            ),
                            ft.SubmenuButton(
                                content=ft.Text('Lista de OS'),
                                on_open=handle_on_open,
                                on_close=handle_on_close,
                                on_hover=handle_on_hover,
                                controls=[
                                    ft.MenuItemButton(
                                        content=ft.Text("OS em aberto "),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click= lambda _: page.go("/lista_os/os"),
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text("OS finalizada"),
                                        style= ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click= lambda _: page.go("os/finalizada/os")
                                                        
                                    )
                                  
                                ]
                            )
                            
                        ]
                    )
                    
                ]
            )
        ]
    )


#ft.app(target=menu) - This line is commented out as per your request
