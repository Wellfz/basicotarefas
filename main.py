import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import logging
from typing import Optional

import controller
import config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskManagerApp:
    """Classe principal da aplicação de gerenciamento de tarefas."""
    
    def __init__(self):
        self.root = None
        self.lista_tarefas = None
        self.entry_titulo = None
        self.entry_descricao = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Configura a interface do usuário."""
        # Inicializar BD
        try:
            controller.inicializar()
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema: {e}")
            messagebox.showerror("Erro", "Erro ao inicializar o sistema. Verifique os logs.")
            return

        # Janela principal
        self.root = ThemedTk(theme=config.WINDOW_CONFIG['theme'])
        self.root.title(config.WINDOW_CONFIG['title'])
        self.root.configure(bg=config.COLORS['background'])
        self.root.geometry(f"{config.WINDOW_CONFIG['width']}x{config.WINDOW_CONFIG['height']}")

        # Frame principal centralizado
        frame_main = tk.Frame(self.root, bg=config.COLORS['background'], padx=40, pady=40)
        frame_main.pack(expand=True)

        # Título
        tk.Label(frame_main, text=config.WINDOW_CONFIG['title'], 
                bg=config.COLORS['background'], fg=config.COLORS['text'], 
                font=config.FONTS['title']).pack(pady=(0, 20))

        # Campos de entrada
        self._create_input_fields(frame_main)
        
        # Treeview de tarefas
        self._create_task_list(frame_main)
        
        # Botões de ação
        self._create_action_buttons(frame_main)
        
        # Carregar lista ao iniciar
        self.atualizar_lista()

    def _create_input_fields(self, parent):
        """Cria os campos de entrada."""
        frame_inputs = tk.Frame(parent, bg=config.COLORS['background'])
        frame_inputs.pack(pady=10)

        tk.Label(frame_inputs, text="Título:", bg=config.COLORS['background'], 
                fg=config.COLORS['text'], font=config.FONTS['label']).grid(row=0, column=0, sticky="w")
        
        self.entry_titulo = tk.Entry(frame_inputs, width=config.INPUT_CONFIG['width'], 
                                   bg=config.COLORS['secondary'], fg=config.COLORS['text'], 
                                   insertbackground=config.COLORS['text'], 
                                   font=config.FONTS['entry'], relief=config.INPUT_CONFIG['relief'])
        self.entry_titulo.grid(row=0, column=1, padx=10, pady=5)
        self.entry_titulo.bind('<Return>', lambda e: self.adicionar_tarefa())

        tk.Label(frame_inputs, text="Descrição:", bg=config.COLORS['background'], 
                fg=config.COLORS['text'], font=config.FONTS['label']).grid(row=1, column=0, sticky="w")
        
        self.entry_descricao = tk.Entry(frame_inputs, width=config.INPUT_CONFIG['width'], 
                                      bg=config.COLORS['secondary'], fg=config.COLORS['text'], 
                                      insertbackground=config.COLORS['text'], 
                                      font=config.FONTS['entry'], relief=config.INPUT_CONFIG['relief'])
        self.entry_descricao.grid(row=1, column=1, padx=10, pady=5)
        self.entry_descricao.bind('<Return>', lambda e: self.adicionar_tarefa())

        btn_add = tk.Button(frame_inputs, text="Adicionar", command=self.adicionar_tarefa, 
                           bg=config.COLORS['accent'], fg=config.COLORS['text'], 
                           activebackground=config.COLORS['accent_hover'], 
                           font=config.FONTS['button'], relief="flat", bd=0)
        btn_add.grid(row=2, column=0, columnspan=2, pady=15)

    def _create_task_list(self, parent):
        """Cria a lista de tarefas."""
        style = ttk.Style()
        style.configure("Treeview", background=config.COLORS['secondary'], 
                       foreground=config.COLORS['text'], rowheight=25, 
                       fieldbackground=config.COLORS['secondary'])
        style.map("Treeview", background=[("selected", config.COLORS['accent'])])

        self.lista_tarefas = ttk.Treeview(parent, columns=("ID", "Título", "Descrição", "Status"), 
                                        show="headings", height=config.TABLE_CONFIG['height'])
        
        # Configurar cabeçalhos e colunas
        for col, width in config.TABLE_CONFIG['columns'].items():
            self.lista_tarefas.heading(col, text=col)
            self.lista_tarefas.column(col, width=width)

        # Configurar tags de status
        self.lista_tarefas.tag_configure("pendente", foreground=config.COLORS['error'])
        self.lista_tarefas.tag_configure("concluída", foreground=config.COLORS['success'])
        self.lista_tarefas.tag_configure("concluida", foreground=config.COLORS['success'])

        self.lista_tarefas.pack(pady=10)

    def _create_action_buttons(self, parent):
        """Cria os botões de ação."""
        frame_botoes = tk.Frame(parent, bg=config.COLORS['background'])
        frame_botoes.pack(pady=5)

        buttons = [
            ("Concluir", self.concluir_tarefa),
            ("Editar", self.editar_tarefa),
            ("Excluir", self.excluir_tarefa),
            ("Atualizar", self.atualizar_lista)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(frame_botoes, text=text, command=command,
                           bg=config.COLORS['accent'], fg=config.COLORS['text'],
                           activebackground=config.COLORS['accent_hover'],
                           font=config.FONTS['button'], relief="flat", bd=0)
            btn.grid(row=0, column=i, padx=5)

    def atualizar_lista(self):
        """Atualiza a lista de tarefas na interface."""
        try:
            # Limpar lista atual
            for item in self.lista_tarefas.get_children():
                self.lista_tarefas.delete(item)
            
            # Carregar tarefas do banco
            tarefas = controller.listar()
            
            # Inserir tarefas na lista
            for tarefa in tarefas:
                self.lista_tarefas.insert("", "end", 
                                        values=(tarefa[0], tarefa[1], tarefa[2], tarefa[3]), 
                                        tags=(tarefa[3],))
            logger.info(f"Lista atualizada com {len(tarefas)} tarefas")
            
        except Exception as e:
            logger.error(f"Erro ao atualizar lista: {e}")
            messagebox.showerror("Erro", config.MESSAGES['error_generic'])

    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa."""
        titulo = self.entry_titulo.get().strip()
        descricao = self.entry_descricao.get().strip()
        
        if not titulo:
            messagebox.showwarning("Aviso", config.MESSAGES['empty_title'])
            return
        
        try:
            controller.adicionar_tarefa(titulo, descricao)
            self.entry_titulo.delete(0, tk.END)
            self.entry_descricao.delete(0, tk.END)
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", config.MESSAGES['task_added'])
            
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            logger.error(f"Erro ao adicionar tarefa: {e}")
            messagebox.showerror("Erro", config.MESSAGES['error_generic'])

    def _get_selected_task_id(self) -> Optional[int]:
        """Obtém o ID da tarefa selecionada."""
        try:
            item = self.lista_tarefas.selection()[0]
            return int(self.lista_tarefas.item(item, "values")[0])
        except (IndexError, ValueError):
            return None

    def concluir_tarefa(self):
        """Marca uma tarefa como concluída."""
        task_id = self._get_selected_task_id()
        if not task_id:
            messagebox.showwarning("Aviso", config.MESSAGES['select_task'])
            return
        
        try:
            success = controller.concluir(task_id)
            if success:
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", config.MESSAGES['task_completed'])
            else:
                messagebox.showwarning("Aviso", "Tarefa não encontrada")
                
        except Exception as e:
            logger.error(f"Erro ao concluir tarefa: {e}")
            messagebox.showerror("Erro", config.MESSAGES['error_generic'])

    def editar_tarefa(self):
        """Abre janela para editar uma tarefa."""
        task_id = self._get_selected_task_id()
        if not task_id:
            messagebox.showwarning("Aviso", config.MESSAGES['select_task'])
            return
        
        try:
            # Buscar dados da tarefa
            tarefa = controller.buscar_tarefa(task_id)
            if not tarefa:
                messagebox.showwarning("Aviso", "Tarefa não encontrada")
                return
            
            self._open_edit_window(task_id, tarefa[1], tarefa[2], tarefa[3])
            
        except Exception as e:
            logger.error(f"Erro ao buscar tarefa para edição: {e}")
            messagebox.showerror("Erro", config.MESSAGES['error_generic'])

    def _open_edit_window(self, task_id: int, titulo_atual: str, descricao_atual: str, status_atual: str):
        """Abre janela de edição de tarefa."""
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Editar Tarefa")
        edit_win.configure(bg=config.COLORS['background'])
        edit_win.transient(self.root)
        edit_win.grab_set()

        # Centralizar janela
        edit_win.geometry("420x260")
        edit_win.resizable(False, False)
        # Centralizar colunas do grid
        edit_win.grid_columnconfigure(0, weight=1)
        edit_win.grid_columnconfigure(1, weight=1)

        tk.Label(edit_win, text="Título:", bg=config.COLORS['background'], 
                fg=config.COLORS['text'], font=config.FONTS['label']).grid(row=0, column=0, padx=10, pady=10)
        
        entry_titulo_edit = tk.Entry(edit_win, width=30, bg=config.COLORS['secondary'], 
                                   fg=config.COLORS['text'], font=config.FONTS['entry'], relief="flat")
        entry_titulo_edit.grid(row=0, column=1, padx=10, pady=10)
        entry_titulo_edit.insert(0, titulo_atual)

        tk.Label(edit_win, text="Descrição:", bg=config.COLORS['background'], 
                fg=config.COLORS['text'], font=config.FONTS['label']).grid(row=1, column=0, padx=10, pady=10)
        
        entry_descricao_edit = tk.Entry(edit_win, width=30, bg=config.COLORS['secondary'], 
                                      fg=config.COLORS['text'], font=config.FONTS['entry'], relief="flat")
        entry_descricao_edit.grid(row=1, column=1, padx=10, pady=10)
        entry_descricao_edit.insert(0, descricao_atual)

        # Campo de Status
        tk.Label(edit_win, text="Status:", bg=config.COLORS['background'], 
                fg=config.COLORS['text'], font=config.FONTS['label']).grid(row=2, column=0, padx=10, pady=10)
        
        status_values = ['pendente', 'concluida']
        # normalizar status atual (pode vir com acento)
        status_norm = 'concluida' if status_atual.lower().startswith('conclu') else 'pendente'
        status_combo = ttk.Combobox(edit_win, values=status_values, state="readonly")
        status_combo.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        status_combo.set(status_norm)

        def salvar_edicao():
            novo_titulo = entry_titulo_edit.get().strip()
            nova_descricao = entry_descricao_edit.get().strip()
            novo_status = status_combo.get().strip()
            
            if not novo_titulo:
                messagebox.showwarning("Aviso", config.MESSAGES['empty_title'])
                return
            
            try:
                success_main = controller.editar_tarefa(task_id, novo_titulo, nova_descricao)
                # Atualizar status se mudou
                success_status = True
                if novo_status and novo_status != status_norm:
                    success_status = controller.atualizar_status(task_id, novo_status)

                if success_main and success_status:
                    self.atualizar_lista()
                    edit_win.destroy()
                    messagebox.showinfo("Sucesso", config.MESSAGES['task_updated'])
                else:
                    messagebox.showwarning("Aviso", "Tarefa não encontrada")
                    
            except ValueError as e:
                messagebox.showwarning("Aviso", str(e))
            except Exception as e:
                logger.error(f"Erro ao editar tarefa: {e}")
                messagebox.showerror("Erro", config.MESSAGES['error_generic'])

        btn_salvar = tk.Button(edit_win, text="Salvar", command=salvar_edicao, 
                              bg=config.COLORS['accent'], fg=config.COLORS['text'], 
                              font=config.FONTS['button'], relief="flat", bd=0)
        btn_salvar.grid(row=3, column=0, columnspan=2, pady=(5,15))

    def excluir_tarefa(self):
        """Exclui uma tarefa após confirmação."""
        task_id = self._get_selected_task_id()
        if not task_id:
            messagebox.showwarning("Aviso", config.MESSAGES['select_task'])
            return
        
        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", config.MESSAGES['confirm_delete']):
            try:
                success = controller.deletar(task_id)
                if success:
                    self.atualizar_lista()
                    messagebox.showinfo("Sucesso", config.MESSAGES['task_deleted'])
                else:
                    messagebox.showwarning("Aviso", "Tarefa não encontrada")
                    
            except Exception as e:
                logger.error(f"Erro ao excluir tarefa: {e}")
                messagebox.showerror("Erro", config.MESSAGES['error_generic'])

    def run(self):
        """Inicia a aplicação."""
        if self.root:
            self.root.mainloop()

def main():
    """Função principal da aplicação."""
    try:
        app = TaskManagerApp()
        app.run()
    except Exception as e:
        logger.error(f"Erro fatal na aplicação: {e}")
        messagebox.showerror("Erro Fatal", "Erro crítico na aplicação. Verifique os logs.")

if __name__ == "__main__":
    main()
