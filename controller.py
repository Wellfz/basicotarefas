import model
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

def inicializar() -> None:
    """Inicializa o banco de dados."""
    try:
        model.criar_tabela()
        logger.info("Sistema inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema: {e}")
        raise

def adicionar_tarefa(titulo: str, descricao: str = "") -> int:
    """Adiciona uma nova tarefa."""
    try:
        task_id = model.adicionar_tarefa(titulo, descricao)
        logger.info(f"Tarefa adicionada via controller: ID {task_id}")
        return task_id
    except ValueError as e:
        logger.warning(f"Validação falhou ao adicionar tarefa: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao adicionar tarefa: {e}")
        raise
    
def listar() -> List[Tuple]:
    """Lista todas as tarefas."""
    try:
        return model.listar_tarefas()
    except Exception as e:
        logger.error(f"Erro ao listar tarefas: {e}")
        raise

def concluir(id: int) -> bool:
    """Marca uma tarefa como concluída."""
    try:
        return model.atualizar_status_tarefa(id, "concluida")
    except ValueError as e:
        logger.warning(f"Status inválido ao concluir tarefa {id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro ao concluir tarefa {id}: {e}")
        raise
    
def editar_tarefa(id: int, novo_titulo: str, nova_descricao: str = "") -> bool:
    """Edita uma tarefa existente."""
    try:
        return model.atualizar_tarefa(id, novo_titulo, nova_descricao)
    except ValueError as e:
        logger.warning(f"Validação falhou ao editar tarefa {id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro ao editar tarefa {id}: {e}")
        raise

def deletar(id: int) -> bool:
    """Deleta uma tarefa."""
    try:
        return model.deletar_tarefa(id)
    except Exception as e:
        logger.error(f"Erro ao deletar tarefa {id}: {e}")
        raise

def buscar_tarefa(id: int) -> Optional[Tuple]:
    """Busca uma tarefa específica por ID."""
    try:
        return model.buscar_tarefa_por_id(id)
    except Exception as e:
        logger.error(f"Erro ao buscar tarefa {id}: {e}")
        raise

