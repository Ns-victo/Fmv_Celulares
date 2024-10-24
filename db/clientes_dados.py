import sqlite3

# Conectar ao banco de dados SQLite no diretório 'db'
conn = sqlite3.connect('db/clientes.db', check_same_thread=False)


"""def adicionar_coluna_email():
    c = conn.cursor()
    # Executar o comando ALTER TABLE para adicionar a coluna 'email'
    c.execute("ALTER TABLE clientes ADD COLUMN email TEXT")
    conn.commit()

adicionar_coluna_email()"""

def cliente_tabela():
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT,
            cpf_cnpj TEXT UNIQUE,
            telefone TEXT,
            email TEXT,
            endereco TEXT,
            bairro TEXT,
            cidade TEXT
    )""")
    conn.commit()

# Chamada da função para criar a tabela (chamada opcional, dependendo do fluxo do seu programa)
cliente_tabela()
