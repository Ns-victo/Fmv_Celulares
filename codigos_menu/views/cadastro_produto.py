import flet as ft
import sqlite3
from flet_route import Params, Basket

conn = sqlite3.connect('db/produtos.db', check_same_thread=False)
c = conn.cursor()

def criar_tabela():
    c.execute("""
        CREATE TABLE IF NOT EXISTS produtos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT,
            n_serie TEXT,
            marca TEXT,
            acessorio TEXT,
            descricao TEXT,
            cor TEXT,
            quantidade INTEGER,
            preco_compra REAL,
            preco_venda REAL
        )
    """)
    conn.commit()

criar_tabela()

def carregar_produto_por_n_serie(n_serie):
    c.execute('SELECT * FROM produtos WHERE n_serie = ?', (n_serie,))
    produto = c.fetchone()
    return produto

def carregar_todos_produtos():
    c.execute("SELECT n_serie FROM produtos")
    produtos = c.fetchall()
    return produtos

def cadastro_produto(page: ft.Page, params=Params, basket=Basket):
    page.title = 'Cadastrar Produto'

    dict_values = {
        'nome_produto': '',
        'n_serie': '',
        'marca': '',
        'acessorio_produto': '',
        'descricao_produto': '',
        'cor': '',
        'quantidade': '',
        'preco_compra': '',
        'preco_venda': ''
    }

    def salvar_produto(e):
        dict_values['nome_produto'] = nome_produto.value
        dict_values['n_serie'] = n_serie.value
        dict_values['marca'] = marca.value
        dict_values['acessorio_produto'] = acessorio_produto.value
        dict_values['descricao_produto'] = descricao_produto.value
        dict_values['cor'] = cor.value
        dict_values['quantidade'] = quantidade.value
        formatacao_preco = preco_compra.value.replace(",", ".").replace(",", ".")
        dict_values['preco_compra'] = formatacao_preco
        formatacao_preco_venda = preco_venda.value.replace(",", ".").replace(",", ".")
        dict_values['preco_venda'] = formatacao_preco_venda

        c.execute('INSERT INTO produtos (nome_produto, n_serie, marca, acessorio, descricao, cor, quantidade, preco_compra, preco_venda) VALUES (?,?,?,?,?,?,?,?,?)',
                  (dict_values['nome_produto'], dict_values['n_serie'], dict_values['marca'],
                   dict_values['acessorio_produto'], dict_values['descricao_produto'],
                   dict_values['cor'], dict_values['quantidade'], dict_values['preco_compra'],
                   dict_values['preco_venda']))
        conn.commit()

        mensagem = ft.SnackBar(
            content=ft.Text('Produto salvo com sucesso'),
            action='fechar'
        )
        page.show_snack_bar(mensagem)

    def atualizar_produto(e):
        novo_nome_produto = nome_produto.value
        novo_descricao_produto = descricao_produto.value
        nova_cor = cor.value
        nova_quantidade = quantidade.value
        novo_preco_compra = preco_compra.value
        novo_preco_venda = preco_venda.value
        n_serie_produto = n_serie.value.strip()

        c.execute("""
                    UPDATE produtos 
                    SET nome_produto = ?, descricao = ?, cor = ?, quantidade = ?, preco_compra = ?, preco_venda = ?
                    WHERE n_serie = ?
                  """,
                  (novo_nome_produto, novo_descricao_produto, nova_cor, nova_quantidade, novo_preco_compra, novo_preco_venda, 
                   n_serie_produto))
        conn.commit()

        mensagem = ft.SnackBar(
            content=ft.Text('Produto atualizado com sucesso'),
            action='fechar'
        )
        page.show_snack_bar(mensagem)

        nome_produto.value = ""
        descricao_produto.value = ""
        cor.value = ""
        preco_compra.value = ""
        quantidade.value = ""
        preco_compra.value = ""
        preco_venda.value = ""
        n_serie.value = ""
        page.update()

    def preencher_campos(n_serie_value):
        produto = carregar_produto_por_n_serie(n_serie_value)
        if produto:
            nome_produto.value = produto[1]
            n_serie.value = produto[2]
            marca.value = produto[3]
            acessorio_produto.value = produto[4]
            descricao_produto.value = produto[5]
            cor.value = produto[6]
            quantidade.value = produto[7]
            preco_compra.value = produto[8]
            preco_venda.value = produto[9]
            page.update()
        else:
            mensagem_erro = ft.SnackBar(
                content=ft.Text('Produto não encontrado.'),
                action='fechar'
            )
            page.show_snack_bar(mensagem_erro)

    def close_anchor(e):
        n_serie_value = e.control.data['n_serie']
        preencher_campos(n_serie_value)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data{e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    produtos = carregar_todos_produtos()

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.BLUE_700,
        bar_hint_text="Pesquise pelo número de série",
        view_hint_text="Escolha seu produto",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        width=350,
        height=35,
        controls=[
            ft.ListTile(title=ft.Text(f"{produto[0]}"), on_click=close_anchor, data={'n_serie': produto[0]})
            for produto in produtos
        ],
    )

    nome_produto = ft.TextField(label='Nome do produto', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    n_serie = ft.TextField(label='Número de série', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    marca = ft.TextField(label='Marca', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    acessorio_produto = ft.TextField(label='Acessórios', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    descricao_produto = ft.TextField(label='Descrição', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    cor = ft.TextField(label='Cor', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    quantidade = ft.TextField(label='Peças em estoque', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    preco_compra = ft.TextField(label='Preço de Compra', width=350, height=30, text_size=13.5, prefix_text='R$ ', bgcolor=ft.colors.WHITE70)
    preco_venda = ft.TextField(label='Preco de venda', width=350, height=30, text_size=13.5, prefix_text='R$ ', bgcolor=ft.colors.WHITE70)
    bnt_cadastrar = ft.ElevatedButton(text='Salvar', on_click=salvar_produto, bgcolor=ft.colors.BLUE_600, color='black')
    bnt_atualizar = ft.ElevatedButton(text='atualizar', on_click=atualizar_produto, bgcolor=ft.colors.BLUE_600, color='black')

    return ft.View(
        "/cadastro_produto",
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
                            ft.Text("Cadastro de Produtos", size=25)
                        ]
                    )
                ]
            ),
            anchor,
            nome_produto,
            n_serie,
            marca,
            acessorio_produto,
            descricao_produto,
            cor,
            quantidade,
            preco_compra,
            preco_venda,
            bnt_cadastrar,
            bnt_atualizar
        ]
    )

