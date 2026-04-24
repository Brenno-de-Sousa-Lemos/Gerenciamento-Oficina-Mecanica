from models.database.connection_db import get_connection

def criar_tabela_ordens():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT
        )
    """)

    conn.commit()
    conn.close()

criar_tabela_ordens()