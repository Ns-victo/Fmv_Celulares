import flet as ft
from flet import Row
import sqlite3
from flet_route import Params, Basket
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

conn = sqlite3.connect('db/entrega.db', check_same_thread=False)
c = conn.cursor()

conn = sqlite3.connect('db/os_finalizada.db', check_same_thread=False)
c_os = conn.cursor()



def tabela_os():
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS entrega (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_os TEXT UNIQUE,
            data_entrega TEXT,
            saida TEXT,
            telefone TEXT,
            sintomas TEXT,
            valor_total TEXT,
            cliente_os TEXT,
            cpf_cnpj TEXT,
            email TEXT,
            modelo TEXT,
            endereco TEXT,
            bairro TEXT,
            cidade TEXT,
            marca TEXT,
            serial TEXT,
            certificado TEXT,
            senha TEXT,
            data TEXT,
            data_saida TEXT     
        )
    """)
    conn.commit()

tabela_os()

def tabela_os_finalizada():
    c_os = conn.cursor()
    c_os.execute("""
        CREATE TABLE IF NOT EXISTS os_finalizada (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_os TEXT UNIQUE,
                    cliente TEXT,
                    endereco TEXT,
                    bairro TEXT,
                    cidade TEXT,
                    cpf_cnpj TEXT,
                    telefone TEXT,
                    email TEXT,
                    data_entrega TEXT,
                    saida TEXT,
                    sintomas TEXT,
                    valor REAL,
                    pecas_substituidas TEXT,
                    marca TEXT,
                    modelo TEXT 
        )
    """)
    conn.commit()

tabela_os_finalizada()

def carregar_os(numero_os):
    c.execute('SELECT * FROM entrega WHERE numero_os = ?', (numero_os,))
    os_numero = c.fetchone()
    return os_numero

def carregar_todos_os():
    c.execute("SELECT numero_os FROM entrega")
    entregas = c.fetchall()
    return entregas

def entrega_aparelho(page: ft.Page, params=Params, basket=Basket):
    
    page.bgcolor = ft.colors.BLUE_400
    page.title = 'Fmv Celulares - Entrada'
    
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

    dict_values = {
        'numero_os': '',
        'data_entrega': '',
        'saida': '',
        'telefone': '',
        'sintomas': '',
        'valor_total': '',
        'cliente_os': '',
        'cpf_cnpj': '',
        'email': '',
        'modelo': '',
        'endereco': '',
        'bairro': '',
        'cidade': '',
        'marca': '',
        'serial': '',
        'certificado': '',
        'senha': '',
        'data': '',
    }

    def finalizar_os(e):
        dict_values["numero_os"] = numero_os_nota.value
        dict_values["data_entrega"] = data_entrega.value
        dict_values["saida"] = saida.value
        dict_values["telefone"] = telefone.value
        dict_values["sintomas"] = sintomas.value
        dict_values["valor"] = valor.value
        dict_values["cliente"] = cliente.value
        dict_values["cpf_cnpj"] = cpf_cnpj.value
        dict_values["email"] = email.value
        dict_values["modelo"] = modelo.value
        dict_values["endereco"] = endereco.value
        dict_values["bairro"] = bairro.value
        dict_values["cidade"] = cidade.value
        dict_values["marca"] = marca.value
        dict_values["serial"] = serial.value
        dict_values["certificado"] = Certificado.value
        dict_values["senha"] = senha_desb.value
        dict_values["data"] = data.value
        
        c_os.execute(
            'INSERT INTO os_finalizada (numero_os, data_entrega, saida, telefone, sintomas, valor, cliente, cpf_cnpj, email, modelo, endereco, bairro, cidade, marca, serial, certificado, senha, data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (dict_values["numero_os"], dict_values["data_entrega"], dict_values["saida"], dict_values["telefone"],dict_values["sintomas"],
             dict_values["valor"], dict_values["cliente"], dict_values["cpf_cnpj"], dict_values["email"], dict_values["modelo"],
             dict_values["endereco"], dict_values["bairro"], dict_values["cidade"], dict_values["marca"], dict_values["serial"],dict_values["certificado"],
             dict_values["senha"], dict_values["data"]))
        conn.commit()
        mensagem = ft.SnackBar(
            content=ft.Text('OS finalizada com sucusso.'),
            action='fechar'
        )
        page.show_snack_bar(mensagem)
    
    
    def preencher_campos(numero_os_value):
        os_numero = carregar_os(numero_os_value)
        if os_numero:
            numero_os_nota.value = os_numero[1]
            data_entrega.value = os_numero[2]
            saida.value = os_numero[3]
            endereco.value = os_numero[11]
            bairro.value = os_numero[12]
            cidade.value = os_numero[13]
            cpf_cnpj.value = os_numero[8]
            telefone.value = os_numero[4]
            email.value = os_numero[9]
            modelo.value = os_numero[10]
            marca.value = os_numero[14]
            serial.value = os_numero[15]
            Certificado.value = os_numero[16]
            senha_desb.value = os_numero[17]
            data.value = os_numero[18]
            acessorios.value = os_numero[23]
            sintomas.value = os_numero[5]
            garantia.value = os_numero[20]
            nota.value = os_numero[21]
            revenda.value = os_numero[22]
            valor.value = os_numero[6]
            cliente.value = os_numero[7]
            page.update()

        else:
            mensagem_erro = ft.SnackBar(
                content=ft.Text('OS não encontrado.'),
                action='fechar'
            )
            page.show_snack_bar(mensagem_erro)

    def close_anchor(e):
        numero_os_value = e.control.data['numero_os']
        preencher_campos(numero_os_value)
        
    def handle_change(e):
        print(f"handle_change e.data: {e.data}")

    def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")

    def handle_tap(e):
        print(f"handle_tap")

    entregas = carregar_todos_os()
    
    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Escolha um N° OS",
        view_hint_text="Número de OS",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        width=350,
        height=35,
        controls=[
            ft.ListTile(title=ft.Text(f"{os_numero[0]}"), on_click=close_anchor, data={'numero_os': os_numero[0]})
            for os_numero in entregas
        ],
    )
    
    # Campos de texto e controles
    numero_os_nota = ft.TextField(label='Número de OS.', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    data_entrega = ft.TextField(label='Data de Entrada.', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    saida = ft.TextField(label='Data de Saída.', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    comprov_entrega = ft.Text('Comprovante de Devolução', weight='bold')
    txt_dadoscliente = ft.Text('Dados do Cliente', weight='bold')
    cliente = ft.TextField(label='Nome do cliente', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    endereco = ft.TextField(label='Endereço', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    cidade = ft.TextField(label='Cidade', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    bairro = ft.TextField(label='Bairro', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    cpf_cnpj = ft.TextField(label='CPF/CNPJ', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    telefone = ft.TextField(label='Whatsapp', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    email = ft.TextField(label='Email', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    txt_dadosaparelho = ft.Text('Dados do Aparelho', weight='bold')
    modelo = ft.TextField(label='Modelo', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    marca = ft.TextField(label='Marca', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    serial = ft.TextField(label="N° Série", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    Certificado = ft.TextField(label="Certificado", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    data = ft.TextField(label="Data", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    acessorios = ft.TextField(label="Acessórios", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    sintomas = ft.TextField(label="Sintomas", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    operadora = ft.TextField(label='Operadora', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    senha_desb = ft.TextField(label="Senha", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    nota = ft.TextField(label="Nota", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    revenda = ft.TextField(label="Revenda", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    txt_dadosdiversos = ft.Text('Dados Diversos', weight='bold')
    pcas_substituidas = ft.TextField(label='Peças Substituídas', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    tp_entrega = ft.TextField(label="Tempo de Garantia", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    garantia = ft.TextField(label='Garantia', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    valor = ft.TextField(label='Valor Total', width=350, height=30, text_size=13.5,prefix_text='R$ ',bgcolor=ft.colors.WHITE70)
    bnt_finalizar = ft.ElevatedButton("Fechar OS", bgcolor=ft.colors.BLUE_600, color='black',on_click=finalizar_os)
    
    def gerar_pdf(e):
        pdf_file = f"Comprovante_{numero_os_nota.value}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=A4)
        width, height = A4

        # Cabeçalho
        c.drawImage('img/logo.jpeg', 50, height - 100, width=100, height=100)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, height - 50, "Comprovante de Devolução")

        # Dados do Cliente e do Aparelho
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 150, f"N° OS: {numero_os_nota.value}")
        c.drawString(165,height - 150, f"Data de Entrada: {data_entrega.value}")
        c.drawString(350,height - 150, f"Data de Saída: {saida.value}")
        c.drawString(50, height - 180, f"Endereço: {endereco.value}")
        c.drawString(50, height - 200, f"Bairro: {bairro.value}")
        c.drawString(50, height - 220, f"Cidade: {cidade.value}")
        c.drawString(50, height - 240, f"Cpf: {cpf_cnpj.value}")
        c.drawString(50, height - 260, f"Telefone: {telefone.value}")
        c.drawString(50, height - 280, f"Email: {email.value}")
        c.drawString(50, height - 300, f"Modelo: {modelo.value}")
        c.drawString(50, height - 320, f"Marca: {marca.value}")
        c.drawString(50, height - 340, f"N° Série: {serial.value}")
        c.drawString(50, height - 360, f"Certificado: {Certificado.value}")
        c.drawString(50, height - 380, f"Data: {data.value}")
        c.drawString(50, height - 400, f"Acessórios: {acessorios.value}")
        c.drawString(50, height - 420, f"Sintomas: {sintomas.value}")
        c.drawString(50, height - 440, f"Operadora: {operadora.value}")
        c.drawString(50, height - 460, f"Senha: {senha_desb.value}")
        c.drawString(50, height - 480, f"Nota: {nota.value}")
        c.drawString(50, height - 500, f"Revenda: {revenda.value}")
        c.drawString(50, height - 520, f"Peças Substituídas: {pcas_substituidas.value}")
        c.drawString(50, height - 540, f"Tipo de Entrega: {tp_entrega.value}")
        c.drawString(50, height - 560, f"Garantia: {garantia.value}")
        c.drawString(50, height - 580, f"Valor Total: {valor.value}")
        
        # Rodapé
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, height - 620, "Declaro estar recebendo os materiais constantes nesta ordem de serviço. Devidamente reparado.")
        c.drawString(50, height - 640, "*Atenção! A não retirada do aparelho no prazo de 90 (noventa) dias será acrescido diárias de R$5,00 (cinco reais) por dia.")
        c.drawString(50, height - 660, "A retirada do aparelho somente com a apresentação da ordem de serviço.")
        c.drawString(50, height - 680, "Não nos responsabilizamos por SIM CARD (chip) ou cartão de memória deixados junto ao aparelho.")
        c.drawString(50, height - 700, "Garantia de 90 (noventa) dias somente do serviço executado. Não é coberto por garantia por maus usos.")
        c.drawString(50, height - 740, "Assinatura: _______________________________________")
        c.drawString(50, height - 780, "FMV: ______________________________________________")
        c.save()
        
        mensagem = ft.SnackBar(
            content=ft.Text("Print realizado com sucesso."),
            action='fechar'
        )
        page.show_snack_bar(mensagem)

    imprimir_os = ft.ElevatedButton('Print', bgcolor=ft.colors.BLUE_600, color='black', on_click=gerar_pdf)

    return ft.View(
        "/entrega_os/entrega",
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
                                on_click=lambda _: page.go('/'),
                                icon_color=ft.colors.BLACK87,
                                style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_600}),
                            ),
                            ft.Text('OS Saída', size=25),
                        ]
                    )
                ]
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        Row(controls=[logo, comprov_entrega]),
                        Row(controls=[anchor]),
                        Row(controls=[numero_os_nota, data_entrega, saida]),
                        Row(controls=[txt_dadoscliente]),
                        Row(controls=[cliente, cpf_cnpj, telefone, email]),
                        Row(controls=[endereco, bairro, cidade]),
                        Row(controls=[txt_dadosaparelho]),
                        Row(controls=[modelo, marca, serial]),
                        Row(controls=[Certificado, data, acessorios]),
                        Row(controls=[sintomas, operadora, senha_desb]),
                        Row(controls=[nota, revenda]),
                        Row(controls=[txt_dadosdiversos]),
                        Row(controls=[pcas_substituidas, tp_entrega, garantia, valor]),
                        Row(controls=[imprimir_os,bnt_finalizar])
                    ]
                )
            )
        ]
    )
