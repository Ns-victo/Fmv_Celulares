import sqlite3

# Connect to SQLite database (creating it if it doesn't exist)
conn = sqlite3.connect('db/os_finalizada.db', check_same_thread=False)

def create_table():
    # Create a cursor object to interact with the database
    c = conn.cursor()
    
    # Define the SQL statement to create the table
    c.execute("""CREATE TABLE IF NOT EXISTS os_finalizada (
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
                )""")
    c.execute("PRAGMA table_info(os_finalizada)")
    colunas = [col[1] for  col  in  c.fetchall()]

    if 'data' not in  colunas:
        try:
            c.execute("ALTER TABLE  os_finalizada ADD COLUMN data TEXT")
            print("Coluna 'data' adicionada com sucesso ")
        except sqlite3.OperationalError as e:
            print(f"Erro  ao adicionar  a coluna: {e}")

    else:
        print('A coluna data já existe')
    
    # Commit changes to the database
    conn.commit()
    # Close the cursor (not closing connection here to keep it open for other operations)
    c.close()
# Call the function to create the table
create_table()

# Optionally, you can close the connection after you're done using it
conn.close()
