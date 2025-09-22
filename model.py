import sqlite3

DB_NAME = "database.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'pendente'
        )
    """)
    conn.commit()
    conn.close()

def adicionar_tarefa(titulo, descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)",(titulo, descricao))
    conn.commit()
    conn.close()

def listar_tarefas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

def atualizar_tarefa(id, novo_titulo, nova_descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET titulo = ?, descricao = ? WHERE id = ?", (novo_titulo, nova_descricao, id))
    conn.commit()
    conn.close()
    
def atualizar_tarefas(id, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET status = ? WHERE id = ?", (status, id))
    conn.commit()
    conn.close()

def deletar_tarefas(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()