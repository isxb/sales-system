import tkinter as tk
from tkinter import ttk
from views import MainWindow
from database import create_database

if __name__ == "__main__":
    # Cria o banco de dados (se não existir)
    create_database()

    # Inicia a interface gráfica
    root = tk.Tk()

    # Define o estilo para o botão vermelho
    style = ttk.Style()
    style.configure("Red.TButton", foreground="red")

    app = MainWindow(root)
    root.mainloop()