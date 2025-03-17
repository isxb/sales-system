import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalisadorVendas:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Vendas")

        # Frame para filtros
        filtros_frame = ttk.Frame(root)
        filtros_frame.pack(fill="x", pady=10)

        # Filtro por data
        ttk.Label(filtros_frame, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5)
        self.data_inicial_entry = DateEntry(filtros_frame, date_pattern="dd/mm/yyyy")
        self.data_inicial_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filtros_frame, text="Data Final:").grid(row=0, column=2, padx=5, pady=5)
        self.data_final_entry = DateEntry(filtros_frame, date_pattern="dd/mm/yyyy")
        self.data_final_entry.grid(row=0, column=3, padx=5, pady=5)

        # Botão para aplicar filtros
        ttk.Button(filtros_frame, text="Analisar", command=self.analisar_vendas).grid(row=0, column=4, padx=5, pady=5)

        # Frame para gráficos
        self.graficos_frame = ttk.Frame(root)
        self.graficos_frame.pack(fill="both", expand=True)

    def analisar_vendas(self):
        # Limpa o frame de gráficos
        for widget in self.graficos_frame.winfo_children():
            widget.destroy()

        # Obtém as datas selecionadas
        data_inicial = self.data_inicial_entry.get_date()
        data_final = self.data_final_entry.get_date()

        # Conecta à database do sistema de vendas
        conn = sqlite3.connect("cantina.db")
        query = '''
            SELECT v.data, SUM(v.total) as total_vendas, SUM(v.quantidade) as total_quantidade
            FROM vendas v
            WHERE v.data BETWEEN ? AND ?
            GROUP BY v.data
        '''
        df = pd.read_sql_query(query, conn, params=(data_inicial.strftime("%Y-%m-%d"), data_final.strftime("%Y-%m-%d")))
        conn.close()

        if df.empty:
            messagebox.showinfo("Info", "Nenhuma venda encontrada no período selecionado.")
            return

        # Exibe as análises
        self.exibir_analises(df)

    def exibir_analises(self, df):
        # Converte a coluna 'data' para datetime
        df['data'] = pd.to_datetime(df['data'])

        # Gráfico de vendas ao longo do tempo
        fig1, ax1 = plt.subplots()
        df.plot(x='data', y='total_vendas', kind='line', ax=ax1, title="Vendas ao Longo do Tempo", legend=False)
        ax1.set_ylabel("Total de Vendas (R$)")
        canvas1 = FigureCanvasTkAgg(fig1, self.graficos_frame)
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        # Gráfico de quantidade de produtos vendidos
        fig2, ax2 = plt.subplots()
        df.plot(x='data', y='total_quantidade', kind='bar', ax=ax2, title="Quantidade de Produtos Vendidos", legend=False)
        ax2.set_ylabel("Quantidade Vendida")
        canvas2 = FigureCanvasTkAgg(fig2, self.graficos_frame)
        canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

        # Exibe informações textuais
        info_frame = ttk.Frame(self.graficos_frame)
        info_frame.pack(fill="x", pady=10)

        ttk.Label(info_frame, text=f"Total de Vendas no Período: R$ {df['total_vendas'].sum():.2f}").pack()
        ttk.Label(info_frame, text=f"Dia com Maior Venda: {df.loc[df['total_vendas'].idxmax(), 'data'].strftime('%d/%m/%Y')} (R$ {df['total_vendas'].max():.2f})").pack()
        ttk.Label(info_frame, text=f"Dia com Menor Venda: {df.loc[df['total_vendas'].idxmin(), 'data'].strftime('%d/%m/%Y')} (R$ {df['total_vendas'].min():.2f})").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisadorVendas(root)
    root.mainloop()