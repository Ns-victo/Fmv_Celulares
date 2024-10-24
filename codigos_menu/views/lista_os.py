import flet as ft
from flet_route import Basket, Params
import sqlite3

conn = sqlite3.connect("db/entrega.db", check_same_thread=False)
c = conn.cursor()

def lista_os(page: ft.Page, basket=Basket, params=Params):
    page.title = "Lista de OS"

    def os_entrega():
        c.execute("SELECT * FROM entrega")
        return c.fetchall()

    def excluir_os(entrega_id):
        c.execute('DELETE FROM entrega WHERE id = ?', (entrega_id,))
        conn.commit()

        # Fecha o diálogo de confirmação após a exclusão
        alerta_dialogo.open = False

        # Atualiza a tabela de OS
        atualizar_os()

    def abrir_modal(entrega_id):
        alerta_dialogo.actions[0].data = entrega_id
        page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        page.update()

    def cancelar_exclusao(e):
        alerta_dialogo.open = False
        page.update()

    def atualizar_os():
        rows.clear()
        entregas = os_entrega()
        for entrega in entregas:
            numero_os = entrega[1]
            data_entrega = entrega[2]
            saida = entrega[3]
            telefone = entrega[4]
            sintomas = entrega[5]
            valor_total = f"R$ { entrega[6]}"
            cliente_os = entrega[7]
            cpf_cnpj = entrega[8]
            email = entrega[9]
            modelo = entrega[10]
            endereco = entrega[11]
            bairro = entrega[12]
            cidade = entrega[13]
            marca = entrega[14]
            serial = entrega[15]
            certificado = entrega[16]
            senha  = entrega[17]
            data = entrega[18]
            garantia = entrega[20]
            n_fiscal = entrega[21]
            revenda = f"R$ { entrega[22]}"
            acessorios = entrega[23]
            observacoes = entrega[25]
            row = ft.DataRow(
                cells=[
                    ft.DataCell(content=ft.Text(numero_os)),
                    ft.DataCell(content=ft.Text(cliente_os)),
                    ft.DataCell(content=ft.Text(cpf_cnpj)),
                    ft.DataCell(content=ft.Text(endereco)),
                    ft.DataCell(content=ft.Text(bairro)),
                    ft.DataCell(content=ft.Text(cidade)),
                    ft.DataCell(content=ft.Text(data_entrega)),
                    ft.DataCell(content=ft.Text(saida)),
                    ft.DataCell(content=ft.Text(telefone)),
                    ft.DataCell(content=ft.Text(email)),
                    ft.DataCell(content=ft.Text(modelo)),
                    ft.DataCell(content=ft.Text(marca)),
                    ft.DataCell(content=ft.Text(serial)),
                    ft.DataCell(content=ft.Text(sintomas)),
                    ft.DataCell(content=ft.Text(certificado)),
                    ft.DataCell(content=ft.Text(senha)),
                    ft.DataCell(content=ft.Text(garantia)),
                    ft.DataCell(content=ft.Text(data)),
                    ft.DataCell(content=ft.Text(n_fiscal)),
                    ft.DataCell(content=ft.Text(revenda)),
                    ft.DataCell(content=ft.Text(acessorios)),
                    ft.DataCell(content=ft.Text(observacoes)),
                    ft.DataCell(content=ft.Text(valor_total)),
                    ft.DataCell(content=ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color='red400',
                        on_click=lambda _, id=entrega[0]: abrir_modal(id)
                    ))
                    
                ]
            )
            rows.append(row)
        page.update()
    rows = []

    # Inicializa a tabela de OS chamando a função atualizar_os() no início
    atualizar_os()

    alerta_dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text('Exclusão'),
        content=ft.Text('Você deseja excluir esta OS?'),
        actions=[
            ft.TextButton('Apagar', on_click=lambda e: excluir_os(e.control.data)),
            ft.TextButton('Cancelar', on_click=cancelar_exclusao)
        ]
    )

    return ft.View(
        "/lista_os/os",
        scroll=ft.ScrollMode.AUTO,
        bgcolor=ft.colors.GREY_300,
        controls=[
            ft.Row(
                controls=[
                    ft.MenuBar(
                        expand=True,
                        style=ft.MenuStyle(
                            alignment=ft.alignment.top_left,
                            bgcolor=ft.colors.BLUE_400
                        ),
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_color=ft.colors.BLACK87,
                                on_click=lambda _: page.go("/"),
                                style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_600}),
                            ),
                            ft.Text('Lista de OS', size=25)
                        ]
                    )
                ]
            ),
            ft.Container(
                width=1600,  # Aumente a largura para acomodar todas as colunas
                content=ft.Row(
                    scroll=ft.ScrollMode.ALWAYS,  # Scroll horizontal sempre visível
                    controls=[
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("N° OS")),
                                ft.DataColumn(ft.Text("Cliente")),
                                ft.DataColumn(ft.Text("CPF/CNPJ")),
                                ft.DataColumn(ft.Text("Endereço")),
                                ft.DataColumn(ft.Text("Bairro")),
                                ft.DataColumn(ft.Text("Cidade")),
                                ft.DataColumn(ft.Text("Data de Entrega")),
                                ft.DataColumn(ft.Text("Data Devolução")),
                                ft.DataColumn(ft.Text("Telefone")),
                                ft.DataColumn(ft.Text("Email")),
                                ft.DataColumn(ft.Text("Modelo")),
                                ft.DataColumn(ft.Text("Marca")),
                                ft.DataColumn(ft.Text("N° de Série")),
                                ft.DataColumn(ft.Text("Sintomas")),
                                ft.DataColumn(ft.Text('Certificado')),
                                ft.DataColumn(ft.Text('Senha')),
                                ft.DataColumn(ft.Text('Garantia')),
                                ft.DataColumn(ft.Text('Data de Compra')),
                                ft.DataColumn(ft.Text('N° de NF')),
                                ft.DataColumn(ft.Text('Revenda')),
                                ft.DataColumn(ft.Text('Acessórios')),
                                ft.DataColumn(ft.Text('Observações')),
                                ft.DataColumn(ft.Text("Valor Total")),
                                ft.DataColumn(ft.Text("Excluir")),
                            ],
                            rows=rows,
                        ),
                    ]
                ),
            )
        ]
    )
