import sqlite3
import flet as ft
from flet import Row
from flet_route import Basket, Params
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('db/entrega.db', check_same_thread=False)
c = conn.cursor()

# Função para criar a tabela no banco de dados
def tabela_os():
    c.execute("""CREATE TABLE IF NOT EXISTS entrega (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_os TEXT UNIQUE,
                    data_entrega TEXT,
                    saida TEXT,
                    telefone TEXT,
                    sintomas TEXT,
                    valor_total TEXT,
                    cliente_os TEXT,
                    cpf_cnpf TEXT,
                    email TEXT,
                    modelo TEXT,
                    endereco TEXT,
                    bairro TEXT,
                    cidade TEXT,
                    marca TEXT,
                    serial TEXT
                    
                )""")
    conn.commit()

tabela_os()

# Classe para gerar códigos de OS
class CodeGenerator:
    def __init__(self):
        self.current = 0 

    def proximo_codigo(self):
        while True:
            if self.current < 999999:
                self.current += 1
                codigo = f'{self.current:06}'
                # Verificar se o código já existe no banco de dados
                c.execute("SELECT COUNT(*) FROM entrega WHERE numero_os = ?", (codigo,))
                if c.fetchone()[0] == 0:  # Se não existe, retornar o código
                    return codigo
            else:
                raise ValueError('O limite de 6 dígitos foi atingido')

