import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkcalendar import DateEntry
from controllers import ProdutoController, VendaController
from datetime import datetime
from openpyxl import Workbook
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import openai  # Para integração com a API da OpenAI

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Vendas da Cantina")

        # Controllers
        self.produto_controller = ProdutoController()
        self.venda_controller = VendaController()

        # Notebook para abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Aba de Produtos
        self.produto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.produto_frame, text="Produtos")
        self.criar_aba_produtos()

        # Aba de Vendas
        self.venda_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.venda_frame, text="Vendas")
        self.criar_aba_vendas()

        # Aba de Análise de Vendas
        self.analise_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analise_frame, text="Análise de Vendas")
        self.criar_aba_analise()

        # Aba de Análise de Dados
        self.analise_dados_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.analise_dados_frame, text="Análise de Dados")
        self.criar_aba_analise_dados()

    def criar_aba_produtos(self):
        # Campos de entrada
        ttk.Label(self.produto_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.nome_entry = ttk.Entry(self.produto_frame)
        self.nome_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.produto_frame, text="Tipo:").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_entry = ttk.Entry(self.produto_frame)
        self.tipo_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.produto_frame, text="Validade:").grid(row=2, column=0, padx=5, pady=5)
        self.validade_entry = DateEntry(self.produto_frame, date_pattern="dd/mm/yyyy")
        self.validade_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.produto_frame, text="Quantidade:").grid(row=3, column=0, padx=5, pady=5)
        self.quantidade_entry = ttk.Entry(self.produto_frame)
        self.quantidade_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.produto_frame, text="Preço de Compra:").grid(row=4, column=0, padx=5, pady=5)
        self.preco_compra_entry = ttk.Entry(self.produto_frame)
        self.preco_compra_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.produto_frame, text="Preço de Venda:").grid(row=5, column=0, padx=5, pady=5)
        self.preco_venda_entry = ttk.Entry(self.produto_frame)
        self.preco_venda_entry.grid(row=5, column=1, padx=5, pady=5)

        # Botão para cadastrar produto
        ttk.Button(self.produto_frame, text="Cadastrar", command=self.cadastrar_produto).grid(row=6, column=1, pady=10)

    def cadastrar_produto(self):
        nome = self.nome_entry.get()
        tipo = self.tipo_entry.get()
        validade = self.validade_entry.get_date().strftime("%d/%m/%Y")  # Formato dd/mm/yyyy
        quantidade = self.quantidade_entry.get()
        preco_compra = self.preco_compra_entry.get()
        preco_venda = self.preco_venda_entry.get()

        if nome and tipo and validade and quantidade and preco_compra and preco_venda:
            self.produto_controller.cadastrar_produto(nome, tipo, validade, quantidade, preco_compra, preco_venda)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.atualizar_tabela_vendas()
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

    def criar_aba_vendas(self):
        # Tabela de produtos
        self.tree = ttk.Treeview(self.venda_frame, columns=("ID", "Nome", "Validade", "Preço", "Quantidade"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Validade", text="Validade")
        self.tree.heading("Preço", text="Preço")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.pack(expand=True, fill="both")

        # Configuração das cores para a validade
        self.tree.tag_configure("red", background="red")
        self.tree.tag_configure("orange", background="orange")
        self.tree.tag_configure("green", background="lightgreen")

        # Legenda para cores de validade
        legenda_frame = ttk.Frame(self.venda_frame)
        legenda_frame.pack(pady=5)

        ttk.Label(legenda_frame, text="Legenda:").pack(side="left")
        ttk.Label(legenda_frame, text="Verde: Mais de 10 dias", background="lightgreen").pack(side="left", padx=5)
        ttk.Label(legenda_frame, text="Laranja: 3 a 10 dias", background="orange").pack(side="left", padx=5)
        ttk.Label(legenda_frame, text="Vermelho: Vencido", background="red").pack(side="left", padx=5)

        # Botão para adicionar ao carrinho
        ttk.Button(self.venda_frame, text="Adicionar ao Carrinho", command=self.adicionar_ao_carrinho).pack(pady=10)

        # Botão para excluir item do estoque
        ttk.Button(self.venda_frame, text="Excluir Item", command=self.excluir_item).pack(pady=10)

        # Carrinho de compras
        self.carrinho_listbox = tk.Listbox(self.venda_frame)
        self.carrinho_listbox.pack(expand=True, fill="both", pady=10)

        # Botão para remover item do carrinho
        ttk.Button(self.venda_frame, text="Remover Item", command=self.remover_do_carrinho).pack(pady=5)

        # Botão para finalizar venda
        ttk.Button(self.venda_frame, text="Finalizar Venda", command=self.finalizar_venda).pack(pady=10)

        # Atualiza a tabela de produtos
        self.atualizar_tabela_vendas()

    def atualizar_tabela_vendas(self):
        self.tree.delete(*self.tree.get_children())
        produtos = self.produto_controller.get_all_products()
        for produto in produtos:
            id, nome, validade, preco, quantidade = produto[0], produto[1], produto[3], produto[6], produto[4]
            
            # Remove produtos com quantidade zero
            if quantidade == 0:
                self.produto_controller.delete_product(id)
                continue

            # Converte a data de dd/mm/yyyy para um objeto datetime
            try:
                data_validade = datetime.strptime(validade, "%d/%m/%Y")
                dias_restantes = (data_validade - datetime.now()).days
            except ValueError:
                # Se a data estiver em um formato inválido, considera como vencido
                dias_restantes = -1

            # Define a cor com base na validade
            if dias_restantes < 0:
                tag = "red"
            elif dias_restantes <= 3:
                tag = "orange"
            else:
                tag = "green"

            self.tree.insert("", tk.END, values=(id, nome, validade, preco, quantidade), tags=(tag,))

    def adicionar_ao_carrinho(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            id, nome, validade, preco, quantidade_disponivel = item['values']
            
            # Pergunta ao usuário a quantidade desejada
            quantidade = simpledialog.askinteger("Quantidade", f"Quantidade disponível: {quantidade_disponivel}\nDigite a quantidade desejada:", minvalue=1, maxvalue=int(quantidade_disponivel))
            
            if quantidade:
                total = float(preco) * quantidade
                self.carrinho_listbox.insert(tk.END, f"{nome} - {quantidade} unidade(s) - R$ {total:.2f}")
        else:
            messagebox.showerror("Erro", "Selecione um produto para adicionar ao carrinho.")

    def remover_do_carrinho(self):
        selected_item = self.carrinho_listbox.curselection()
        if selected_item:
            self.carrinho_listbox.delete(selected_item)
        else:
            messagebox.showerror("Erro", "Selecione um item para remover do carrinho.")

    def excluir_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            produto_id = item['values'][0]  # Obtém o ID do produto (primeira coluna na tabela)
            nome = item['values'][1]  # Obtém o nome do produto (segunda coluna na tabela)
            
            confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o produto '{nome}'?")
            if confirm:
                self.produto_controller.delete_product(produto_id)  # Passa o ID do produto
                self.atualizar_tabela_vendas()
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        else:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")

    def finalizar_venda(self):
        if self.carrinho_listbox.size() == 0:
            messagebox.showerror("Erro", "O carrinho está vazio.")
            return

        # Calcula o valor total da compra
        total_compra = 0
        produtos_vendidos = []
        for item in self.carrinho_listbox.get(0, tk.END):
            nome, quantidade, total = item.split(" - ")
            quantidade = int(quantidade.split()[0])
            total = float(total.split("R$")[1])
            total_compra += total
            produtos_vendidos.append((nome, quantidade, total))

        # Janela de confirmação
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirmar Venda")

        ttk.Label(confirm_window, text="Resumo da Venda:").pack(pady=10)
        for produto in produtos_vendidos:
            ttk.Label(confirm_window, text=f"{produto[0]} - {produto[1]} unidade(s) - R$ {produto[2]:.2f}").pack()
        ttk.Label(confirm_window, text=f"Total: R$ {total_compra:.2f}").pack(pady=10)

        ttk.Button(confirm_window, text="Confirmar", command=lambda: self.confirmar_venda(produtos_vendidos, confirm_window)).pack(pady=10)
        ttk.Button(confirm_window, text="Cancelar", command=confirm_window.destroy).pack(pady=10)

    def confirmar_venda(self, produtos_vendidos, confirm_window):
        for produto in produtos_vendidos:
            nome, quantidade, total = produto
            produto_id = self.produto_controller.get_product_id_by_name(nome)
            if produto_id:
                self.venda_controller.registrar_venda(produto_id, quantidade, total)
                # Atualiza a quantidade no estoque
                produto_info = self.produto_controller.get_product_by_id(produto_id)
                nova_quantidade = produto_info[4] - quantidade
                self.produto_controller.update_product_quantity(produto_id, nova_quantidade)
        
        self.carrinho_listbox.delete(0, tk.END)
        confirm_window.destroy()
        messagebox.showinfo("Sucesso", "Venda finalizada com sucesso!")
        self.atualizar_tabela_vendas()
        self.atualizar_tabela_analise()

    def criar_aba_analise(self):
        # Tabela de vendas
        self.analise_tree = ttk.Treeview(self.analise_frame, columns=("Venda", "Produtos", "Total"), show="headings")
        self.analise_tree.heading("Venda", text="Venda")
        self.analise_tree.heading("Produtos", text="Produtos")
        self.analise_tree.heading("Total", text="Total")
        self.analise_tree.pack(expand=True, fill="both")

        # Botão para exportar para Excel
        ttk.Button(self.analise_frame, text="Exportar para Excel", command=self.exportar_para_excel).pack(pady=10)

        # Botão para apagar dados da tabela
        self.btn_apagar_dados = ttk.Button(self.analise_frame, text="Apagar Dados", command=self.apagar_dados, style="Red.TButton")
        self.btn_apagar_dados.pack(side="left", padx=10, pady=10)

        # Atualiza a tabela de análise
        self.atualizar_tabela_analise()

    def apagar_dados(self):
        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja apagar todos os dados da tabela?")
        if confirm:
            self.venda_controller.apagar_todas_vendas()
            self.atualizar_tabela_analise()
            messagebox.showinfo("Sucesso", "Dados apagados com sucesso!")

    def atualizar_tabela_analise(self):
        self.analise_tree.delete(*self.analise_tree.get_children())
        vendas = self.venda_controller.get_all_sales()
        vendas_agrupadas = {}

        # Agrupa as vendas por ID de venda
        for venda in vendas:
            venda_id = venda[0]
            if venda_id not in vendas_agrupadas:
                vendas_agrupadas[venda_id] = {
                    "data": venda[3],
                    "hora": venda[4],
                    "produtos": [],
                    "total": 0
                }
            produto_nome = self.produto_controller.get_product_name_by_id(venda[1])
            vendas_agrupadas[venda_id]["produtos"].append(f"{produto_nome} {venda[2]} unidades")
            vendas_agrupadas[venda_id]["total"] += venda[5]

        # Insere as vendas agrupadas na tabela
        for venda_id, info in vendas_agrupadas.items():
            produtos_str = "\n".join(info["produtos"])
            self.analise_tree.insert("", tk.END, values=(
                f"Venda {venda_id} {info['data']} {info['hora']}",
                produtos_str,
                f"Valor total: R$ {info['total']:.2f}"
            ))

    def exportar_para_excel(self):
        vendas = self.venda_controller.get_all_sales()
        if not vendas:
            messagebox.showerror("Erro", "Nenhuma venda encontrada para exportar.")
            return

        # Cria um novo arquivo Excel
        wb = Workbook()
        ws = wb.active

        # Adiciona os cabeçalhos
        ws.append(["Venda", "Produtos", "Total"])

        # Adiciona os dados das vendas
        for venda in vendas:
            produto_id, quantidade, data, hora, total = venda[1], venda[2], venda[3], venda[4], venda[5]
            produto_nome = self.produto_controller.get_product_name_by_id(produto_id)
            ws.append([f"Venda {venda[0]} {data} {hora}", f"{produto_nome} {quantidade} unidades", f"R$ {total:.2f}"])

        # Abre uma janela para salvar o arquivo
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            wb.save(file_path)
            messagebox.showinfo("Sucesso", "Dados exportados para Excel com sucesso!")

    def criar_aba_analise_dados(self):
        # Frame para filtros
        filtros_frame = ttk.Frame(self.analise_dados_frame)
        filtros_frame.pack(fill="x", pady=10)

        # Filtro por data
        ttk.Label(filtros_frame, text="Data Inicial:").grid(row=0, column=0, padx=5, pady=5)
        self.data_inicial_entry = DateEntry(filtros_frame, date_pattern="dd/mm/yyyy")
        self.data_inicial_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filtros_frame, text="Data Final:").grid(row=0, column=2, padx=5, pady=5)
        self.data_final_entry = DateEntry(filtros_frame, date_pattern="dd/mm/yyyy")
        self.data_final_entry.grid(row=0, column=3, padx=5, pady=5)

        # Botão para aplicar filtros
        ttk.Button(filtros_frame, text="Aplicar Filtros", command=self.atualizar_graficos).grid(row=0, column=4, padx=5, pady=5)

        # Frame para gráficos
        self.graficos_frame = ttk.Frame(self.analise_dados_frame)
        self.graficos_frame.pack(fill="both", expand=True)

        # Frame para resumo da IA
        self.resumo_frame = ttk.Frame(self.analise_dados_frame)
        self.resumo_frame.pack(fill="x", pady=10)

        # Inicializa os gráficos
        self.atualizar_graficos()

    def atualizar_graficos(self):
        # Limpa o frame de gráficos
        for widget in self.graficos_frame.winfo_children():
            widget.destroy()

        # Obtém os dados filtrados
        data_inicial = self.data_inicial_entry.get_date()
        data_final = self.data_final_entry.get_date()
        vendas = self.venda_controller.get_sales_by_date(data_inicial, data_final)

        if not vendas:
            messagebox.showinfo("Info", "Nenhuma venda encontrada no período selecionado.")
            return

        # Cria um DataFrame com os dados
        df = pd.DataFrame(vendas, columns=["ID", "Produto", "Quantidade", "Data", "Hora", "Total"])

        # Gráfico de vendas ao longo do tempo
        fig1, ax1 = plt.subplots()
        df['Data'] = pd.to_datetime(df['Data'])
        df.groupby('Data')['Total'].sum().plot(kind='line', ax=ax1, title="Vendas ao Longo do Tempo")
        canvas1 = FigureCanvasTkAgg(fig1, self.graficos_frame)
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

        # Gráfico de distribuição por produto
        fig2, ax2 = plt.subplots()
        df.groupby('Produto')['Quantidade'].sum().plot(kind='bar', ax=ax2, title="Vendas por Produto")
        canvas2 = FigureCanvasTkAgg(fig2, self.graficos_frame)
        canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

        # Atualiza o resumo da IA
        self.gerar_resumo_ia(df)

    def gerar_resumo_ia(self, df):
        # Gera um resumo textual com base nos dados
        resumo = self.gerar_resumo_com_ia(df)
        
        # Limpa o frame de resumo
        for widget in self.resumo_frame.winfo_children():
            widget.destroy()

        # Exibe o resumo
        ttk.Label(self.resumo_frame, text="Resumo das Vendas:").pack()
        ttk.Label(self.resumo_frame, text=resumo).pack()

    def gerar_resumo_com_ia(self, df):
        # Exemplo de integração com a API da OpenAI
        openai.api_key = "SUA_CHAVE_DA_API_AQUI"  # Substitua pela sua chave da API

        # Cria um prompt com os dados
        prompt = f"Com base nos seguintes dados de vendas, gere um resumo:\n{df.to_string()}\n\nResumo:"

        # Faz a requisição à API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Modelo da OpenAI
            prompt=prompt,
            max_tokens=150
        )

        return response.choices[0].text.strip()