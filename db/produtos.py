import sqlite3
conn = sqlite3.connect("db/produtos",check_same_thread = False)

def creat_table():
    c = conn.cursor()
    c.execute(""" CREATE TABLE IF NOT EXISTS produtos(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nome_produto TEXT ,
              n_serie TEXT,
              marca TEXT,
              acessorio TEXT,
              descricao TEXT,
              cor TEXT ,
              quantidade INTEGER  ,
              preco_compra REAL ,
              preco_venda REAL ,

    ) """)

    conn.commit()

