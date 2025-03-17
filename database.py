import sqlite3
from pathlib import Path
from datetime import datetime

# Caminho para o banco de dados
DB_PATH = Path(__file__).parent / "cantina.db"

def create_database():
    """Cria o banco de dados e as tabelas necessárias."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            validade TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_compra REAL NOT NULL,
            preco_venda REAL NOT NULL
        )
    ''')

    # Tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')

    conn.commit()
    conn.close()

def get_all_products():
    """Retorna todos os produtos cadastrados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

def update_product_quantity(product_id, quantidade):
    """Atualiza a quantidade de um produto no estoque."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE produtos
        SET quantidade = ?
        WHERE id = ?
    ''', (quantidade, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    """Remove um produto do banco de dados."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()