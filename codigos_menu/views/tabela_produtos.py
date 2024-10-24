import flet as ft
from flet_route import Basket, Params
import sqlite3
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

# Conexão com o banco de dados SQLite
conn = sqlite3.connect("db/produtos.db", check_same_thread=False)
c = conn.cursor()

def produtos_estoque(page: ft.Page, basket=Basket, params=Params):
    page.title = 'Lista de Produtos'

    def handle_menu_item_click(e):
        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked")))
        page.update()

    def obter_produtos():
        c.execute("SELECT * FROM produtos")
        return c.fetchall()

    def excluir_produtos(produto_id):
        c.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        conn.commit()
        alerta_dialogo.open = False
        atualizar_tabela()

    def abrir_modal(produto_id):
        alerta_dialogo.actions[0].data = produto_id
        alerta_dialogo.open = True
        page.dialog = alerta_dialogo
        page.update()

    def cancelar_exclusao(e):
        alerta_dialogo.open = False
        page.update()

    def atualizar_tabela():
        rows.clear()
        produtos = obter_produtos()
        for produto in produtos:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(content=ft.Text(produto[1])),
                    ft.DataCell(content=ft.Text(produto[2])),
                    ft.DataCell(content=ft.Text(produto[3])),
                    ft.DataCell(content=ft.Text(produto[4])),
                    ft.DataCell(content=ft.Text(produto[5])),
                    ft.DataCell(content=ft.Text(produto[6])),
                    ft.DataCell(content=ft.Text(str(produto[7]))),
                    ft.DataCell(content=ft.Text(f"R$ {produto[8]:.2f}")),
                    ft.DataCell(content=ft.Text(f"R$ {produto[9]:.2f}")),
                    ft.DataCell(content=ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color='red400',
                        on_click=lambda _, id=produto[0]: abrir_modal(id),
                    ))
                ]
            )
            rows.append(row)

        page.update()

    rows = []

    alerta_dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text('Exclusão'),
        content=ft.Text('Você deseja excluir este produto?'),
        actions=[
            ft.TextButton('Apagar', on_click=lambda e: excluir_produtos(e.control.data)),
            ft.TextButton('Cancelar', on_click=cancelar_exclusao)
        ]
    )

    atualizar_tabela()

    def imprimir_itens(e):
        pdf_file = "itens_em_estoque.pdf"  # Nome do arquivo PDF
        c = canvas.Canvas(pdf_file, pagesize=landscape(A4))  # PDF em modo paisagem
        width, height = landscape(A4)

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(20, height - 20,  "Itens em Estoque")

        # Títulos das colunas
        col_titles = ["Produto", "Nº Série", "Marca", "Cor", "Qtd", "P. Compra", "P. Venda"]
        for idx, title in enumerate(col_titles):
            c.drawString(20 + idx * 100, height - 100, title)

        # Adiciona a tabela de produtos no PDF
        c.setFont("Helvetica", 12)
        y = height - 120  # Posição inicial para os dados

        produtos = obter_produtos()
        for produto in produtos:
            # Desenha cada coluna em sua posição específica
            c.drawString(20, y, produto[1])               # Produto
            c.drawString(120, y, produto[2])              # Nº Série
            c.drawString(220, y, produto[3])              # Marca
            c.drawString(320, y, produto[6])              # Cor
            c.drawString(430, y, str(produto[7]))         # Qtd
            c.drawString(520, y, f"R$ {produto[8]:.2f}")  # P. Compra
            c.drawString(620, y, f"R$ {produto[9]:.2f}")  # P. Venda

            y -= 20  # Espaçamento entre as linhas

            if y < 50:  # Se atingir o fim da página, cria uma nova
                c.showPage()
                c.setFont("Helvetica", 12)
                # Redefine a posição y para o topo da nova página
                y = height - 100  

                for idx, title in enumerate(col_titles):
                    c.drawString(20 + idx * 100, height - 100, title)

        c.save()  # Salva o arquivo PDF
        page.show_snack_bar(ft.SnackBar(content=ft.Text("PDF gerado com sucesso!")))
        page.update()

    def imprimir_faltantes(e):
        pdf_faltante = "itens_em_baixa.pdf"  # Nome do arquivo PDF
        c = canvas.Canvas(pdf_faltante, pagesize=landscape(A4))  # PDF em modo paisagem
        width, height = landscape(A4)

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(20, height - 20, "Itens em Baixa")

        # Títulos das colunas
        col_titles = ["Produto", "Nº Série", "Marca", "Cor", "Qtd", "P. Compra", "P. Venda"]
        for idx, title in enumerate(col_titles):
            c.drawString(20 + idx * 100, height - 100, title)

        # Adiciona a tabela de produtos no PDF
        c.setFont("Helvetica", 12)
        y = height - 120  # Posição inicial para os dados

        produtos = obter_produtos()  # Obter todos os produtos
        for produto in produtos:
            # Verifica se a quantidade é 5 ou inferior
            if produto[7] <= 5:
                c.drawString(20, y, produto[1])               # Produto
                c.drawString(120, y, produto[2])              # Nº Série
                c.drawString(220, y, produto[3])              # Marca
                c.drawString(320, y, produto[6])              # Cor
                c.drawString(430, y, str(produto[7]))         # Qtd
                c.drawString(520, y, f"R$ {produto[8]:.2f}")  # P. Compra
                c.drawString(620, y, f"R$ {produto[9]:.2f}")  # P. Venda

                y -= 20  # Espaçamento entre as linhas

                if y < 50:  # Se atingir o fim da página, cria uma nova
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    # Redefine a posição y para o topo da nova página
                    y = height - 100  

                    for idx, title in enumerate(col_titles):
                        c.drawString(20 + idx * 100, height - 100, title)

        c.save()  # Salva o arquivo PDF
        page.show_snack_bar(ft.SnackBar(content=ft.Text("PDF gerado com sucesso!")))
        page.update()


    return ft.View(
        "/produtos_estoque/produtos",
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
                                on_click=lambda _: page.go("/"),
                                icon_color=ft.colors.BLACK87,
                                style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_600}),
                            ),
                            ft.Text('Produtos em Estoque', size=25, width=1110),
                            ft.SubmenuButton(
                                content=ft.Text("Itens em Estoque"),
                                controls=[
                                    ft.MenuItemButton(
                                        content=ft.Text('Imprimir Faltantes'),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=imprimir_faltantes
                                    ),
                                    ft.MenuItemButton(
                                        content=ft.Text("Imprimir Estoque"),
                                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_200}),
                                        on_click=imprimir_itens
                                    )
                                ]
                            ),
                        ],
                    )
                ]
            ),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Produto")),
                    ft.DataColumn(ft.Text("Nº Série")),
                    ft.DataColumn(ft.Text("Marca")),
                    ft.DataColumn(ft.Text("Acessórios")),
                    ft.DataColumn(ft.Text("Descrição")),
                    ft.DataColumn(ft.Text("Cor")),
                    ft.DataColumn(ft.Text("Quantidade")),
                    ft.DataColumn(ft.Text("Preço de Compra")),
                    ft.DataColumn(ft.Text("Preço de Venda")),
                    ft.DataColumn(ft.Text('Excluir'))
                ],
                rows=rows
            )
        ]
    )

# Inicia o aplicativo
