import pandas as pd
import tkinter as tk
from tkinter import ttk

def cadastro_produto():
    nome_item = nome_entry.get()
    descricao_item = descricao_entry.get()
    valor_item = float(valor_entry.get())
    disponibilidade_item = disponivel_var.get()

    if nome_item and valor_item:
        try:
            novo_item = pd.DataFrame({ "Nome": [nome_item],
                                    "Descrição": [descricao_item],
                                    "Valor" : [valor_item],
                                    "Disponível" : [disponibilidade_item]
                                    })
            with open("produtos_cadastrados.csv", "a") as file:
                novo_item.to_csv(file, header=not file.tell(), index=False)
                lista_de_produtos()
                limpar()
        except ValueError:
            print("Error")
    else:
        print("Error")

def lista_de_produtos():
    try:
        produtos = pd.read_csv("produtos_cadastrados.csv")
        produtos = produtos[["Nome", "Valor"]].sort_values(by="Valor", ascending=True)
        tree.delete(*tree.get_children())
        for index, row in produtos.iterrows():
            tree.insert("", "end", values=(row["Nome"], 
                                            row["Valor"]))
    except FileNotFoundError:
        print("Nenhum produto cadastrado ainda.")

def limpar():
    nome_entry.delete(0, "end")
    descricao_entry.delete(0, "end")
    valor_entry.delete(0, "end")
    disponivel_var.setvar("Sim")

root = tk.Tk()
root.title("Listagem de Produtos")

cadastro_frame = tk.Frame(root)
cadastro_frame.pack(pady=10)

tk.Label(cadastro_frame, text="Nome do Produto").grid(row=0, column=0, padx=5, pady=5)
nome_entry = tk.Entry(cadastro_frame)
nome_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(cadastro_frame, text="Descrição").grid(row=2, column=0, padx=5, pady=5)
descricao_entry = tk.Entry(cadastro_frame)
descricao_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(cadastro_frame, text="Valor ").grid(row=4, column=0, padx=5, pady=5)
valor_entry = tk.Entry(cadastro_frame)
valor_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(cadastro_frame, text="Disponíve?").grid(row=6, column=0, padx=5, pady=5)
disponivel_var = tk.Entry(cadastro_frame)
disponivel_combobox = ttk.Combobox(cadastro_frame, textvariable=disponivel_var, values=["Sim", "Não"])
disponivel_combobox.grid(row=6, column=1, padx=5, pady=5)
disponivel_combobox.current(0)

cadastrar_btn = tk.Button(cadastro_frame, text="Cadastrar", command=cadastro_produto)
cadastrar_btn.grid(row=8, column=1, padx=5, pady=5)

lista_frame = tk.Frame(root)
lista_frame.pack()

tree = ttk.Treeview(lista_frame, columns=("Nome", "Valor"), show="headings")
tree.heading("Nome", text="Nome")
tree.heading("Valor", text="Valor")
tree.pack()

lista_de_produtos()

root.mainloop()
