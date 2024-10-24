import flet as ft 
from flet_route import Basket, Params
import sqlite3

conn = sqlite3.connect("db/os_finalizada.db", check_same_thread=False)
c = conn.cursor()

def os_finalizada(page: ft.Page, basket: Basket, params: Params):
    page.title = "OS Finalizada"

    def fetch_os_finalizada():
        c.execute("SELECT * FROM os_finalizada")
        return c.fetchall()
    
    def tabela_os_finalizada():
        rows.clear()
        entregas = fetch_os_finalizada()
        for entrega in entregas:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(content=ft.Text(entrega[1])),  
                    ft.DataCell(content=ft.Text(entrega[2])),  
                    ft.DataCell(content=ft.Text(entrega[3])),  
                    ft.DataCell(content=ft.Text(entrega[4])),  
                    ft.DataCell(content=ft.Text(entrega[5])),  
                    ft.DataCell(content=ft.Text(entrega[6])),  
                    ft.DataCell(content=ft.Text(entrega[7])),  
                    ft.DataCell(content=ft.Text(entrega[8])),  
                    ft.DataCell(content=ft.Text(entrega[9])),  
                    ft.DataCell(content=ft.Text(entrega[10])), # Data Saída
                    ft.DataCell(content=ft.Text(entrega[11])), # Modelo
                    ft.DataCell(content=ft.Text(entrega[12])), # Marca
                    ft.DataCell(content=ft.Text(entrega[13])), # Serial
                    ft.DataCell(content=ft.Text(entrega[14])), # Certificado
                    ft.DataCell(content=ft.Text(entrega[15])), # Senha
                    ft.DataCell(content=ft.Text(entrega[16])), # Data
                ]
            )
            rows.append(row)
        page.update()

    rows = []
    tabela_os_finalizada()

    return ft.View(
        "os/finalizada/os",
        bgcolor=ft.colors.GREY_300,
        controls=[
            ft.Row(
                controls=[
                    ft.MenuBar(
                        expand=True,
                        style=ft.MenuStyle(
                            alignment=ft.alignment.top_left,
                            bgcolor=ft.colors.BLUE_400,
                        ),
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_color=ft.colors.BLACK87,
                                on_click=lambda _: page.go('/'),
                                style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_600})
                            ),
                            ft.Text('OS Finalizada', size=25)
                        ]
                    )
                ]
            ),
            ft.Container(
                width=1600,
                content=ft.Row(
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text('N° OS')),
                                ft.DataColumn(ft.Text('Cliente')),
                                ft.DataColumn(ft.Text('Cpf')),
                                ft.DataColumn(ft.Text('Telefone')),
                                ft.DataColumn(ft.Text('Email')),
                                ft.DataColumn(ft.Text('Endereço')),
                                ft.DataColumn(ft.Text('Bairro')),
                                ft.DataColumn(ft.Text('Cidade')),
                                ft.DataColumn(ft.Text('Data Entrada')),
                                ft.DataColumn(ft.Text('Data Saída')),
                                ft.DataColumn(ft.Text('Modelo')),
                                ft.DataColumn(ft.Text('Marca')),
                                ft.DataColumn(ft.Text('Serial')),
                                ft.DataColumn(ft.Text('Certificado')),
                                ft.DataColumn(ft.Text('Senha')),
                                ft.DataColumn(ft.Text('Data')),
                            ],
                            rows=rows,
                        )
                    ]
                )
            )
        ]
    )
