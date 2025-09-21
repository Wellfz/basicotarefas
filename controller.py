import model

def inicializar():
    model.criar_tabela()

def adicionar_tabela(titulo, descricao):
    model.adicionar_tarefa(titulo, descricao)

def listar():
    return model.listar_tarefas()

def concluir(id):
    model.atualizar_tarefas(id, "concluida")

def deletar(id):
    model.deletar_tarefas(id)