def devolver(page: ft.Page, basket=Basket, params=Params):
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

    page.bgcolor = ft.colors.BLUE_400
    page.title = ('Fmv Celulares - Devolução')
    comprov_devolucao = ft.Text('Comprovante de Entrega', weight='bold')
    txt_empresa = ft.Text('''  
                                FMV
                                Av. Almirante Cochrane, 257 - Embaré - Canal 5 - Santos/SP
                                CEP: 11040-003
                                Whatsapp 13 99615-7359
                                fmvcelulares@gmail.com - Horário de funcionamento:
                                Segunda à Sexta  - 9:00 às 19:00 horas.
                          ''', weight='bold')

    dict_values = {
        'numero_os': '',
        'data_entrega': '',
        'saida': '',
        'telefone': '',
        'sintomas': '',
        'valor_total': '',
        'cliente_os': '',
    }

    def salvar_os(e):
        dict_values['numero_os'] = numero_os.value
        dict_values['data_entrega'] = data_entrega.value
        dict_values['saida'] = saida.value
        dict_values['telefone'] = telefone.value
        dict_values['sintomas'] = sintomas.value
        dict_values['valor_total'] = valor_total.value
        dict_values['cliente_os'] = cliente.value
        dict_values['cpf_cnpj'] = cpf_cnpj.value
        dict_values['email'] = email.value
        dict_values['modelo'] = modelo.value
        dict_values['endereco'] = endereco.value
        dict_values['bairro'] = bairro.value
        dict_values['cidade'] = cidade.value    
        dict_values['marca'] = marca.value
        dict_values['serial'] = serial.value
        dict_values['certificado'] = garantia.value
        dict_values['senha'] = senha_desb.value
        dict_values['data'] = data.value
        dict_values['saida'] = saida.value
        dict_values['garantia'] = garantia.value
        dict_values['n_fiscal'] = nota_fiscal.value
        dict_values['revenda'] = revenda.value
        dict_values['acessorios'] = acessorios.value
        dict_values['observacoes'] = observacoes.value
        dict_values['defeitos'] = sintomas.value
 
        c.execute(
            'INSERT INTO entrega (numero_os, data_entrega, saida, telefone, sintomas, valor_total, cliente_os,cpf_cnpj,email,modelo,endereco,bairro,cidade,marca,serial,certificado,senha,data,saida,garantia,n_fiscal,revenda,acessorios,observacoes, sintomas) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (dict_values['numero_os'], dict_values['data_entrega'], dict_values['saida'],
             dict_values['telefone'], dict_values['sintomas'], dict_values['valor_total'],dict_values['cliente_os'],
             dict_values['cpf_cnpj'],dict_values['email'], dict_values['modelo'], dict_values['endereco'],dict_values['bairro'],dict_values['cidade'],
             dict_values['marca'], dict_values['serial'],dict_values['certificado'],dict_values['senha'], dict_values['data'],dict_values['saida'],
             dict_values['garantia'],dict_values['n_fiscal'],dict_values['revenda'],dict_values['acessorios'],dict_values['observacoes'],
             dict_values['sintomas']))
        conn.commit()
        mensagem = ft.SnackBar(
            content=ft.Text("OS Salva com sucesso"),
            action='fechar'
        )
        page.show_snack_bar(mensagem)

    def gerar_codigo(e):
        try:
            codigo = gerador.proximo_codigo()
            numero_os.value = codigo
            page.update()

        except ValueError as ve:
            numero_os.value = str(ve)
            page.update()

    bnt_gerar = ft.ElevatedButton('Gerar OS', bgcolor=ft.colors.BLUE_500, color='black', on_click=gerar_codigo)
    gerador = CodeGenerator()
    numero_os = ft.TextField(label='N°-OS', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    data_entrega = ft.TextField(label='Data de  Entrada.', width=350, height=30, text_size=13.5,bgcolor=ft.colors.WHITE70)
    saida = ft.TextField(label='Data de Saída. ', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    txt_dadoscliente = ft.Text('Dados do  Cliente', weight='bold')
    cliente = ft.TextField(label='Nome do Cliente', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    endereco = ft.TextField(label='Endereço', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    cidade = ft.TextField(label='Cidade', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    bairro = ft.TextField(label='Bairro', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    cpf_cnpj = ft.TextField(label='CPF/CNPJ', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    telefone = ft.TextField(label='Whatsapp', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    email = ft.TextField(label='Email', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    txt_dadosaparelho = ft.Text('Dados do Aparelho', weight='bold')
    valor_total = ft.TextField(label='Valor', width=350, height=30, text_size=13.5,prefix_text='R$ ',bgcolor=ft.colors.WHITE70)
    modelo = ft.TextField(label='Modelo', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    marca = ft.TextField(label='Marca', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    serial = ft.TextField(label="N° Série", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    garantia = ft.TextField(label="Garantia", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    data = ft.TextField(label="Data da Compra", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    acessorios = ft.TextField(label="Acessórios", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    nota_fiscal = ft.TextField(label="N° Nota Fiscal", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    observacoes = ft.TextField(label='Observações', width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    senha_desb = ft.TextField(label="Senha", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    sintomas = ft.TextField(label="Defeitos", width=350, height=30, text_size=13.5, bgcolor=ft.colors.WHITE70)
    revenda = ft.TextField(label="Revenda", width=350, height=30, text_size=13.5,prefix_text='R$ ', bgcolor=ft.colors.WHITE70)
    bnt_finalizar = ft.ElevatedButton('Salvar OS', bgcolor=ft.colors.BLUE_600, color='black', on_click=salvar_os)
    
    def gerar_pdf(e):
        pdf_file = f"Comprovante_{numero_os.value}.pdf"  # Usar o número da OS como parte do nome
        c = canvas.Canvas(pdf_file, pagesize=A4)
        width, height = A4

        #CABEÇALHO
        c.drawImage('img/logo.jpeg', 50, height - 100, width=100, height=100)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(180, height - 50, "Recebimento de Materiais para Manutenção")

        #DATAS E NUMERO OS 
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 150, f"Numero OS: {numero_os.value}")
        c.drawString(165, height - 150, f"Data de entrega : {data_entrega.value}")
        c.drawString(350, height - 150, f"Data de saída: {saida.value}")

        #DADOS GERAIS
        c.drawString(50, height - 180, f"Cliente: {cliente.value}")
        c.drawString(50, height - 200, f"Cpf: {cpf_cnpj.value}")
        c.drawString(50, height - 220, f"Whatsapp: {telefone.value}")
        c.drawString(50, height - 240, f"Email: {email.value}")
        c.drawString(50, height - 260, f"Modelo: {modelo.value}")
        c.drawString(50, height - 280, f"Marca: {marca.value}")
        c.drawString(50, height - 300, f"Número de série: {serial.value}")
        c.drawString(50, height - 320, f"Data da Compra: {data.value}")
        c.drawString(50, height - 340, f"Acessórios: {acessorios.value}")
        c.drawString(50, height - 360, f"Sintomas: {sintomas.value}")
        c.drawString(50, height - 380, f"Senha: {senha_desb.value}")
        c.drawString(50, height - 400, f"Nota: {nota_fiscal.value}")
        c.drawString(50, height - 420, f"Observações: {observacoes.value}")
        c.drawString(50, height - 440, f"Revenda: {revenda.value}")

        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, height - 520, "Declaro estar deixando o aparelho celular indicado nesta ordem de serviço para manutenção.")
        c.drawString(50, height - 540, "A retirada do aparelho só poderá ser feita mediante a apresentação desta ordem de serviço.")
        c.drawString(50, height - 580, "Não nos responsabilizamos por SIM CARD (chip) ou cartão de memória deixados junto ao aparelho.")
        c.drawString(50, height - 600, "A garantia cobre exclusivamente o serviço realizado e é válida por 90 (noventa) ")
        c.drawString(50, height - 620, "dias a partir da data de entrega do aparelho. A garantia não se aplica em casos de mau uso do aparelho.")
        c.drawString(50, height - 660, "Assinatura: _______________________________________")
        c.drawString(50, height - 700, "FMV: ______________________________________________")
        c.save()

        mensagem = ft.SnackBar(
            content=ft.Text("Print Realizado com sucesso."),
            action='fechar'
        )
        page.show_snack_bar(mensagem)
        
    bnt_imprimir = ft.ElevatedButton('Print', bgcolor=ft.colors.BLUE_600, color='black', on_click=gerar_pdf)
    
    return ft.View(
        "/devolucao_os/devolver",
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
                            ft.Text('OS Entrega', size=25),
                        ]
                    )
                ]
            ),
            ft.Container(
                content=ft.Column(
                    controls=(
                        Row(controls=[logo, comprov_devolucao, txt_empresa]),
                        Row(controls=[bnt_gerar]),
                        Row(controls=[numero_os, data_entrega, saida]),
                        Row(controls=[txt_dadoscliente]),
                        Row(controls=[cliente, cpf_cnpj, telefone, email]),
                        Row(controls=[endereco, bairro, cidade]),
                        Row(controls=[txt_dadosaparelho]),
                        Row(controls=[modelo, marca, serial, senha_desb]),
                        Row(controls=[garantia, data, nota_fiscal, revenda]),
                        Row(controls=[acessorios, observacoes, sintomas, valor_total]),
                        Row(controls=[bnt_imprimir, bnt_finalizar])
                    )
                )
            )
        ]
    )
