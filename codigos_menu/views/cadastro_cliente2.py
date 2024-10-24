import flet as ft
import sqlite3
from flet_route import Params, Basket

conn = sqlite3.connect('db/clientes.db', check_same_thread=False)
c = conn.cursor()

def criar_tabela():
    c.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_cliente TEXT,
        cpf_cnpj TEXT UNIQUE , 
        telefone TEXT,
        email TEXT,
        endereco TEXT,
        bairro TEXT,
        cidade TEXT        
    )""")
    conn.commit()

criar_tabela()

def validar_cpf(cpf_cnpj):
    if len(cpf_cnpj) != 11 and len(cpf_cnpj) != 14:  # Verifica se o CPF ou CNPJ tem o tamanho correto
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    pesos = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(9):
        soma += int(cpf_cnpj[i]) * pesos[i]
    resto = soma % 11
    if resto < 2:
        digito_verif1 = 0
    else:
        digito_verif1 = 11 - resto

    # Calcula o segundo dígito verificador
    soma = 0
    pesos.insert(0, 11)
    for i in range(10):
        soma += int(cpf_cnpj[i]) * pesos[i]
    resto = soma % 11
    if resto < 2:
        digito_verif2 = 0
    else:
        digito_verif2 = 11 - resto

    # Verifica se os dígitos verificadores calculados correspondem aos fornecidos
    if int(cpf_cnpj[-2]) == digito_verif1 and int(cpf_cnpj[-1]) == digito_verif2:
        return True
    else:
        return False

def carregar_cliente(cpf_cnpj):# PARA BUSCAR AS INFORMAÇÕES NO BANCO DE DADOS BASEANDO - SE PELO CPF (USANDO UMA INFORMAÇÃO DE ACESSO ÚNICO )
    c.execute("SELECT * FROM clientes WHERE cpf_cnpj = ?", (cpf_cnpj,))
    cliente = c.fetchone()
    return cliente

def cadastrar_cliente(page: ft.Page, params=Params, basket=Basket):
    # Defina a cor de fundo aqui
    page.title = 'Cadastre seu Cliente'
    
    dict_values = {
        'nome_cliente': '',
        'cpf_cnpj': '',
        'telefone': '',
        'email': '',
        'endereco': '',
        'bairro': '',
        'cidade': '',
    }

    def cpf_unico(cpf_cnpj_value):
        c.execute("SELECT COUNT(*) FROM clientes WHERE cpf_cnpj = ?", (cpf_cnpj_value,))
        count = c.fetchone()[0]
        return count == 0

    def salvar_clientes(cpf_cnpj_value):
        if not validar_cpf(cpf_cnpj_value):
            mensagem_erro = ft.SnackBar(
                content=ft.Text("CPF ou CNPJ inválido."),
                action='fechar'
            )
            page.show_snack_bar(mensagem_erro)
            return
        
        if not cpf_unico(cpf_cnpj_value):
            mensagem_erro = ft.SnackBar(
                content=ft.Text("CPF ou CNPJ já cadastrado."),
                action='fechar'
            )
            page.show_snack_bar(mensagem_erro)
            return
        
        dict_values['nome_cliente'] = nome_cliente.value
        dict_values['cpf_cnpj'] = cpf_cnpj_value
        dict_values['telefone'] = telefone.value
        dict_values['email'] = email.value
        dict_values['endereco'] = endereco.value
        dict_values['bairro'] = bairro.value
        dict_values['cidade'] = cidade.value

        c.execute('INSERT INTO clientes (nome_cliente, cpf_cnpj, telefone, email, endereco, bairro, cidade) VALUES (?,?,?,?,?,?,?)',
                  (dict_values['nome_cliente'], dict_values['cpf_cnpj'], dict_values['telefone'], dict_values['email'],
                   dict_values['endereco'], dict_values['bairro'], dict_values['cidade']))
        conn.commit()

        mensagem = ft.SnackBar(
            content=ft.Text('Cliente salvo com sucesso.'),
            action='Fechar'
        )
        page.show_snack_bar(mensagem)

    def atualizar_cliente(e):
        novo_telefone = telefone.value
        novo_email = email.value
        novo_endereco = endereco.value
        novo_bairro = bairro.value
        nova_cidade = cidade.value
        cpf_cnpj_cliente = cpf_cnpj.value.strip()  # Obtém o valor do campo e remove espaços em branco
        
        c.execute("SELECT COUNT(*) FROM clientes WHERE cpf_cnpj = ?", (cpf_cnpj_cliente,))
        count = c.fetchone()[0]
        
        if count == 0:
            mensagem_erro = ft.SnackBar(
                content=ft.Text("Cliente não encontrado."),
                action='fechar'
            )
            page.show_snack_bar(mensagem_erro)
            return
        
        c.execute("""
                    UPDATE clientes
                    SET telefone = ?, email = ?, endereco = ?, bairro = ?, cidade = ?
                    WHERE cpf_cnpj = ?
                    """, (novo_telefone, novo_email, novo_endereco, novo_bairro, nova_cidade, cpf_cnpj_cliente))
        conn.commit()

        mensagem = ft.SnackBar(
            content=ft.Text("Cliente atualizado com sucesso!"),
            action='fechar'
        )
        page.show_snack_bar(mensagem)

        # Limpa os campos após a atualização
        nome_cliente.value = ''
        cpf_cnpj.value = ''
        telefone.value = ''
        email.value = ''
        endereco.value = ''
        bairro.value = ''
        cidade.value = ''
        page.update()

    # Função para preencher os campos com os dados do cliente
    def preencher_campos(cpf_cnpj_value):
        cliente = carregar_cliente(cpf_cnpj_value)#VARIÁVEL COM FUNÇÃO ATRIBUIDA (JUNTO AO PARAMETRO RESPONSÁVEL PELA BUSCA NO BANCO  DE DADOS )
        if cliente:
            nome_cliente.value = cliente[1]
            cpf_cnpj.value = cliente[2]
            telefone.value = cliente[3]
            email.value = cliente[7]
            endereco.value = cliente[4]
            bairro.value = cliente[6]
            cidade.value = cliente[5]
            page.update()
        else:
            mensagem_erro = ft.SnackBar(
                content=ft.Text("Cliente não encontrado."),
                action='fechar'
            )
            page.show_snack_bar(mensagem_erro)

    def close_anchor(e):
        cpf_cnpj_value = e.control.data['cpf_cnpj']
        preencher_campos(cpf_cnpj_value)

    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data {e.data}" )

    def handle_tap(e):
        print(f"handle_tap")

    def carregar_clientes():
        c.execute("SELECT cpf_cnpj FROM clientes")
        clientes = c.fetchall()
        return clientes
    
    clientes = carregar_clientes()

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.BLUE_700,
        bar_hint_text="Pesquise pelo CPF do cliente",
        view_hint_text="Escolha um CPF",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        width=350,
        height=35,
        controls=[
            ft.ListTile(title=ft.Text(f"{cliente[0]}"), on_click=close_anchor, data={'cpf_cnpj': cliente[0]})
            for cliente in clientes
        ],
    )

    nome_cliente = ft.TextField(label='Nome do cliente', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    cpf_cnpj = ft.TextField(label='CPF OU CNPJ', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    telefone = ft.TextField(label='Whatsapp', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    email = ft.TextField(label='Email', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    endereco = ft.TextField(label='Endereço', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    cidade = ft.TextField(label='Cidade', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    bairro = ft.TextField(label='Bairro', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    bnt_cadastrar = ft.ElevatedButton('Salvar', on_click=lambda _: salvar_clientes(cpf_cnpj.value.strip()), bgcolor=ft.colors.BLUE_600, color='black')
    bnt_atualizar = ft.ElevatedButton('Atualizar', bgcolor=ft.colors.BLUE_600, color='black', on_click=atualizar_cliente)
     
    return ft.View(
        "/cadastro_cliente2/cadastrar_cliente",
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
                            ft.Text("Cadastro de Clientes", size=25)              
                        ]
                    )
                ]
            ),
            anchor,
            nome_cliente,
            cpf_cnpj,
            telefone,
            email,
            endereco,
            bairro,
            cidade,
            bnt_cadastrar,
            bnt_atualizar
        ]
    )
