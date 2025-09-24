import sqlite3
import logging
from typing import List, Tuple, Optional
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_NAME = "database.db"

@contextmanager
def conectar():
    """Context manager para gerenciar conexões com o banco de dados."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row 
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Erro ao conectar com o banco: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def criar_tabela() -> None:
    """Cria a tabela de tarefas se ela não existir e atualiza se necessário."""
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tarefas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    status TEXT DEFAULT 'pendente'
                )
            """)
            
            cursor.execute("PRAGMA table_info(tarefas)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'data_criacao' not in columns:
                cursor.execute("ALTER TABLE tarefas ADD COLUMN data_criacao TIMESTAMP")
                logger.info("Coluna data_criacao adicionada")
            
            if 'data_atualizacao' not in columns:
                cursor.execute("ALTER TABLE tarefas ADD COLUMN data_atualizacao TIMESTAMP")
                logger.info("Coluna data_atualizacao adicionada")
            
            cursor.execute("UPDATE tarefas SET data_criacao = datetime('now') WHERE data_criacao IS NULL")
            cursor.execute("UPDATE tarefas SET data_atualizacao = datetime('now') WHERE data_atualizacao IS NULL")
            
            conn.commit()
            logger.info("Tabela de tarefas criada/atualizada com sucesso")
    except sqlite3.Error as e:
        logger.error(f"Erro ao criar/atualizar tabela: {e}")
        raise

def adicionar_tarefa(titulo: str, descricao: str = "") -> int:
    """Adiciona uma nova tarefa ao banco de dados."""
    if not titulo or not titulo.strip():
        raise ValueError("Título não pode estar vazio")
    
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tarefas (titulo, descricao) VALUES (?, ?)",
                (titulo.strip(), descricao.strip())
            )
            conn.commit()
            task_id = cursor.lastrowid
            logger.info(f"Tarefa adicionada com ID: {task_id}")
            return task_id
    except sqlite3.Error as e:
        logger.error(f"Erro ao adicionar tarefa: {e}")
        raise

def listar_tarefas() -> List[Tuple]:
    """Lista todas as tarefas do banco de dados."""
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute("PRAGMA table_info(tarefas)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'data_criacao' in columns:
                cursor.execute("SELECT * FROM tarefas ORDER BY data_criacao DESC")
            else:
                cursor.execute("SELECT * FROM tarefas ORDER BY id DESC")
            
            tarefas = cursor.fetchall()
            logger.info(f"Listadas {len(tarefas)} tarefas")
            return tarefas
    except sqlite3.Error as e:
        logger.error(f"Erro ao listar tarefas: {e}")
        raise

def atualizar_tarefa(id: int, novo_titulo: str, nova_descricao: str = "") -> bool:
    """Atualiza uma tarefa existente."""
    if not novo_titulo or not novo_titulo.strip():
        raise ValueError("Título não pode estar vazio")
    
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute("PRAGMA table_info(tarefas)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'data_atualizacao' in columns:
                cursor.execute(
                    "UPDATE tarefas SET titulo = ?, descricao = ?, data_atualizacao = datetime('now') WHERE id = ?",
                    (novo_titulo.strip(), nova_descricao.strip(), id)
                )
            else:
                cursor.execute(
                    "UPDATE tarefas SET titulo = ?, descricao = ? WHERE id = ?",
                    (novo_titulo.strip(), nova_descricao.strip(), id)
                )
            
            conn.commit()
            rows_affected = cursor.rowcount
            if rows_affected > 0:
                logger.info(f"Tarefa {id} atualizada com sucesso")
                return True
            else:
                logger.warning(f"Tarefa {id} não encontrada para atualização")
                return False
    except sqlite3.Error as e:
        logger.error(f"Erro ao atualizar tarefa {id}: {e}")
        raise
    
def atualizar_status_tarefa(id: int, status: str) -> bool:
    """Atualiza o status de uma tarefa."""
    valid_statuses = ['pendente', 'concluida', 'concluída']
    if status not in valid_statuses:
        raise ValueError(f"Status inválido. Use um dos seguintes: {valid_statuses}")
    
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            
            cursor.execute("PRAGMA table_info(tarefas)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'data_atualizacao' in columns:
                cursor.execute(
                    "UPDATE tarefas SET status = ?, data_atualizacao = datetime('now') WHERE id = ?",
                    (status, id)
                )
            else:
                cursor.execute(
                    "UPDATE tarefas SET status = ? WHERE id = ?",
                    (status, id)
                )
            
            conn.commit()
            rows_affected = cursor.rowcount
            if rows_affected > 0:
                logger.info(f"Status da tarefa {id} atualizado para '{status}'")
                return True
            else:
                logger.warning(f"Tarefa {id} não encontrada para atualização de status")
                return False
    except sqlite3.Error as e:
        logger.error(f"Erro ao atualizar status da tarefa {id}: {e}")
        raise

def deletar_tarefa(id: int) -> bool:
    """Deleta uma tarefa do banco de dados."""
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
            conn.commit()
            rows_affected = cursor.rowcount
            if rows_affected > 0:
                logger.info(f"Tarefa {id} deletada com sucesso")
                return True
            else:
                logger.warning(f"Tarefa {id} não encontrada para exclusão")
                return False
    except sqlite3.Error as e:
        logger.error(f"Erro ao deletar tarefa {id}: {e}")
        raise

def buscar_tarefa_por_id(id: int) -> Optional[Tuple]:
    """Busca uma tarefa específica por ID."""
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id,))
            tarefa = cursor.fetchone()
            return tarefa
    except sqlite3.Error as e:
        logger.error(f"Erro ao buscar tarefa {id}: {e}")
        raise