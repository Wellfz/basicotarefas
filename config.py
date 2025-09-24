"""
Configurações do sistema de tarefas.
Centraliza todas as constantes e configurações da aplicação.
"""

# Configurações de cores
COLORS = {
    'background': '#23244a',
    'secondary': '#2c2f66',
    'accent': '#6c63ff',
    'accent_hover': '#8f85ff',
    'text': '#ffffff',
    'success': '#00ff00',
    'error': '#ff0000',
    'warning': '#ffaa00'
}

# Configurações de fonte
FONTS = {
    'title': ('Segoe UI', 18, 'bold'),
    'label': ('Segoe UI', 12),
    'entry': ('Segoe UI', 12),
    'button': ('Segoe UI', 12, 'bold')
}

# Configurações da janela
WINDOW_CONFIG = {
    'title': 'Agenda de Tarefas',
    'theme': 'black',
    'width': 800,
    'height': 600
}

# Configurações da tabela
TABLE_CONFIG = {
    'height': 8,
    'columns': {
        'ID': 40,
        'Título': 150,
        'Descrição': 200,
        'Status': 100
    }
}

# Configurações de entrada
INPUT_CONFIG = {
    'width': 30,
    'relief': 'flat'
}

# Status válidos para tarefas
VALID_STATUSES = ['pendente', 'concluida', 'concluída']

# Mensagens do sistema
MESSAGES = {
    'empty_title': 'Título não pode estar vazio!',
    'select_task': 'Selecione uma tarefa para realizar esta ação!',
    'confirm_delete': 'Tem certeza que deseja excluir esta tarefa?',
    'task_added': 'Tarefa adicionada com sucesso!',
    'task_updated': 'Tarefa atualizada com sucesso!',
    'task_deleted': 'Tarefa excluída com sucesso!',
    'task_completed': 'Tarefa marcada como concluída!',
    'error_generic': 'Ocorreu um erro inesperado. Tente novamente.'
}
