from database import DB_PATH
import sqlite3
from models import Produto, Venda
from datetime import datetime

class ProdutoController:
    def cadastrar_produto(self, nome, tipo, validade, quantidade, preco_compra, preco_venda):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produtos (nome, tipo, validade, quantidade, preco_compra, preco_venda)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, tipo, validade, quantidade, preco_compra, preco_venda))
        conn.commit()
        conn.close()

    def get_all_products(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        conn.close()
        return produtos

    def delete_product(self, product_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

    def get_product_id_by_name(self, nome):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))
        produto_id = cursor.fetchone()
        conn.close()
        return produto_id[0] if produto_id else None

    def get_product_by_id(self, product_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (product_id,))
        produto = cursor.fetchone()
        conn.close()
        return produto

    def get_product_name_by_id(self, product_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nome FROM produtos WHERE id = ?", (product_id,))
        produto_nome = cursor.fetchone()
        conn.close()
        return produto_nome[0] if produto_nome else None

    def update_product_quantity(self, product_id, quantidade):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produtos
            SET quantidade = ?
            WHERE id = ?
        ''', (quantidade, product_id))
        conn.commit()
        conn.close()

class VendaController:
    def registrar_venda(self, produto_id, quantidade, total):
        data = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO vendas (produto_id, quantidade, data, hora, total)
            VALUES (?, ?, ?, ?, ?)
        ''', (produto_id, quantidade, data, hora, total))
        conn.commit()
        conn.close()

    def get_all_sales(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vendas")
        vendas = cursor.fetchall()
        conn.close()
        return vendas

    def get_sales_by_date(self, data_inicial, data_final):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id, p.nome, v.quantidade, v.data, v.hora, v.total
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            WHERE v.data BETWEEN ? AND ?
        ''', (data_inicial.strftime("%Y-%m-%d"), data_final.strftime("%Y-%m-%d")))
        vendas = cursor.fetchall()
        conn.close()
        return vendas

    def apagar_todas_vendas(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vendas")
        conn.commit()
        conn.close()