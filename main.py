import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk

import controller

def atualizar_lista():
    for item in lista_tarefas.get_children():
        lista_tarefas.delete(item)
    tarefas = controller.listar()
    for t in tarefas:
        lista_tarefas.insert("", "end", values=(t[0], t[1], t[2], t[3]), tags=(t[3],))

def adicionar_tarefa():
    titulo = entry_titulo.get()
    descricao = entry_descricao.get()
    if not titulo:
        messagebox.showwarning("Aviso", "Título não pode estar vazio!")
        return
    controller.adicionar_tabela(titulo, descricao)
    entry_titulo.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    atualizar_lista()

def concluir_tarefa():
    try:
        item = lista_tarefas.selection()[0]
        id = lista_tarefas.item(item, "values")[0]
        controller.concluir(int(id))
        atualizar_lista()
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para concluir!")

def excluir_tarefa():
    try:
        item = lista_tarefas.selection()[0]
        id = lista_tarefas.item(item, "values")[0]
        controller.deletar(int(id))
        atualizar_lista()
    except IndexError:
        messagebox.showwarning("Aviso", "Selecione uma tarefa para excluir!")

# Inicializar BD
controller.inicializar()

# Janela principal
root = ThemedTk(theme="black")  # Ou "equilux", "yaru", "arc", etc.
root.title("Agenda de Tarefas")
root.configure(bg="#23244a")  # Azul escuro

# Fonte moderna
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 12)
FONT_ENTRY = ("Segoe UI", 12)
FONT_BUTTON = ("Segoe UI", 12, "bold")

# Frame principal centralizado
frame_main = tk.Frame(root, bg="#23244a", padx=40, pady=40)
frame_main.pack(expand=True)

# Título
tk.Label(frame_main, text="Agenda de Tarefas", bg="#23244a", fg="#ffffff", font=FONT_TITLE).pack(pady=(0, 20))

# Campos de entrada
frame_inputs = tk.Frame(frame_main, bg="#23244a")
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Título:", bg="#23244a", fg="#ffffff", font=FONT_LABEL).grid(row=0, column=0, sticky="w")
entry_titulo = tk.Entry(frame_inputs, width=30, bg="#2c2f66", fg="#ffffff", insertbackground="#ffffff", font=FONT_ENTRY, relief="flat")
entry_titulo.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_inputs, text="Descrição:", bg="#23244a", fg="#ffffff", font=FONT_LABEL).grid(row=1, column=0, sticky="w")
entry_descricao = tk.Entry(frame_inputs, width=30, bg="#2c2f66", fg="#ffffff", insertbackground="#ffffff", font=FONT_ENTRY, relief="flat")
entry_descricao.grid(row=1, column=1, padx=10, pady=5)

btn_add = tk.Button(frame_inputs, text="Adicionar", command=adicionar_tarefa, bg="#6c63ff", fg="#ffffff", activebackground="#8f85ff", font=FONT_BUTTON, relief="flat", bd=0)
btn_add.grid(row=2, column=0, columnspan=2, pady=15)

# Treeview de tarefas
style = ttk.Style()
style.configure("Treeview", background="#2c2f66", foreground="white", rowheight=25, fieldbackground="#2c2f66")
style.map("Treeview", background=[("selected", "#6c63ff")])

lista_tarefas = ttk.Treeview(frame_main, columns=("ID", "Título", "Descrição", "Status"), show="headings", height=8)
lista_tarefas.heading("ID", text="ID")
lista_tarefas.heading("Título", text="Título")
lista_tarefas.heading("Descrição", text="Descrição")
lista_tarefas.heading("Status", text="Status")

lista_tarefas.column("ID", width=40)
lista_tarefas.column("Título", width=150)
lista_tarefas.column("Descrição", width=200)
lista_tarefas.column("Status", width=100)

lista_tarefas.tag_configure("pendente", foreground="red")
lista_tarefas.tag_configure("concluída", foreground="#00ff00")
lista_tarefas.tag_configure("concluida", foreground="#00ff00")

lista_tarefas.pack(pady=10)

# Botões de ação
frame_botoes = tk.Frame(frame_main, bg="#23244a")
frame_botoes.pack(pady=5)

btn_concluir = tk.Button(frame_botoes, text="Concluir", command=concluir_tarefa, bg="#6c63ff", fg="#ffffff", activebackground="#8f85ff", font=FONT_BUTTON, relief="flat", bd=0)
btn_concluir.grid(row=0, column=0, padx=5)

btn_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir_tarefa, bg="#6c63ff", fg="#ffffff", activebackground="#8f85ff", font=FONT_BUTTON, relief="flat", bd=0)
btn_excluir.grid(row=0, column=1, padx=5)

btn_atualizar = tk.Button(frame_botoes, text="Atualizar Lista", command=atualizar_lista, bg="#6c63ff", fg="#ffffff", activebackground="#8f85ff", font=FONT_BUTTON, relief="flat", bd=0)
btn_atualizar.grid(row=0, column=2, padx=5)

# Carregar lista ao iniciar
atualizar_lista()

# Loop principal
root.mainloop()
