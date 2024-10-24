import flet as ft
from flet_route import Basket, Params  # Verifique se as importações estão corretas com base na estrutura do seu projeto
import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('db/clientes.db', check_same_thread=False)
c = conn.cursor()

def lista_cliente(page: ft.Page, basket=Basket, params=Params):
    page.title = 'Lista de Clientes'
    page.bgcolor = ft.colors.BLUE_200

    # Função para obter todos os clientes cadastrados no banco de dados
    def obter_clientes():
        c.execute('SELECT * FROM clientes')
        return c.fetchall()

    # Função para excluir um cliente do banco de dados
    def excluir_cliente(cliente_id):
        c.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        conn.commit()

        # Fecha o diálogo de confirmação após a exclusão
        alerta_dialogo.open = False
        
        # Atualiza a lista de clientes após a exclusão
        atualizar_tabela()

    # Função para abrir o modal de exclusão
    def abrir_modal(cliente_id):
        # Configura o diálogo de exclusão com o cliente_id passado
        alerta_dialogo.actions[0].data = cliente_id
        page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        # Atualiza a página para refletir o estado do diálogo
        page.update()

    # Função para fechar o modal de exclusão ao clicar em "Cancelar"
    def cancelar_exclusao(e):
        alerta_dialogo.open = False
        page.update()

    # Função para atualizar a tabela de clientes
    def atualizar_tabela():
        rows.clear()
        clientes = obter_clientes()
        for cliente in clientes:
            cliente_id = cliente[0]
            nome_cliente = cliente[1]
            cpf_cnpj = cliente[2]
            telefone = cliente[3]
            email = cliente[7]
            endereco = cliente[4]
            bairro = cliente[6]
            cidade = cliente[5]

            # Cria uma linha de dados para cada cliente
            row = ft.DataRow(
                cells=[
                    ft.DataCell(content=ft.Text(nome_cliente)),
                    ft.DataCell(content=ft.Text(cpf_cnpj)),
                    ft.DataCell(content=ft.Text(telefone)),
                    ft.DataCell(content=ft.Text(email)),
                    ft.DataCell(content=ft.Text(endereco)),
                    ft.DataCell(content=ft.Text(bairro)),
                    ft.DataCell(content=ft.Text(cidade)),
                    ft.DataCell(content=ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color="red400",
                        on_click=lambda _, id=cliente_id: abrir_modal(id),  # Passa o cliente_id para abrir_modal
                    )),
                ]
            )
            rows.append(row)

        # Atualiza a visualização com a tabela dinâmica de clientes
        page.update()

    # Inicializa a lista de linhas da tabela
    rows = []

    # AlertDialog para confirmação de exclusão
    alerta_dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text('Exclusão'),
        content=ft.Text("Você deseja excluir esse cliente?"),
        actions=[
            ft.TextButton('Apagar', on_click=lambda e: excluir_cliente(e.control.data)),
            ft.TextButton('Cancelar', on_click=cancelar_exclusao)
        ]
    )

    # Chama a função para atualizar a tabela inicialmente
    atualizar_tabela()

    # Cria a visualização com a tabela dinâmica de clientes
    return ft.View(
        "/lista_cliente/cliente",
        bgcolor=ft.colors.GREY_300,
        scroll=ft.ScrollMode.AUTO,
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
                                style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_600})
                            ),
                            ft.Text('Lista de Clientes', size=25)
                        ]
                    )
                ]
            ),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Cpf/Cnpj")),
                    ft.DataColumn(ft.Text("Celular")),
                    ft.DataColumn(ft.Text("Email")),
                    ft.DataColumn(ft.Text("Endereço")),
                    ft.DataColumn(ft.Text("Bairro")),
                    ft.DataColumn(ft.Text("Cidade")),
                    ft.DataColumn(ft.Text("Excluir"))  # Adiciona uma coluna para o botão de exclusão
                ],
                rows=rows
            )
        ]
    )
