import sqlite3

def adaptar_banco_de_dados():
    conn = sqlite3.connect('db/entrega.db', check_same_thread=False)
    c = conn.cursor()

    # Cria a tabela se não existir
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
            data_saida TEXT,
            sintomas TEXT
            pecas_substituidas TEXT,
            tipo_entrega TEXT        )
    """)

    # Verifica se o nome exite na coluna 
    c.execute("PRAGMA table_info(entrega)")
    colunas = [col[1] for col in c.fetchall()]

    if 'tipo_entrega' not in colunas:
        try:
            c.execute("ALTER TABLE entrega ADD COLUMN tipo_entrega TEXT")
            print("Coluna 'pecas_substituidas' adicionada com sucesso.")
        except sqlite3.OperationalError as e:
            print(f"Erro ao adicionar a coluna: {e}")
    else:
        print("A coluna 'garantia' já existe.")

    conn.commit()
    conn.close()

# Executa a função para adaptar o banco de dados
adaptar_banco_de_dados()
