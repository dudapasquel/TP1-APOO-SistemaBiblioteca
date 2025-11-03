import customtkinter as ctk
import sys
import os
from pathlib import Path
from tkinter import messagebox, simpledialog
from typing import Optional, List
import threading
sys.path.append(str(Path(__file__).parent.parent))


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

try:
    from Backend.Usuario import Usuario
    from Backend.Livro import Livro
    from Backend.Aluno import Aluno
    from Backend.Professor import Professor
    from Backend.Bibliotecario import Bibliotecario
    from Backend.Notificacao import Notificacao, TipoNotificacao, StatusNotificacao
    from Backend.Avaliacao import Avaliacao
    from Backend.Reserva import Reserva, StatusReserva
    from Backend.Emprestimo import Emprestimo
    BACKEND_DISPONIVEL = True
    print("✅ Backend disponível - Modo integrado completo")
except ImportError as e:
    print(f"⚠️ Backend não disponível: {e}")
    print("📝 Executando em modo simulação")
    BACKEND_DISPONIVEL = False

    class Livro:
        pass

    class Usuario:
        pass


class SistemaBibliotecaCompleto:
    """
    Sistema completo de biblioteca com todas as funcionalidades integradas

    Funcionalidades:
    - Seleção de tipo de usuário
    - Autenticação real com banco de dados
    - CRUD completo de livros (para bibliotecário)
    - Visualização de livros ativos/inativos
    - Interfaces específicas por tipo de usuário
    """

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Biblioteca - Completo e Integrado")
        self.root.geometry("1400x800")
        self.root.minsize(1200, 700)

        self.usuario_logado: Optional[Usuario] = None
        self.livros_atuais: List[Livro] = []
        self.incluir_inativos = False

        self.criar_tela_selecao_usuario()

    def criar_tela_selecao_usuario(self):
        """Cria a tela de seleção do tipo de usuário"""

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = ctk.CTkLabel(
            main_frame,
            text="🏛️ Sistema de Biblioteca Universitária",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        titulo.pack(pady=(40, 10))

        selecao_titulo = ctk.CTkLabel(
            main_frame,
            text="👤 Selecione seu Tipo de Usuário:",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        selecao_titulo.pack(pady=(20, 40))

        botoes_frame = ctk.CTkFrame(main_frame)
        botoes_frame.pack(pady=30)

        botoes_frame.grid_columnconfigure(0, weight=1)
        botoes_frame.grid_columnconfigure(1, weight=1)
        botoes_frame.grid_columnconfigure(2, weight=1)

        bibliotecario_btn = ctk.CTkButton(
            botoes_frame,
            text="📚\nBIBLIOTECÁRIO",
            command=lambda: self.ir_para_login("Bibliotecario"),
            width=300,
            height=120,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#2B5CE6",
            hover_color="#1E42A4"
        )
        bibliotecario_btn.grid(row=0, column=0, padx=20, pady=20)

        desc_bib = ctk.CTkLabel(
            botoes_frame,
            text="• Gerenciar acervo completo\n• Controle de usuários\n• Relatórios administrativos",
            font=ctk.CTkFont(
                size=12),
            justify="left")
        desc_bib.grid(row=1, column=0, padx=20, pady=5)

        aluno_btn = ctk.CTkButton(
            botoes_frame,
            text="🎓\nALUNO",
            command=lambda: self.ir_para_login("Aluno"),
            width=300,
            height=120,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#28A745",
            hover_color="#1E7E34"
        )
        aluno_btn.grid(row=0, column=1, padx=20, pady=20)

        desc_aluno = ctk.CTkLabel(
            botoes_frame,
            text="• Consultar catálogo\n• Solicitar empréstimos\n• Acompanhar devoluções",
            font=ctk.CTkFont(
                size=12),
            justify="left")
        desc_aluno.grid(row=1, column=1, padx=20, pady=5)

        professor_btn = ctk.CTkButton(
            botoes_frame,
            text="👨‍🏫\nPROFESSOR",
            command=lambda: self.ir_para_login("Professor"),
            width=300,
            height=120,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#DC3545",
            hover_color="#C82333"
        )
        professor_btn.grid(row=0, column=2, padx=20, pady=20)

        desc_prof = ctk.CTkLabel(
            botoes_frame,
            text="• Pesquisa avançada\n• Reservas prioritárias\n• Avaliações prioritárias",
            font=ctk.CTkFont(
                size=12),
            justify="left")
        desc_prof.grid(row=1, column=2, padx=20, pady=5)

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(pady=30, fill="x", padx=50)

        if BACKEND_DISPONIVEL:
            status_label = ctk.CTkLabel(
                info_frame,
                text="� Sistema Online - Conectado ao Banco de Dados",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#28A745"
            )
            status_label.pack(pady=15)
        else:
            status_label = ctk.CTkLabel(
                info_frame,
                text="⚠️ Sistema Offline - Modo Demonstração",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#DC3545"
            )
            status_label.pack(pady=15)

    def ir_para_login(self, tipo_usuario: str):
        """Vai para a tela de login com o tipo de usuário selecionado"""
        self.tipo_usuario_selecionado = tipo_usuario
        self.criar_tela_login()

    def criar_tela_login(self):
        """Cria a tela de login específica para o tipo de usuário"""

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(10, 0))

        voltar_btn = ctk.CTkButton(
            header_frame,
            text="← Voltar",
            command=self.criar_tela_selecao_usuario,
            width=100
        )
        voltar_btn.pack(side="left", padx=20, pady=15)

        icones = {"Bibliotecario": "📚", "Aluno": "🎓", "Professor": "👨‍🏫"}
        cores = {"Bibliotecario": "#2B5CE6",
                 "Aluno": "#28A745", "Professor": "#DC3545"}

        titulo = ctk.CTkLabel(
            main_frame,
            text=f"{icones[self.tipo_usuario_selecionado]} Login - {self.tipo_usuario_selecionado}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=cores[self.tipo_usuario_selecionado]
        )
        titulo.pack(pady=(30, 20))

        login_frame = ctk.CTkFrame(main_frame)
        login_frame.pack(pady=30)

        ctk.CTkLabel(login_frame, text="📧 Email:", font=ctk.CTkFont(
            size=16, weight="bold")).pack(pady=(30, 5))
        self.email_entry = ctk.CTkEntry(
            login_frame,
            width=400,
            height=40,
            placeholder_text="Digite seu email...",
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(pady=(0, 15))

        ctk.CTkLabel(login_frame, text="🔒 Senha:", font=ctk.CTkFont(
            size=16, weight="bold")).pack(pady=5)
        self.senha_entry = ctk.CTkEntry(
            login_frame,
            width=400,
            height=40,
            show="*",
            placeholder_text="Digite sua senha...",
            font=ctk.CTkFont(size=14)
        )
        self.senha_entry.pack(pady=(0, 25))

        login_btn = ctk.CTkButton(
            login_frame,
            text=f"🚀 Entrar como {self.tipo_usuario_selecionado}",
            command=self.fazer_login,
            width=400,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=cores[self.tipo_usuario_selecionado],
            hover_color=cores[self.tipo_usuario_selecionado]
        )
        login_btn.pack(pady=(0, 30))

        self.root.bind('<Return>', lambda event: self.fazer_login())

        if BACKEND_DISPONIVEL:
            emails = {
                "Bibliotecario": "bibliotecario@biblioteca.com",
                "Aluno": "aluno@universidade.edu",
                "Professor": "professor@universidade.edu"
            }

            if self.tipo_usuario_selecionado in emails:

                threading.Timer(0.5, lambda: self.email_entry.insert(
                    0, emails[self.tipo_usuario_selecionado])).start()

    def fazer_login(self):
        """Realiza o login com autenticação real ou simulada"""
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha email e senha!")
            return

        if BACKEND_DISPONIVEL:

            sucesso, usuario, mensagem = Usuario.autenticar(email, senha)

            if sucesso and usuario:

                if usuario.tipo_usuario != self.tipo_usuario_selecionado:
                    messagebox.showerror(
                        "Erro de Tipo",
                        f"Este usuário é do tipo '{usuario.tipo_usuario}', mas você selecionou '{self.tipo_usuario_selecionado}'.\n\nPor favor, selecione o tipo correto."
                    )
                    return

                self.usuario_logado = usuario
                self.redirecionar_por_tipo_usuario()
            else:
                messagebox.showerror("Erro de Login", mensagem)
        else:

            self.fazer_login_simulado(email, senha)

    def fazer_login_simulado(self, email: str, senha: str):
        """Simula login para modo sem backend"""
        usuarios_teste = {
            "bibliotecario@teste.com": {"senha": "bibliotecario123", "tipo": "Bibliotecario", "nome": "João Silva"},
            "aluno@teste.com": {"senha": "aluno123", "tipo": "Aluno", "nome": "Maria Santos"},
            "professor@teste.com": {"senha": "professor123", "tipo": "Professor", "nome": "Dr. Carlos Lima"}
        }

        if email in usuarios_teste and usuarios_teste[email]["senha"] == senha:
            if usuarios_teste[email]["tipo"] != self.tipo_usuario_selecionado:
                messagebox.showerror(
                    "Erro de Tipo",
                    f"Tipo de usuário incorreto. Esperado: {self.tipo_usuario_selecionado}")
                return

            self.usuario_logado = type('Usuario', (), {
                'nome': usuarios_teste[email]["nome"],
                'email': email,
                'tipo_usuario': usuarios_teste[email]["tipo"]
            })()

            self.redirecionar_por_tipo_usuario()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos!")

    def redirecionar_por_tipo_usuario(self):
        """Redireciona para a interface apropriada baseada no tipo de usuário"""
        if not self.usuario_logado:
            return

        tipo = self.usuario_logado.tipo_usuario

        if tipo == "Bibliotecario":
            self.tela_bibliotecario()
        elif tipo == "Aluno":
            self.tela_aluno()
        elif tipo == "Professor":
            self.tela_professor()
        else:
            messagebox.showerror("Erro", f"Tipo de usuário inválido: {tipo}")

    def tela_bibliotecario(self):
        """Interface completa do bibliotecário com CRUD de livros"""

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        titulo = ctk.CTkLabel(
            header_frame,
            text=f"📚 Painel do Bibliotecário - {self.usuario_logado.nome}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(side="left", padx=20, pady=15)

        logout_btn = ctk.CTkButton(
            header_frame,
            text="🚪 Logout",
            command=self.fazer_logout,
            width=100,
            fg_color="#DC3545",
            hover_color="#C82333"
        )
        logout_btn.pack(side="right", padx=20, pady=15)

        notebook = ctk.CTkTabview(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab_livros = notebook.add("Gerenciar Livros")
        self.criar_aba_livros_completa(tab_livros)

        tab_alunos = notebook.add("Alunos")
        self.criar_aba_usuarios_tipo(tab_alunos, "Aluno")

        tab_professores = notebook.add("�‍🏫 Professores")
        self.criar_aba_usuarios_tipo(tab_professores, "Professor")

        tab_bibliotecarios = notebook.add("Bibliotecários")
        self.criar_aba_usuarios_tipo(tab_bibliotecarios, "Bibliotecario")

        self.carregar_livros_completo()

    def criar_aba_livros_completa(self, parent):
        """Cria a aba completa de gerenciamento de livros"""

        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)

        titulo_frame = ctk.CTkFrame(controls_frame)
        titulo_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            titulo_frame,
            text="📚 Gerenciamento Completo de Livros",
            font=ctk.CTkFont(
                size=20,
                weight="bold")).pack(
            side="left",
            padx=10)

        self.stats_label = ctk.CTkLabel(
            titulo_frame,
            text="Carregando estatísticas...",
            font=ctk.CTkFont(
                size=12))
        self.stats_label.pack(side="right", padx=10)

        acoes_frame = ctk.CTkFrame(controls_frame)
        acoes_frame.pack(fill="x", pady=10)

        btn_frame1 = ctk.CTkFrame(acoes_frame)
        btn_frame1.pack(fill="x", pady=5)

        ctk.CTkButton(
            btn_frame1,
            text="➕ Adicionar Livro",
            command=self.adicionar_livro_completo,
            width=150,
            fg_color="#28A745",
            hover_color="#1E7E34").pack(
            side="left",
            padx=5)

        ctk.CTkButton(
            btn_frame1,
            text="✅ Ativar",
            command=self.ativar_livro_selecionado,
            width=150,
            fg_color="#28A745",
            hover_color="#1E7E34").pack(
            side="left",
            padx=5)

        ctk.CTkButton(
            btn_frame1,
            text="❌ Inativar",
            command=self.inativar_livro_selecionado,
            width=150,
            fg_color="#DC3545",
            hover_color="#C82333").pack(
            side="left",
            padx=5)

        btn_frame2 = ctk.CTkFrame(acoes_frame)
        btn_frame2.pack(fill="x", pady=5)

        ctk.CTkButton(
            btn_frame1,
            text="� Atualizar Lista",
            command=self.carregar_livros_completo,
            width=150).pack(
            side="left",
            padx=5)

        self.switch_inativos = ctk.CTkSwitch(
            btn_frame2,
            text="Mostrar Livros Inativos",
            command=self.toggle_livros_inativos,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.switch_inativos.pack(side="right", padx=10)

        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        search_label = ctk.CTkLabel(
            search_frame,
            text="🔍 Buscar Livros:",
            font=ctk.CTkFont(
                weight="bold"))
        search_label.pack(side="left", padx=10)

        self.search_entry_livros = ctk.CTkEntry(
            search_frame,
            placeholder_text="Digite título, autor, ISBN ou gênero...",
            width=300)
        self.search_entry_livros.pack(side="left", padx=(0, 10), pady=10)
        self.search_entry_livros.bind(
            "<KeyRelease>", lambda e: self.buscar_livros())

        ctk.CTkButton(
            search_frame,
            text="🔄",
            command=self.limpar_busca_livros,
            width=40).pack(
            side="left")

        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        headers = [
            "Título",
            "Autor",
            "ISBN",
            "Gênero",
            "Quantidade",
            "Disponíveis",
            "Emprestados",
            "Status",
            "Ações"]
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header,
                                 font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(
                i, weight=1 if i in [0, 1] else 0)

        self.livros_content_frame = ctk.CTkScrollableFrame(
            list_frame, height=300)
        self.livros_content_frame.pack(
            fill="both", expand=True, padx=5, pady=5)

        self.livro_selecionado = None
        self.linha_selecionada = None

    def toggle_livros_inativos(self):
        """Alterna a exibição de livros inativos"""
        self.incluir_inativos = self.switch_inativos.get()
        self.carregar_livros_completo()

    def carregar_livros_completo(self):
        """Carrega e exibe a lista completa de livros"""

        self.linha_selecionada = None
        self.livro_selecionado = None

        if hasattr(self, 'btn_toggle_status'):
            self.atualizar_botao_status()

        for widget in self.livros_content_frame.winfo_children():
            widget.destroy()

        if BACKEND_DISPONIVEL:

            self.livros_atuais = Livro.listar_todos(
                limite=1000, incluir_inativos=self.incluir_inativos)
        else:

            self.livros_atuais = self.obter_livros_simulados()

        total_livros = len(self.livros_atuais)
        ativos = len(
            [l for l in self.livros_atuais if getattr(l, 'ativo', True)])
        inativos = total_livros - ativos

        stats_texto = f"📊 Total: {total_livros} | ✅ Ativos: {ativos} | ❌ Inativos: {inativos}"
        self.stats_label.configure(text=stats_texto)

        for i, livro in enumerate(self.livros_atuais):
            self.criar_linha_livro(livro, i)

    def criar_linha_livro(self, livro: Livro, index: int):
        """Cria uma linha na tabela de livros com seleção visual"""
        row_frame = ctk.CTkFrame(self.livros_content_frame)
        row_frame.pack(fill="x", pady=1, padx=2)

        for j in range(9):
            row_frame.grid_columnconfigure(j, weight=1 if j in [0, 1] else 0)

        ativo = getattr(livro, 'ativo', True)
        cor_status = "#28A745" if ativo else "#DC3545"
        status_texto = "✅ Ativo" if ativo else "❌ Inativo"

        row_frame.bind("<Button-1>", lambda e, l=livro,
                       f=row_frame: self.selecionar_livro_visual(l, f))

        titulo_texto = livro.nome[:35] + \
            "..." if len(livro.nome) > 35 else livro.nome
        titulo_label = ctk.CTkLabel(
            row_frame, text=titulo_texto, font=ctk.CTkFont(weight="bold"))
        titulo_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")
        titulo_label.bind("<Button-1>", lambda e, l=livro,
                          f=row_frame: self.selecionar_livro_visual(l, f))

        autor_label = ctk.CTkLabel(row_frame, text=livro.autor)
        autor_label.grid(row=0, column=1, padx=5, pady=8)
        autor_label.bind("<Button-1>", lambda e, l=livro,
                         f=row_frame: self.selecionar_livro_visual(l, f))

        isbn_label = ctk.CTkLabel(row_frame, text=livro.isbn)
        isbn_label.grid(row=0, column=2, padx=5, pady=8)
        isbn_label.bind("<Button-1>", lambda e, l=livro,
                        f=row_frame: self.selecionar_livro_visual(l, f))

        genero_label = ctk.CTkLabel(row_frame, text=livro.genero)
        genero_label.grid(row=0, column=3, padx=5, pady=8)
        genero_label.bind("<Button-1>", lambda e, l=livro,
                          f=row_frame: self.selecionar_livro_visual(l, f))

        quantidade_total = getattr(livro, 'quantidade_total', 5)
        quantidade_disponivel = getattr(
            livro, 'quantidade_disponivel', quantidade_total)
        quantidade_emprestada = getattr(livro, 'quantidade_emprestada', 0)

        quantidade_label = ctk.CTkLabel(
            row_frame,
            text=str(quantidade_total),
            font=ctk.CTkFont(
                weight="bold"))
        quantidade_label.grid(row=0, column=4, padx=5, pady=8)
        quantidade_label.bind("<Button-1>", lambda e, l=livro,
                              f=row_frame: self.selecionar_livro_visual(l, f))

        disponiveis_label = ctk.CTkLabel(
            row_frame,
            text=str(quantidade_disponivel),
            text_color="#28A745")
        disponiveis_label.grid(row=0, column=5, padx=5, pady=8)
        disponiveis_label.bind("<Button-1>", lambda e, l=livro,
                               f=row_frame: self.selecionar_livro_visual(l, f))

        emprestados_label = ctk.CTkLabel(
            row_frame,
            text=str(quantidade_emprestada),
            text_color="#DC3545")
        emprestados_label.grid(row=0, column=6, padx=5, pady=8)
        emprestados_label.bind("<Button-1>", lambda e, l=livro,
                               f=row_frame: self.selecionar_livro_visual(l, f))

        status_label = ctk.CTkLabel(
            row_frame,
            text=status_texto,
            text_color=cor_status,
            font=ctk.CTkFont(
                weight="bold"))
        status_label.grid(row=0, column=7, padx=5, pady=8)
        status_label.bind("<Button-1>", lambda e, l=livro,
                          f=row_frame: self.selecionar_livro_visual(l, f))

        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=8, padx=5, pady=4)

        ctk.CTkButton(
            actions_frame,
            text="👁️",
            command=lambda: self.mostrar_detalhes_livro(livro),
            width=30,
            height=25,
            fg_color="#17A2B8",
            hover_color="#117A8B"
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            actions_frame,
            text="✏️",
            command=lambda: self.mostrar_formulario_livro(livro),
            width=30,
            height=25,
            fg_color="#FFC107",
            hover_color="#E0A800"
        ).pack(side="left", padx=2)

        if ativo:
            ctk.CTkButton(
                actions_frame,
                text="❌",
                command=lambda: self.inativar_livro(livro),
                width=30,
                height=25,
                fg_color="#DC3545",
                hover_color="#C82333"
            ).pack(side="left", padx=2)
        else:
            ctk.CTkButton(
                actions_frame,
                text="✅",
                command=lambda: self.ativar_livro(livro),
                width=30,
                height=25,
                fg_color="#28A745",
                hover_color="#1E7E34"
            ).pack(side="left", padx=2)

    def selecionar_livro_visual(self, livro: Livro, row_frame):
        """Seleciona um livro com destaque visual"""
        try:

            if hasattr(self, 'linha_selecionada') and self.linha_selecionada:
                try:
                    self.linha_selecionada.configure(
                        fg_color=["gray92", "gray14"])
                except Exception:
                    pass

            row_frame.configure(fg_color=["#E3F2FD", "#1E3A8A"])

            self.livro_selecionado = livro
            self.linha_selecionada = row_frame

            self.atualizar_botao_status()
        except Exception as e:
            print(f"Erro na seleção visual: {e}")

            self.linha_selecionada = None
            self.livro_selecionado = None

    def selecionar_usuario_visual(self, usuario, row_frame):
        """Seleciona um usuário com destaque visual"""
        try:

            if hasattr(
                    self,
                    'linha_selecionada_usuario') and self.linha_selecionada_usuario:
                try:
                    self.linha_selecionada_usuario.configure(
                        fg_color=["gray92", "gray14"])
                except Exception:
                    pass

            row_frame.configure(fg_color=["#E3F2FD", "#1E3A8A"])

            self.usuario_selecionado = usuario
            self.linha_selecionada_usuario = row_frame

        except Exception as e:
            print(f"Erro na seleção visual do usuário: {e}")
            self.linha_selecionada_usuario = None
            self.usuario_selecionado = None

    def buscar_livros(self):
        """Filtra livros com base no texto de busca"""
        texto_busca = self.search_entry_livros.get().strip().lower()

        for widget in self.livros_content_frame.winfo_children():
            widget.destroy()

        if not texto_busca:

            self.carregar_livros_completo()
            return

        if BACKEND_DISPONIVEL:
            self.livros_atuais = Livro.listar_todos(
                limite=1000, incluir_inativos=self.incluir_inativos)
        else:
            self.livros_atuais = self.obter_livros_simulados()

        livros_filtrados = []
        for livro in self.livros_atuais:

            if (texto_busca in livro.nome.lower() or
                texto_busca in livro.autor.lower() or
                texto_busca in livro.isbn.lower() or
                    texto_busca in livro.genero.lower()):
                livros_filtrados.append(livro)

        self.livros_atuais = livros_filtrados

        total_livros = len(self.livros_atuais)
        ativos = len(
            [l for l in self.livros_atuais if getattr(l, 'ativo', True)])
        inativos = total_livros - ativos

        stats_texto = f"📊 Filtrado: {total_livros} | ✅ Ativos: {ativos} | ❌ Inativos: {inativos}"
        self.stats_label.configure(text=stats_texto)

        if not livros_filtrados:
            no_data_label = ctk.CTkLabel(
                self.livros_content_frame,
                text="📭 Nenhum livro encontrado com os critérios de busca",
                font=ctk.CTkFont(size=14)
            )
            no_data_label.pack(pady=50)
        else:
            for i, livro in enumerate(livros_filtrados):
                self.criar_linha_livro(livro, i)

    def limpar_busca_livros(self):
        """Limpa a busca e recarrega todos os livros"""
        self.search_entry_livros.delete(0, 'end')
        self.carregar_livros_completo()

    def mostrar_detalhes_livro(self, livro=None):
        """Abre modal com detalhes completos do livro selecionado ou especificado"""
        livro_alvo = livro or self.livro_selecionado

        if not livro_alvo:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        detalhes_window = ctk.CTkToplevel(self.root)
        detalhes_window.title("Detalhes do Livro")
        detalhes_window.geometry("600x500")
        detalhes_window.transient(self.root)
        detalhes_window.grab_set()

        main_frame = ctk.CTkFrame(detalhes_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = ctk.CTkLabel(
            main_frame,
            text="📖 Detalhes do Livro",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        titulo.pack(pady=20)

        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)

        livro = livro_alvo
        ativo = getattr(livro, 'ativo', True)
        status_cor = "#28A745" if ativo else "#DC3545"
        status_texto = "Ativo" if ativo else "Inativo"

        quantidade_total = getattr(livro, 'quantidade_total', 6)
        disponiveis = getattr(livro, 'disponiveis', 2)
        emprestados = quantidade_total - disponiveis

        detalhes_info = [
            ("📋 ID:", str(getattr(livro, 'id', 'N/A'))),
            ("📚 Título:", livro.nome),
            ("✍️ Autor:", livro.autor),
            ("🔢 ISBN:", livro.isbn),
            ("🎭 Gênero:", livro.genero),
            ("📦 Quantidade Total:", f"{quantidade_total} exemplares"),
            ("✅ Disponíveis:", f"{disponiveis} exemplares"),
            ("📚 Emprestados:", f"{emprestados} exemplares"),
            ("📈 Status de Disponibilidade:", f"{disponiveis}/{quantidade_total} disponíveis"),
            ("📊 Status:", status_texto),
        ]

        data_cadastro = getattr(livro, 'data_cadastro', None)
        if data_cadastro:
            if hasattr(data_cadastro, 'strftime'):
                data_str = data_cadastro.strftime("%d/%m/%Y às %H:%M")
            else:
                data_str = str(data_cadastro)
            detalhes_info.append(("📅 Data de Cadastro:", data_str))

        data_atualizacao = getattr(livro, 'data_atualizacao', None)
        if data_atualizacao:
            if hasattr(data_atualizacao, 'strftime'):
                data_str = data_atualizacao.strftime("%d/%m/%Y às %H:%M")
            else:
                data_str = str(data_atualizacao)
            detalhes_info.append(("🔄 Última Atualização:", data_str))

        for i, (label, valor) in enumerate(detalhes_info):

            label_widget = ctk.CTkLabel(
                info_frame,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            label_widget.grid(row=i, column=0, sticky="w", padx=20, pady=10)

            cor_texto = None
            if label.startswith("📊"):
                cor_texto = status_cor
            elif label.startswith("✅"):
                cor_texto = "#28A745"
            elif label.startswith("�") and "Emprestados" in label:
                cor_texto = "#DC3545" if emprestados > 0 else "#28A745"
            elif label.startswith("📈"):
                cor_texto = "#28A745" if disponiveis > 0 else "#DC3545"
            elif label.startswith("📦"):
                cor_texto = "#2B5CE6"

            valor_widget = ctk.CTkLabel(
                info_frame,
                text=valor,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold" if cor_texto else "normal"),
                anchor="w",
                text_color=cor_texto)
            valor_widget.grid(row=i, column=1, sticky="w", padx=20, pady=10)

            info_frame.grid_columnconfigure(1, weight=1)

        fechar_btn = ctk.CTkButton(
            main_frame,
            text="✅ Fechar",
            command=detalhes_window.destroy,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        fechar_btn.pack(pady=20)

    def adicionar_livro_completo(self):
        """Janela para adicionar novo livro"""
        self.janela_livro(modo="adicionar")

    def editar_livro_completo(self):
        """Edita o livro selecionado"""
        if not self.livro_selecionado:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        self.janela_livro(modo="editar", livro=self.livro_selecionado)

    def mostrar_formulario_livro(self, livro):
        """Mostra o formulário de edição para um livro específico"""
        self.janela_livro(modo="editar", livro=livro)

    def ativar_livro_selecionado(self):
        """Ativa o livro selecionado"""
        if not self.livro_selecionado:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        if not BACKEND_DISPONIVEL:
            messagebox.showerror("Erro", "Backend não disponível!")
            return

        try:
            livro = Livro.buscar_por_id(self.livro_selecionado.id)
            if not livro:
                messagebox.showerror("Erro", "Livro não encontrado!")
                return

            resultado = messagebox.askyesno(
                "Confirmar Ativação",
                f"Tem certeza que deseja ativar o livro '{livro.nome}'?")

            if not resultado:
                return

            # Usar o método reativar() da classe Livro
            sucesso, mensagem = livro.reativar()
            
            if sucesso:
                self.carregar_livros_completo()
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showerror("Erro", mensagem)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ativar livro: {str(e)}")

    def inativar_livro_selecionado(self):
        """Inativa o livro selecionado"""
        if not self.livro_selecionado:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        if not BACKEND_DISPONIVEL:
            messagebox.showerror("Erro", "Backend não disponível!")
            return

        try:
            # Buscar o livro pelo ID usando a classe Livro
            livro = Livro.buscar_por_id(self.livro_selecionado.id)
            if not livro:
                messagebox.showerror("Erro", "Livro não encontrado!")
                return

            resultado = messagebox.askyesno(
                "Confirmar Inativação",
                f"Tem certeza que deseja inativar o livro '{livro.nome}'?\n\n"
                "ATENÇÃO: Livros inativos não poderão ser emprestados!")

            if not resultado:
                return

            # Verificar empréstimos ativos usando a classe Emprestimo
            from Backend.Emprestimo import Emprestimo
            emprestimos_ativos = Emprestimo.contar_emprestimos_ativos_por_livro(livro.id)
            
            if emprestimos_ativos > 0:
                messagebox.showwarning(
                    "Atenção",
                    f"Não é possível inativar este livro pois há {emprestimos_ativos} empréstimo(s) ativo(s)!\n\n"
                    "Aguarde a devolução dos exemplares emprestados.")
                return

            # Usar o método excluir() da classe Livro (que na verdade inativa)
            sucesso, mensagem = livro.excluir()
            
            if sucesso:
                self.carregar_livros_completo()
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showerror("Erro", mensagem)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inativar livro: {str(e)}")

    def janela_livro(self, modo: str, livro: Optional[Livro] = None):
        """Janela unificada para adicionar/editar livro"""
        janela = ctk.CTkToplevel(self.root)
        janela.title(
            f"{'Adicionar' if modo == 'adicionar' else 'Editar'} Livro")
        janela.geometry("500x600")
        janela.transient(self.root)
        janela.grab_set()

        main_frame = ctk.CTkFrame(janela)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        titulo = ctk.CTkLabel(
            main_frame,
            text=f"{'📝 Adicionar Novo Livro' if modo == 'adicionar' else '✏️ Editar Livro'}",
            font=ctk.CTkFont(
                size=20,
                weight="bold"))
        titulo.pack(pady=20)

        campos_frame = ctk.CTkFrame(main_frame)
        campos_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(campos_frame, text="📖 Título:", font=ctk.CTkFont(
            size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        nome_entry = ctk.CTkEntry(
            campos_frame, width=400, height=35, font=ctk.CTkFont(size=12))
        nome_entry.pack(pady=(0, 10))
        if livro:
            nome_entry.insert(0, livro.nome)

        ctk.CTkLabel(campos_frame, text="✍️ Autor:", font=ctk.CTkFont(
            size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        autor_entry = ctk.CTkEntry(
            campos_frame, width=400, height=35, font=ctk.CTkFont(size=12))
        autor_entry.pack(pady=(0, 10))
        if livro:
            autor_entry.insert(0, livro.autor)

        ctk.CTkLabel(campos_frame, text="🔢 ISBN:", font=ctk.CTkFont(
            size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        isbn_entry = ctk.CTkEntry(
            campos_frame, width=400, height=35, font=ctk.CTkFont(size=12))
        isbn_entry.pack(pady=(0, 10))
        if livro:
            isbn_entry.insert(0, livro.isbn)

        ctk.CTkLabel(campos_frame, text="🎭 Gênero:", font=ctk.CTkFont(
            size=14, weight="bold")).pack(anchor="w", pady=(10, 5))
        genero_combo = ctk.CTkComboBox(
            campos_frame,
            values=["Ficção", "Não-ficção", "Romance", "Mistério", "Fantasia",
                    "Biografia", "História", "Ciência", "Tecnologia", "Outro"],
            width=400,
            height=35,
            font=ctk.CTkFont(size=12)
        )
        genero_combo.pack(pady=(0, 20))
        if livro:
            genero_combo.set(livro.genero)

        botoes_frame = ctk.CTkFrame(campos_frame)
        botoes_frame.pack(pady=20)

        def salvar_livro():
            nome = nome_entry.get().strip()
            autor = autor_entry.get().strip()
            isbn = isbn_entry.get().strip()
            genero = genero_combo.get().strip()

            if not all([nome, autor, isbn, genero]):
                messagebox.showerror(
                    "Erro", "Todos os campos são obrigatórios!")
                return

            if BACKEND_DISPONIVEL:
                try:
                    if modo == "adicionar":
                        novo_livro = Livro(
                            nome=nome, autor=autor, isbn=isbn, genero=genero)
                        sucesso, mensagem = novo_livro.salvar()
                    else:
                        livro_atualizado = Livro(
                            id=getattr(livro, 'id', None),
                            nome=nome,
                            autor=autor,
                            isbn=isbn,
                            genero=genero
                        )
                        sucesso, mensagem = livro_atualizado.salvar()

                    if sucesso:
                        messagebox.showinfo("Sucesso", mensagem)
                        janela.destroy()
                        self.carregar_livros_completo()
                    else:
                        messagebox.showerror("Erro", mensagem)

                except Exception as e:
                    messagebox.showerror(
                        "Erro", f"Erro ao salvar livro: {str(e)}")
            else:
                messagebox.showinfo(
                    "Simulação",
                    f"Livro {'adicionado' if modo == 'adicionar' else 'editado'} com sucesso (modo simulação)")
                janela.destroy()

        ctk.CTkButton(
            botoes_frame,
            text=f"💾 {'Adicionar' if modo == 'adicionar' else 'Salvar Alterações'}",
            command=salvar_livro,
            width=150,
            height=40,
            font=ctk.CTkFont(
                size=14,
                weight="bold"),
            fg_color="#28A745",
            hover_color="#1E7E34").pack(
            side="left",
            padx=10)

        ctk.CTkButton(
            botoes_frame,
            text="❌ Cancelar",
            command=janela.destroy,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#DC3545",
            hover_color="#C82333"
        ).pack(side="left", padx=10)

    def inativar_livro(self, livro=None):
        """Inativa o livro selecionado ou especificado"""
        livro_alvo = livro or self.livro_selecionado

        if not livro_alvo:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        resposta = messagebox.askyesno(
            "Confirmar Inativação",
            f"Deseja realmente inativar o livro:\n\n'{livro_alvo.nome}'?\n\nO livro ficará indisponível para empréstimos."
        )

        if resposta:
            if BACKEND_DISPONIVEL:
                sucesso, mensagem = livro_alvo.excluir()

                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.carregar_livros_completo()
                    if livro_alvo == self.livro_selecionado:
                        self.livro_selecionado = None
                        self.linha_selecionada = None
                else:
                    messagebox.showerror("Erro", mensagem)
            else:
                messagebox.showinfo("Operação Realizada",
                                    "Livro inativado com sucesso")

    def ativar_livro(self, livro=None):
        """Reativa o livro selecionado ou especificado"""
        livro_alvo = livro or self.livro_selecionado

        if not livro_alvo:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        if getattr(livro_alvo, 'ativo', True):
            messagebox.showinfo("Informação", "Este livro já está ativo!")
            return

        resposta = messagebox.askyesno(
            "Confirmar Reativação",
            f"Deseja reativar o livro:\n\n'{livro_alvo.nome}'?"
        )

        if resposta:
            if BACKEND_DISPONIVEL:
                sucesso, mensagem = livro_alvo.reativar()

                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.carregar_livros_completo()
                    if livro_alvo == self.livro_selecionado:
                        self.livro_selecionado = None
                        self.linha_selecionada = None
                else:
                    messagebox.showerror("Erro", mensagem)
            else:
                messagebox.showinfo("Operação Realizada",
                                    "Livro reativado com sucesso")

    def atualizar_botao_status(self):
        """Atualiza o botão de status baseado no livro selecionado"""
        if not hasattr(self, 'btn_toggle_status'):
            return

        if self.livro_selecionado:
            ativo = getattr(self.livro_selecionado, 'ativo', True)
            if ativo:
                self.btn_toggle_status.configure(
                    text="🗑️ Inativar Livro",
                    fg_color="#DC3545",
                    hover_color="#C82333"
                )
            else:
                self.btn_toggle_status.configure(
                    text="🔄 Reativar Livro",
                    fg_color="#17A2B8",
                    hover_color="#138496"
                )
        else:
            self.btn_toggle_status.configure(
                text="🔄 Alterar Status",
                fg_color="#6C757D",
                hover_color="#5A6268"
            )

    def obter_livros_simulados(self):
        """Retorna dados simulados de livros"""
        return [
            type('Livro', (), {
                'id': 1, 'nome': 'Dom Casmurro', 'autor': 'Machado de Assis',
                'isbn': '978-85-359-0277-5', 'genero': 'Romance', 'ativo': True,
                'data_cadastro': '2024-01-15'
            })(),
            type('Livro', (), {
                'id': 2, 'nome': 'O Cortiço', 'autor': 'Aluísio Azevedo',
                'isbn': '978-85-359-0276-8', 'genero': 'Romance', 'ativo': False,
                'data_cadastro': '2024-01-16'
            })(),
            type('Livro', (), {
                'id': 3, 'nome': 'Iracema', 'autor': 'José de Alencar',
                'isbn': '978-85-359-0278-2', 'genero': 'Romance', 'ativo': True,
                'data_cadastro': '2024-01-17'
            })(),
        ]

    def criar_aba_usuarios_tipo(self, parent, tipo_usuario):
        """Cria a aba de gerenciamento de usuários por tipo específico"""

        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        titulos = {
            "Aluno": (
                "🎓 Gerenciamento de Alunos",
                "➕ Adicionar Aluno"),
            "Professor": (
                "👨‍🏫 Gerenciamento de Professores",
                "➕ Adicionar Professor"),
            "Bibliotecario": (
                "👨‍💼 Gerenciamento de Bibliotecários",
                "➕ Adicionar Bibliotecário")}

        titulo_texto, botao_texto = titulos.get(
            tipo_usuario, ("👥 Gerenciamento", "➕ Adicionar"))

        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)

        header_frame = ctk.CTkFrame(controls_frame)
        header_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text=titulo_texto,
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkButton(
            header_frame,
            text=botao_texto,
            command=lambda: self.mostrar_formulario_usuario(
                None,
                tipo_usuario),
            width=150,
            fg_color="#28A745",
            hover_color="#1E7E34").pack(
            side="right",
            padx=20,
            pady=15)

        search_frame = ctk.CTkFrame(controls_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            search_frame,
            text="🔍 Buscar:",
            font=ctk.CTkFont(
                size=14,
                weight="bold")).pack(
            side="left",
            padx=(
                20,
                10),
            pady=10)

        ctk.CTkButton(
            search_frame,
            text="🔄 Recarregar",
            command=lambda: self.carregar_usuarios_tipo(tipo_usuario),
            width=100,
            fg_color="#6C757D",
            hover_color="#545B62"
        ).pack(side="right", padx=20, pady=10)

        if not BACKEND_DISPONIVEL:
            info_label = ctk.CTkLabel(
                main_frame,
                text="⚠️ Funcionalidade disponível apenas com backend conectado",
                font=ctk.CTkFont(
                    size=14))
            info_label.pack(pady=50)
            return

        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True)

        if tipo_usuario == "Aluno":
            headers = [
                "Nome",
                "Email",
                "Matrícula",
                "Curso",
                "Status",
                "Ações"]
        elif tipo_usuario == "Professor":
            headers = [
                "Nome",
                "Email",
                "Matrícula",
                "Departamento",
                "Status",
                "Ações"]
        else:
            headers = ["Nome", "Email", "Status", "Ações"]

        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header,
                                 font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(
                i, weight=1 if i in [0, 1] else 0)

        content_attr = f"usuarios_{tipo_usuario.lower()}_content_frame"
        setattr(
            self,
            content_attr,
            ctk.CTkScrollableFrame(
                list_frame,
                height=300))
        getattr(
            self,
            content_attr).pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5)

        setattr(self, f"usuario_selecionado_{tipo_usuario.lower()}", None)
        setattr(self, f"linha_selecionada_{tipo_usuario.lower()}", None)

        self.carregar_usuarios_tipo(tipo_usuario)

    def carregar_usuarios_tipo(self, tipo_usuario):
        """Carrega e exibe usuários de um tipo específico"""
        if not BACKEND_DISPONIVEL:
            return

        try:
            content_frame = getattr(
                self, f"usuarios_{tipo_usuario.lower()}_content_frame")

            for widget in content_frame.winfo_children():
                widget.destroy()

            todos_usuarios = Usuario.listar_todos()
            usuarios_filtrados = [
                u for u in todos_usuarios if u.tipo_usuario == tipo_usuario]

            if hasattr(
                    self,
                    'busca_matricula_var') and self.busca_matricula_var.get().strip():
                busca = self.busca_matricula_var.get().strip().lower()
                usuarios_filtrados = [u for u in usuarios_filtrados if hasattr(
                    u, 'matricula') and u.matricula and busca in u.matricula.lower()]

            if not usuarios_filtrados:
                no_data_label = ctk.CTkLabel(
                    content_frame,
                    text=f"📭 Nenhum {tipo_usuario.lower()} encontrado",
                    font=ctk.CTkFont(size=14)
                )
                no_data_label.pack(pady=50)
                return

            for usuario in usuarios_filtrados:
                self.criar_linha_usuario_tipo(
                    usuario, tipo_usuario, content_frame)

        except Exception as e:
            print(f"Erro ao carregar usuários {tipo_usuario}: {e}")

    def criar_linha_usuario_tipo(self, usuario, tipo_usuario, content_frame):
        """Cria uma linha na tabela de usuários por tipo específico"""
        row_frame = ctk.CTkFrame(content_frame)
        row_frame.pack(fill="x", pady=1, padx=2)

        num_colunas = 4 if tipo_usuario == "Bibliotecario" else 6
        for j in range(num_colunas):
            row_frame.grid_columnconfigure(j, weight=1 if j in [0, 1] else 0)

        ativo = getattr(usuario, 'ativo', True)
        cor_status = "#28A745" if ativo else "#DC3545"
        status_texto = "✅ Ativo" if ativo else "❌ Inativo"

        nome_texto = usuario.nome[:25] + \
            "..." if len(usuario.nome) > 25 else usuario.nome
        nome_label = ctk.CTkLabel(
            row_frame,
            text=nome_texto,
            font=ctk.CTkFont(
                weight="bold"))
        nome_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")

        email_texto = usuario.email[:30] + \
            "..." if len(usuario.email) > 30 else usuario.email
        email_label = ctk.CTkLabel(row_frame, text=email_texto)
        email_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        col_index = 2

        if tipo_usuario == "Aluno":

            matricula_label = ctk.CTkLabel(
                row_frame, text=usuario.matricula or "-")
            matricula_label.grid(row=0, column=col_index, padx=5, pady=8)
            col_index += 1

            curso_label = ctk.CTkLabel(row_frame, text=usuario.curso or "-")
            curso_label.grid(row=0, column=col_index, padx=5, pady=8)
            col_index += 1

        elif tipo_usuario == "Professor":

            matricula_label = ctk.CTkLabel(
                row_frame, text=usuario.matricula or "-")
            matricula_label.grid(row=0, column=col_index, padx=5, pady=8)
            col_index += 1

            depto_label = ctk.CTkLabel(
                row_frame, text=usuario.departamento or "-")
            depto_label.grid(row=0, column=col_index, padx=5, pady=8)
            col_index += 1

        status_label = ctk.CTkLabel(
            row_frame,
            text=status_texto,
            text_color=cor_status,
            font=ctk.CTkFont(
                weight="bold"))
        status_label.grid(row=0, column=col_index, padx=5, pady=8)
        col_index += 1

        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=col_index, padx=5, pady=4)

        ctk.CTkButton(
            actions_frame,
            text="👁️",
            command=lambda: self.mostrar_detalhes_usuario(usuario),
            width=30,
            height=25,
            fg_color="#17A2B8",
            hover_color="#117A8B"
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            actions_frame,
            text="✏️",
            command=lambda: self.mostrar_formulario_usuario(
                usuario,
                tipo_usuario),
            width=30,
            height=25,
            fg_color="#FFC107",
            hover_color="#E0A800").pack(
            side="left",
            padx=2)

        if ativo:
            ctk.CTkButton(
                actions_frame,
                text="❌",
                command=lambda: self.inativar_usuario(usuario, tipo_usuario),
                width=30,
                height=25,
                fg_color="#DC3545",
                hover_color="#C82333"
            ).pack(side="left", padx=2)
        else:
            ctk.CTkButton(
                actions_frame,
                text="✅",
                command=lambda: self.ativar_usuario(usuario, tipo_usuario),
                width=30,
                height=25,
                fg_color="#28A745",
                hover_color="#1E7E34"
            ).pack(side="left", padx=2)

    def carregar_usuarios(self):
        """Carrega e exibe a lista de usuários"""
        if not BACKEND_DISPONIVEL:
            return

        try:

            for widget in self.usuarios_content_frame.winfo_children():
                widget.destroy()

            usuarios = Usuario.listar_todos(incluir_inativos=True)

            if not usuarios:
                no_data_frame = ctk.CTkFrame(self.scroll_frame_usuarios)
                no_data_frame.pack(fill="x", pady=20)
                ctk.CTkLabel(
                    no_data_frame,
                    text="📭 Nenhum usuário encontrado",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=20)
                return

            for usuario in usuarios:
                self.criar_linha_usuario(usuario)

        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao carregar usuários: {str(e)}")

    def criar_linha_usuario(self, usuario):
        """Cria uma linha na tabela de usuários com seleção visual"""
        row_frame = ctk.CTkFrame(self.usuarios_content_frame)
        row_frame.pack(fill="x", pady=1, padx=2)

        for j in range(7):
            row_frame.grid_columnconfigure(j, weight=1 if j in [0, 1] else 0)

        ativo = getattr(usuario, 'ativo', True)
        cor_status = "#28A745" if ativo else "#DC3545"
        status_texto = "✅ Ativo" if ativo else "❌ Inativo"

        row_frame.bind("<Button-1>", lambda e, u=usuario,
                       f=row_frame: self.selecionar_usuario_visual(u, f))

        nome_texto = usuario.nome[:25] + \
            "..." if len(usuario.nome) > 25 else usuario.nome
        nome_label = ctk.CTkLabel(
            row_frame, text=nome_texto, font=ctk.CTkFont(weight="bold"))
        nome_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")
        nome_label.bind("<Button-1>", lambda e, u=usuario,
                        f=row_frame: self.selecionar_usuario_visual(u, f))

        email_texto = usuario.email[:30] + \
            "..." if len(usuario.email) > 30 else usuario.email
        email_label = ctk.CTkLabel(row_frame, text=email_texto)
        email_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        email_label.bind("<Button-1>", lambda e, u=usuario,
                         f=row_frame: self.selecionar_usuario_visual(u, f))

        tipo_emoji = {
            'Bibliotecario': '👨‍💼',
            'Professor': '👨‍🏫',
            'Aluno': '🎓'
        }.get(usuario.tipo_usuario, '👤')
        tipo_display = f"{tipo_emoji} {usuario.tipo_usuario}"
        tipo_label = ctk.CTkLabel(row_frame, text=tipo_display)
        tipo_label.grid(row=0, column=2, padx=5, pady=8)
        tipo_label.bind("<Button-1>", lambda e, u=usuario,
                        f=row_frame: self.selecionar_usuario_visual(u, f))

        matricula = usuario.matricula or "-"
        matricula_label = ctk.CTkLabel(row_frame, text=matricula)
        matricula_label.grid(row=0, column=3, padx=5, pady=8)
        matricula_label.bind("<Button-1>", lambda e, u=usuario,
                             f=row_frame: self.selecionar_usuario_visual(u, f))

        curso_depto = ""
        if usuario.tipo_usuario == 'Aluno' and usuario.curso:
            curso_depto = usuario.curso[:15] + \
                "..." if len(usuario.curso) > 15 else usuario.curso
        elif usuario.tipo_usuario == 'Professor' and usuario.departamento:
            curso_depto = usuario.departamento[:15] + "..." if len(
                usuario.departamento) > 15 else usuario.departamento
        else:
            curso_depto = "-"

        curso_label = ctk.CTkLabel(row_frame, text=curso_depto)
        curso_label.grid(row=0, column=4, padx=5, pady=8)
        curso_label.bind("<Button-1>", lambda e, u=usuario,
                         f=row_frame: self.selecionar_usuario_visual(u, f))

        status_label = ctk.CTkLabel(
            row_frame,
            text=status_texto,
            text_color=cor_status,
            font=ctk.CTkFont(
                weight="bold"))
        status_label.grid(row=0, column=5, padx=5, pady=8)
        status_label.bind("<Button-1>", lambda e, u=usuario,
                          f=row_frame: self.selecionar_usuario_visual(u, f))

        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=6, padx=5, pady=4)

        ctk.CTkButton(
            actions_frame,
            text="👁️",
            command=lambda: self.mostrar_detalhes_usuario(usuario),
            width=30,
            height=25,
            fg_color="#17A2B8",
            hover_color="#117A8B"
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            actions_frame,
            text="✏️",
            command=lambda: self.mostrar_formulario_usuario(usuario),
            width=30,
            height=25,
            fg_color="#FFC107",
            hover_color="#E0A800"
        ).pack(side="left", padx=2)

        if usuario.ativo:
            ctk.CTkButton(
                actions_frame,
                text="🚫",
                command=lambda: self.inativar_usuario(usuario),
                width=30,
                height=25,
                fg_color="#DC3545",
                hover_color="#C82333"
            ).pack(side="left", padx=2)
        else:
            ctk.CTkButton(
                actions_frame,
                text="✅",
                command=lambda: self.ativar_usuario(usuario),
                width=30,
                height=25,
                fg_color="#28A745",
                hover_color="#1E7E34"
            ).pack(side="left", padx=2)

    def mostrar_formulario_usuario(self, usuario=None, tipo_predefinido=None):
        """Mostra o formulário para adicionar/editar usuário"""

        modal = ctk.CTkToplevel(self.root)
        modal.title(
            "➕ Adicionar Usuário" if not usuario else "✏️ Editar Usuário")
        modal.geometry("500x650")
        modal.transient(self.root)
        modal.grab_set()
        modal.resizable(False, False)

        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (500 // 2)
        y = (modal.winfo_screenheight() // 2) - (650 // 2)
        modal.geometry(f"500x650+{x}+{y}")

        main_frame = ctk.CTkFrame(modal)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = "➕ Adicionar Novo Usuário" if not usuario else f"✏️ Editar Usuário: {usuario.nome}"
        ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 20))

        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        nome_var = ctk.StringVar(value=usuario.nome if usuario else "")
        email_var = ctk.StringVar(value=usuario.email if usuario else "")
        senha_var = ctk.StringVar()
        tipo_var = ctk.StringVar(
            value=usuario.tipo_usuario if usuario else (
                tipo_predefinido or "Aluno"))
        matricula_var = ctk.StringVar(
            value=usuario.matricula if usuario and usuario.matricula else "")
        curso_var = ctk.StringVar(
            value=usuario.curso if usuario and usuario.curso else "")
        departamento_var = ctk.StringVar(
            value=usuario.departamento if usuario and usuario.departamento else "")

        y_pos = 20

        ctk.CTkLabel(
            form_frame,
            text="Nome Completo:",
            font=ctk.CTkFont(
                weight="bold")).pack(
            anchor="w",
            padx=20,
            pady=(
                y_pos,
                5))
        nome_entry = ctk.CTkEntry(form_frame, textvariable=nome_var, height=35)
        nome_entry.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            form_frame,
            text="Email:",
            font=ctk.CTkFont(
                weight="bold")).pack(
            anchor="w",
            padx=20,
            pady=(
                0,
                5))
        email_entry = ctk.CTkEntry(
            form_frame, textvariable=email_var, height=35)
        email_entry.pack(fill="x", padx=20, pady=(0, 15))

        senha_label = "Nova Senha:" if usuario else "Senha:"
        ctk.CTkLabel(
            form_frame,
            text=senha_label,
            font=ctk.CTkFont(
                weight="bold")).pack(
            anchor="w",
            padx=20,
            pady=(
                0,
                5))
        senha_entry = ctk.CTkEntry(
            form_frame,
            textvariable=senha_var,
            show="*",
            height=35)
        senha_entry.pack(fill="x", padx=20, pady=(0, 15))

        if usuario:
            ctk.CTkLabel(
                form_frame,
                text="(Deixe em branco para manter a senha atual)",
                font=ctk.CTkFont(
                    size=10),
                text_color="gray").pack(
                anchor="w",
                padx=20,
                pady=(
                    0,
                    10))

        ctk.CTkLabel(
            form_frame,
            text="Tipo de Usuário:",
            font=ctk.CTkFont(
                weight="bold")).pack(
            anchor="w",
            padx=20,
            pady=(
                0,
                5))
        tipo_combo = ctk.CTkComboBox(
            form_frame,
            variable=tipo_var,
            values=["Aluno", "Professor", "Bibliotecario"],
            height=35,
            state="readonly"
        )
        tipo_combo.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            form_frame,
            text="Matrícula:",
            font=ctk.CTkFont(
                weight="bold")).pack(
            anchor="w",
            padx=20,
            pady=(
                0,
                5))
        matricula_readonly = usuario is not None and hasattr(
            usuario, 'matricula') and usuario.matricula
        matricula_entry = ctk.CTkEntry(
            form_frame,
            textvariable=matricula_var,
            height=35,
            state="disabled" if matricula_readonly else "normal")
        matricula_entry.pack(fill="x", padx=20, pady=(0, 15))

        campos_especificos_frame = ctk.CTkFrame(
            form_frame, fg_color="transparent")
        campos_especificos_frame.pack(fill="x", padx=20, pady=(0, 15))

        curso_label = ctk.CTkLabel(
            campos_especificos_frame,
            text="Curso:",
            font=ctk.CTkFont(
                weight="bold"))
        curso_entry = ctk.CTkEntry(
            campos_especificos_frame,
            textvariable=curso_var,
            height=35)

        depto_label = ctk.CTkLabel(
            campos_especificos_frame,
            text="Departamento:",
            font=ctk.CTkFont(
                weight="bold"))

        depto_readonly = usuario is not None and usuario.tipo_usuario == "Professor"
        depto_entry = ctk.CTkEntry(
            campos_especificos_frame,
            textvariable=departamento_var,
            height=35,
            state="disabled" if depto_readonly else "normal")

        def atualizar_campos_especificos(*args):

            for widget in campos_especificos_frame.winfo_children():
                widget.pack_forget()

            tipo_selecionado = tipo_var.get()
            if tipo_selecionado == "Aluno":
                curso_label.pack(anchor="w", pady=(0, 5))
                curso_entry.pack(fill="x", pady=(0, 10))
            elif tipo_selecionado == "Professor":
                depto_label.pack(anchor="w", pady=(0, 5))
                depto_entry.pack(fill="x", pady=(0, 10))

        tipo_var.trace("w", atualizar_campos_especificos)
        atualizar_campos_especificos()

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 10))

        def salvar_usuario():
            try:

                if not nome_var.get().strip():
                    messagebox.showerror("Erro", "Nome é obrigatório")
                    return

                if not email_var.get().strip():
                    messagebox.showerror("Erro", "Email é obrigatório")
                    return

                if not usuario and not senha_var.get().strip():
                    messagebox.showerror(
                        "Erro", "Senha é obrigatória para novos usuários")
                    return

                tipo_selecionado = tipo_var.get()
                if tipo_selecionado in [
                        "Aluno", "Professor"] and not matricula_var.get().strip():
                    messagebox.showerror(
                        "Erro", f"{tipo_selecionado} deve ter matrícula")
                    return

                if tipo_selecionado == "Aluno" and not curso_var.get().strip():
                    messagebox.showerror("Erro", "Aluno deve ter curso")
                    return

                if tipo_selecionado == "Professor" and not departamento_var.get().strip():
                    messagebox.showerror(
                        "Erro", "Professor deve ter departamento")
                    return

                if usuario:

                    usuario.nome = nome_var.get().strip()
                    usuario.email = email_var.get().strip()
                    if senha_var.get().strip():
                        usuario.senha = senha_var.get().strip()
                    usuario._tipo_usuario = tipo_selecionado
                    usuario.matricula = matricula_var.get().strip() or None
                    usuario.curso = curso_var.get().strip() or None
                    usuario.departamento = departamento_var.get().strip() or None

                    sucesso, mensagem = usuario.salvar()
                else:

                    if tipo_selecionado == "Aluno":
                        novo_usuario = Aluno(
                            nome=nome_var.get().strip(),
                            email=email_var.get().strip(),
                            senha=senha_var.get().strip(),
                            matricula=matricula_var.get().strip(),
                            curso=curso_var.get().strip()
                        )
                    elif tipo_selecionado == "Professor":
                        novo_usuario = Professor(
                            nome=nome_var.get().strip(),
                            email=email_var.get().strip(),
                            senha=senha_var.get().strip(),
                            matricula=matricula_var.get().strip(),
                            departamento=departamento_var.get().strip()
                        )
                    elif tipo_selecionado == "Bibliotecario":
                        novo_usuario = Bibliotecario(
                            nome=nome_var.get().strip(),
                            email=email_var.get().strip(),
                            senha=senha_var.get().strip()
                        )

                    sucesso, mensagem = novo_usuario.salvar()

                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    modal.destroy()
                    self.carregar_usuarios()
                else:
                    messagebox.showerror("Erro", mensagem)

            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao salvar usuário: {str(e)}")

        ctk.CTkButton(
            buttons_frame,
            text="💾 Salvar",
            command=salvar_usuario,
            width=120,
            height=35,
            fg_color="#28A745",
            hover_color="#1E7E34"
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=modal.destroy,
            width=120,
            height=35,
            fg_color="#6C757D",
            hover_color="#545B62"
        ).pack(side="right")

        nome_entry.focus_set()

    def mostrar_detalhes_usuario(self, usuario):
        """Mostra os detalhes completos do usuário"""

        modal = ctk.CTkToplevel(self.root)
        modal.title(f"👁️ Detalhes do Usuário: {usuario.nome}")
        modal.geometry("450x500")
        modal.transient(self.root)
        modal.grab_set()
        modal.resizable(False, False)

        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (450 // 2)
        y = (modal.winfo_screenheight() // 2) - (500 // 2)
        modal.geometry(f"450x500+{x}+{y}")

        main_frame = ctk.CTkFrame(modal)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tipo_emoji = {
            'Bibliotecario': '👨‍💼',
            'Professor': '👨‍🏫',
            'Aluno': '🎓'
        }.get(usuario.tipo_usuario, '👤')

        ctk.CTkLabel(
            main_frame,
            text=f"{tipo_emoji} Detalhes do {usuario.tipo_usuario}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 20))

        info_frame = ctk.CTkScrollableFrame(main_frame, height=350)
        info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        status_cor = "#28A745" if usuario.ativo else "#DC3545"
        status_texto = "✅ Usuário Ativo" if usuario.ativo else "❌ Usuário Inativo"

        informacoes = [
            ("👤 Nome", usuario.nome),
            ("📧 Email", usuario.email),
            ("🏷️ Tipo", f"{tipo_emoji} {usuario.tipo_usuario}"),
            ("🆔 ID Sistema", f"#{usuario.id}"),
            ("📊 Status", status_texto),
        ]

        if usuario.matricula:
            informacoes.insert(-1, ("🎫 Matrícula", usuario.matricula))

        if usuario.tipo_usuario == "Aluno" and usuario.curso:
            informacoes.insert(-1, ("🎓 Curso", usuario.curso))
        elif usuario.tipo_usuario == "Professor" and usuario.departamento:
            informacoes.insert(-1, ("🏢 Departamento", usuario.departamento))

        if usuario.data_cadastro:
            informacoes.append(
                ("📅 Cadastrado em", usuario.data_cadastro.strftime("%d/%m/%Y às %H:%M")))

        if usuario.data_atualizacao:
            informacoes.append(
                ("🔄 Última atualização",
                 usuario.data_atualizacao.strftime("%d/%m/%Y às %H:%M")))

        for label, valor in informacoes:

            info_item_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            info_item_frame.pack(fill="x", pady=5)

            label_widget = ctk.CTkLabel(
                info_item_frame,
                text=label + ":",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            label_widget.pack(anchor="w", padx=10, pady=2)

            cor_texto = status_cor if label.startswith("📊") else None

            valor_widget = ctk.CTkLabel(
                info_item_frame,
                text=valor,
                font=ctk.CTkFont(size=12),
                anchor="w",
                text_color=cor_texto
            )
            valor_widget.pack(anchor="w", padx=20, pady=2)

        ctk.CTkButton(
            main_frame,
            text="❌ Fechar",
            command=modal.destroy,
            width=120,
            height=35,
            fg_color="#6C757D",
            hover_color="#545B62"
        ).pack(pady=(0, 10))

    def inativar_usuario(self, usuario, tipo_usuario=None):
        """Inativa um usuário"""
        resposta = messagebox.askyesno(
            "Confirmar Inativação",
            f"Tem certeza que deseja inativar o usuário:\n\n{usuario.nome}\n{usuario.email}\n\nO usuário não poderá mais fazer login."
        )

        if resposta:
            try:
                sucesso, mensagem = usuario.excluir()

                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    if tipo_usuario:
                        self.carregar_usuarios_tipo(tipo_usuario)
                    else:
                        self.carregar_usuarios()
                else:
                    messagebox.showerror("Erro", mensagem)

            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao inativar usuário: {str(e)}")

    def ativar_usuario(self, usuario, tipo_usuario=None):
        """Ativa um usuário inativo"""
        if not BACKEND_DISPONIVEL:
            messagebox.showerror("Erro", "Backend não disponível!")
            return

        resposta = messagebox.askyesno(
            "Confirmar Ativação",
            f"Tem certeza que deseja ativar o usuário:\n\n{usuario.nome}\n{usuario.email}")

        if resposta:
            try:
                sucesso, mensagem = usuario.ativar()
                
                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    if tipo_usuario:
                        self.carregar_usuarios_tipo(tipo_usuario)
                    else:
                        self.carregar_usuarios()
                else:
                    messagebox.showerror("Erro", mensagem)

            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao ativar usuário: {str(e)}")

    def tela_aluno(self):
        """Interface específica do aluno"""
        self.tela_usuario_comum("🎓 Painel do Aluno", "aluno")

    def tela_professor(self):
        """Interface específica do professor"""
        self.tela_usuario_comum("👨‍🏫 Painel do Professor", "professor")

    def tela_usuario_comum(self, titulo: str, tipo: str):
        """Interface completa para aluno e professor com todas as funcionalidades"""

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(
            header_frame,
            text=f"{titulo} - {self.usuario_logado.nome}",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkButton(
            header_frame,
            text="🚪 Logout",
            command=self.fazer_logout,
            width=100,
            fg_color="#DC3545",
            hover_color="#C82333"
        ).pack(side="right", padx=20, pady=15)

        if BACKEND_DISPONIVEL:
            self.verificar_mostrar_alertas_atraso()

        notebook = ctk.CTkTabview(main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        tab_emprestimos = notebook.add("📚 Meus Empréstimos")
        self.criar_aba_meus_emprestimos(tab_emprestimos)

        tab_catalogo = notebook.add("🔍 Catálogo de Livros")
        self.criar_aba_catalogo_livros(tab_catalogo, tipo)

        tab_avaliacoes = notebook.add("⭐ Minhas Avaliações")
        self.criar_aba_avaliacoes_usuario(tab_avaliacoes)

    def verificar_mostrar_alertas_atraso(self):
        """Verifica e exibe alertas para empréstimos em atraso - APENAS dados reais"""
        if not BACKEND_DISPONIVEL:
            return

        try:
            from Backend.Emprestimo import Emprestimo
            from Backend.Notificacao import Notificacao, TipoNotificacao

            emprestimos_atrasados = Emprestimo.verificar_emprestimos_atrasados(
                self.usuario_logado.id)

            if emprestimos_atrasados:

                for emp in emprestimos_atrasados:
                    titulo = f"📚 Livro em Atraso: {emp['livro_titulo']}"
                    mensagem = f"O livro '{emp['livro_titulo']}' do autor {emp['livro_autor']} está {emp['dias_atraso']} dia(s) em atraso. Por favor, devolva o quanto antes para evitar multas."

                    Notificacao.criar_notificacao_sistema(
                        usuario_id=self.usuario_logado.id,
                        titulo=titulo,
                        mensagem=mensagem,
                        livro_id=None
                    )

                total_atraso = len(emprestimos_atrasados)
                livros_atrasados = ", ".join(
                    [f"'{emp['livro_titulo']}'" for emp in emprestimos_atrasados[:3]])
                if len(emprestimos_atrasados) > 3:
                    livros_atrasados += f" e mais {len(emprestimos_atrasados) - 3} livro(s)"

                messagebox.showwarning(
                    "⚠️ Empréstimos em Atraso",
                    f"Você possui {total_atraso} empréstimo(s) em atraso:\n\n{livros_atrasados}\n\nPor favor, proceda com as devoluções o quanto antes para evitar multas."
                )

        except Exception as e:
            print(f"Erro ao verificar alertas de atraso: {e}")

    def criar_aba_meus_emprestimos(self, parent):
        """Cria aba com histórico de empréstimos do usuário"""

        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        titulo_frame = ctk.CTkFrame(main_frame)
        titulo_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            titulo_frame,
            text="📚 Histórico de Empréstimos",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkButton(
            titulo_frame,
            text="🔄 Atualizar",
            command=lambda: self.carregar_historico_emprestimos(content_frame),
            width=100,
            fg_color="#6C757D",
            hover_color="#545B62"
        ).pack(side="right", padx=20, pady=15)

        if not BACKEND_DISPONIVEL:
            ctk.CTkLabel(
                main_frame,
                text="⚠️ Funcionalidade disponível apenas com backend conectado",
                font=ctk.CTkFont(
                    size=14)).pack(
                pady=50)
            return

        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True)

        headers = [
            "Título do Livro",
            "Autor",
            "Data Empréstimo",
            "Data Devolução",
            "Status"]
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(
                    weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(i, weight=1)

        content_frame = ctk.CTkScrollableFrame(list_frame, height=350)
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.carregar_historico_emprestimos(content_frame)

    def carregar_historico_emprestimos(self, content_frame):
        """Carrega e exibe o histórico de empréstimos do usuário - APENAS dados reais"""

        for widget in content_frame.winfo_children():
            widget.destroy()

        if not BACKEND_DISPONIVEL:
            ctk.CTkLabel(
                content_frame,
                text="❌ Sistema offline - Backend não disponível",
                font=ctk.CTkFont(size=14),
                text_color="#DC3545"
            ).pack(pady=50)
            return

        try:
            from Backend.Emprestimo import Emprestimo

            historico = Emprestimo.obter_historico_usuario_completo(
                self.usuario_logado.id)

            if not historico:

                info_frame = ctk.CTkFrame(content_frame)
                info_frame.pack(pady=50, padx=20, fill="x")

                ctk.CTkLabel(
                    info_frame,
                    text="� Nenhum Empréstimo Encontrado",
                    font=ctk.CTkFont(size=18, weight="bold")
                ).pack(pady=(20, 10))

                ctk.CTkLabel(
                    info_frame,
                    text="Você ainda não possui empréstimos registrados.\nVisite a aba 'Catálogo de Livros' para fazer reservas!",
                    font=ctk.CTkFont(
                        size=14),
                    justify="center").pack(
                    pady=(
                        0,
                        20))
                return

            total = len(historico)
            ativos = len([h for h in historico if h['status'] != 'Devolvido'])
            devolvidos = total - ativos
            atrasados = len(
                [h for h in historico if h['status_visual'] == 'atrasado'])

            stats_frame = ctk.CTkFrame(content_frame)
            stats_frame.pack(fill="x", pady=(0, 10), padx=5)

            ctk.CTkLabel(
                stats_frame,
                text=f"📊 Total: {total} | 📚 Ativos: {ativos} | ✅ Devolvidos: {devolvidos} | 🔴 Atrasados: {atrasados}",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold")).pack(
                pady=10)

            for emprestimo in historico:
                self.criar_linha_emprestimo_usuario(content_frame, emprestimo)

        except Exception as e:
            print(f"❌ Erro ao carregar histórico: {e}")
            ctk.CTkLabel(
                content_frame,
                text=f"❌ Erro ao conectar com banco de dados\nDetalhes: {str(e)}",
                font=ctk.CTkFont(
                    size=14),
                text_color="#DC3545").pack(
                pady=50)

    def criar_linha_emprestimo_usuario(self, parent, emprestimo):
        """Cria uma linha do histórico de empréstimos"""

        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", pady=2, padx=2)

        for i in range(6):
            row_frame.grid_columnconfigure(i, weight=1 if i < 2 else 0)

        titulo_label = ctk.CTkLabel(row_frame, text=emprestimo['livro_titulo'][:30] + "..." if len(
            emprestimo['livro_titulo']) > 30 else emprestimo['livro_titulo'], font=ctk.CTkFont(weight="bold"))
        titulo_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")

        autor_label = ctk.CTkLabel(row_frame, text=emprestimo['livro_autor'])
        autor_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        data_emp = emprestimo['data_emprestimo'].strftime(
            "%d/%m/%Y") if emprestimo['data_emprestimo'] else "-"
        data_emp_label = ctk.CTkLabel(row_frame, text=data_emp)
        data_emp_label.grid(row=0, column=2, padx=5, pady=8)

        if emprestimo['data_devolucao']:
            data_dev = emprestimo['data_devolucao'].strftime("%d/%m/%Y")
        elif emprestimo['data_devolucao_prevista']:
            data_dev = f"Até {emprestimo['data_devolucao_prevista'].strftime('%d/%m/%Y')}"
        else:
            data_dev = "-"
        data_dev_label = ctk.CTkLabel(row_frame, text=data_dev)
        data_dev_label.grid(row=0, column=3, padx=5, pady=8)

        status_text = f"{emprestimo['icone_status']} {emprestimo['status']}"
        cores_status = {
            "blue": "#007BFF",
            "green": "#28A745",
            "yellow": "#FFC107",
            "red": "#DC3545",
            "gray": "#6C757D"
        }
        cor = cores_status.get(emprestimo['cor_status'], "#000000")

        status_label = ctk.CTkLabel(
            row_frame,
            text=status_text,
            text_color=cor,
            font=ctk.CTkFont(weight="bold")
        )
        status_label.grid(row=0, column=4, padx=5, pady=8)

        if emprestimo['status_visual'] == "devolvido":

            ctk.CTkButton(
                row_frame,
                text="⭐ Avaliar",
                command=lambda emp=emprestimo: self.mostrar_formulario_avaliacao(
                    emp['livro_id'],
                    emp['livro_titulo'],
                    emp['id']),
                width=80,
                height=25,
                fg_color="#FFC107",
                hover_color="#E0A800").grid(
                row=0,
                column=5,
                padx=5,
                pady=4)
        else:

            ctk.CTkButton(
                row_frame,
                text="📥 Devolver",
                command=lambda emp=emprestimo: self.devolver_livro(emp['id']),
                width=80,
                height=25,
                fg_color="#28A745",
                hover_color="#1E7E34"
            ).grid(row=0, column=5, padx=5, pady=4)

    def recarregar_historico_se_ativo(self):
        """Recarrega o histórico de empréstimos se a aba estiver ativa"""
        try:

            if hasattr(self, 'notebook') and hasattr(self, 'usuario_logado'):

                current_tab = self.notebook.get()
                if "empréstimo" in current_tab.lower() or "histórico" in current_tab.lower():

                    try:

                        for child in self.notebook.winfo_children():
                            if hasattr(child, 'winfo_children'):
                                for grandchild in child.winfo_children():
                                    if hasattr(
                                            grandchild, 'winfo_children') and len(
                                            grandchild.winfo_children()) > 0:

                                        self.carregar_historico_emprestimos(
                                            grandchild)
                                        return
                    except Exception:
                        pass
        except Exception:

            pass

    def criar_aba_catalogo_livros(self, parent, tipo_usuario):
        """Cria aba com catálogo de livros para busca e reserva - Professores têm prioridade"""
        self.tipo_usuario_catalogo = tipo_usuario

        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            header_frame,
            text="🔍 Catálogo de Livros",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=20, pady=15)

        self.search_entry_catalogo = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar por título, autor, ISBN...",
            width=300
        )
        self.search_entry_catalogo.pack(side="left", padx=(0, 10))
        self.search_entry_catalogo.bind(
            "<KeyRelease>", lambda e: self.buscar_livros_catalogo())

        ctk.CTkButton(
            search_frame,
            text="🔄",
            command=self.limpar_busca_catalogo,
            width=40
        ).pack(side="left")

        if not BACKEND_DISPONIVEL:
            ctk.CTkLabel(
                main_frame,
                text="⚠️ Funcionalidade disponível apenas com backend conectado",
                font=ctk.CTkFont(
                    size=14)).pack(
                pady=50)
            return

        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True)

        headers = [
            "Título",
            "Autor",
            "Gênero",
            "Avaliação",
            "Disponível",
            "Ações"]
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(
                    weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(
                i, weight=1 if i in [0, 1] else 0)

        self.catalogo_content_frame = ctk.CTkScrollableFrame(
            list_frame, height=350)
        self.catalogo_content_frame.pack(
            fill="both", expand=True, padx=5, pady=5)

        self.carregar_catalogo_livros()

    def carregar_catalogo_livros(self):
        """Carrega livros do catálogo com priorização para professores"""

        for widget in self.catalogo_content_frame.winfo_children():
            widget.destroy()

        try:
            livros = Livro.listar_todos(incluir_inativos=False)

            if not livros:
                ctk.CTkLabel(
                    self.catalogo_content_frame,
                    text="📭 Nenhum livro disponível no momento",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=50)
                return

            if hasattr(
                    self,
                    'tipo_usuario_catalogo') and self.tipo_usuario_catalogo.lower() == 'professor':
                try:
                    from Backend.Avaliacao import Avaliacao

                    livros_com_media = []
                    for livro in livros:
                        media = Avaliacao.calcular_media_livro(livro.id)
                        livros_com_media.append((livro, media))

                    livros_com_media.sort(key=lambda x: (-x[1], x[0].nome))
                    livros = [livro for livro, media in livros_com_media]

                except Exception as e:
                    print(f"Erro ao ordenar por avaliações: {e}")

            for livro in livros:
                self.criar_linha_livro_catalogo(livro)

        except Exception as e:
            print(f"Erro ao carregar catálogo: {e}")

    def criar_linha_livro_catalogo(self, livro):
        """Cria linha do catálogo de livros"""

        row_frame = ctk.CTkFrame(self.catalogo_content_frame)
        row_frame.pack(fill="x", pady=2, padx=2)

        for i in range(6):
            row_frame.grid_columnconfigure(i, weight=1 if i in [0, 1] else 0)

        titulo_texto = livro.nome[:35] + \
            "..." if len(livro.nome) > 35 else livro.nome
        titulo_label = ctk.CTkLabel(
            row_frame,
            text=titulo_texto,
            font=ctk.CTkFont(
                weight="bold"))
        titulo_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")

        autor_label = ctk.CTkLabel(row_frame, text=livro.autor)
        autor_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        genero_label = ctk.CTkLabel(row_frame, text=livro.genero)
        genero_label.grid(row=0, column=2, padx=5, pady=8)

        try:
            from Backend.Avaliacao import Avaliacao
            media = Avaliacao.calcular_media_livro(livro.id)
            if media > 0:
                estrelas = "⭐" * int(media) + "☆" * (5 - int(media))
                avaliacao_texto = f"{estrelas} ({media:.1f})"
            else:
                avaliacao_texto = "Sem avaliações"
        except BaseException:
            avaliacao_texto = "N/A"

        avaliacao_label = ctk.CTkLabel(row_frame, text=avaliacao_texto)
        avaliacao_label.grid(row=0, column=3, padx=5, pady=8)

        disponivel = getattr(livro, 'quantidade_disponivel', 0)
        if disponivel > 0:
            disp_texto = f"✅ {disponivel} exemplar(es)"
            disp_cor = "#28A745"
        else:
            disp_texto = "❌ Indisponível"
            disp_cor = "#DC3545"

        disp_label = ctk.CTkLabel(
            row_frame,
            text=disp_texto,
            text_color=disp_cor)
        disp_label.grid(row=0, column=4, padx=5, pady=8)

        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=5, padx=5, pady=4)

        ctk.CTkButton(
            actions_frame,
            text="⭐ Avaliações",
            command=lambda l=livro: self.mostrar_avaliacoes_livro(l),
            width=90,
            height=25,
            fg_color="#FFC107",
            hover_color="#E0A800",
            text_color="black"
        ).pack(side="left", padx=2)

        if disponivel > 0:
            ctk.CTkButton(
                actions_frame,
                text="� Emprestar",
                command=lambda l=livro: self.pegar_emprestado(l),
                width=80,
                height=25,
                fg_color="#28A745",
                hover_color="#1E7E34"
            ).pack(side="left", padx=2)

        ctk.CTkButton(
            actions_frame,
            text="📋 Reservar",
            command=lambda l=livro: self.fazer_reserva_livro(l),
            width=80,
            height=25,
            fg_color="#007BFF",
            hover_color="#0056B3"
        ).pack(side="left", padx=2)

    def buscar_livros_catalogo(self):
        """Filtra livros no catálogo"""
        texto_busca = self.search_entry_catalogo.get().strip().lower()

        for widget in self.catalogo_content_frame.winfo_children():
            widget.destroy()

        if not texto_busca:
            self.carregar_catalogo_livros()
            return

        try:
            livros = Livro.listar_todos(incluir_inativos=False)
            livros_filtrados = []

            for livro in livros:
                if (texto_busca in livro.nome.lower() or
                    texto_busca in livro.autor.lower() or
                    texto_busca in livro.isbn.lower() or
                        texto_busca in livro.genero.lower()):
                    livros_filtrados.append(livro)

            if not livros_filtrados:
                ctk.CTkLabel(
                    self.catalogo_content_frame,
                    text="📭 Nenhum livro encontrado com os critérios de busca",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=50)
            else:
                for livro in livros_filtrados:
                    self.criar_linha_livro_catalogo(livro)

        except Exception as e:
            print(f"Erro na busca: {e}")

    def limpar_busca_catalogo(self):
        """Limpa a busca do catálogo"""
        self.search_entry_catalogo.delete(0, 'end')
        self.carregar_catalogo_livros()

    def mostrar_avaliacoes_livro(self, livro):
        """Mostra modal com avaliações do livro"""

        modal = ctk.CTkToplevel(self.root)
        modal.title(f"📊 Avaliações: {livro.nome}")
        modal.geometry("600x500")
        modal.transient(self.root)
        modal.grab_set()
        modal.resizable(True, True)

        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (600 // 2)
        y = (modal.winfo_screenheight() // 2) - (500 // 2)
        modal.geometry(f"600x500+{x}+{y}")

        main_frame = ctk.CTkFrame(modal)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            header_frame,
            text=f"📊 Avaliações",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        ctk.CTkLabel(
            header_frame,
            text=f"📚 {livro.nome}",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 10))

        try:
            from Backend.Avaliacao import Avaliacao
            avaliacoes = Avaliacao.listar_por_livro(livro.id)

            if avaliacoes:
                media = Avaliacao.calcular_media_livro(livro.id)
                total_avaliacoes = len(avaliacoes)

                stats_frame = ctk.CTkFrame(main_frame)
                stats_frame.pack(fill="x", pady=(0, 15))

                estrelas_visual = "⭐" * int(media) + "☆" * (5 - int(media))
                ctk.CTkLabel(
                    stats_frame,
                    text=f"Média: {estrelas_visual} {media:.1f}/5.0",
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack(pady=5)

                ctk.CTkLabel(
                    stats_frame,
                    text=f"Total de avaliações: {total_avaliacoes}",
                    font=ctk.CTkFont(size=12)
                ).pack(pady=5)

                avaliacoes_frame = ctk.CTkScrollableFrame(
                    main_frame, height=300)
                avaliacoes_frame.pack(fill="both", expand=True, pady=(0, 15))

                for i, avaliacao in enumerate(avaliacoes, 1):
                    av_frame = ctk.CTkFrame(avaliacoes_frame)
                    av_frame.pack(fill="x", pady=5, padx=5)

                    av_header = ctk.CTkFrame(av_frame, fg_color="transparent")
                    av_header.pack(fill="x", padx=10, pady=5)

                    estrelas = "⭐" * avaliacao.nota + \
                        "☆" * (5 - avaliacao.nota)
                    ctk.CTkLabel(
                        av_header,
                        text=f"{estrelas} ({avaliacao.nota}/5)",
                        font=ctk.CTkFont(weight="bold")
                    ).pack(side="left")

                    try:
                        from Backend.Usuario import Usuario
                        usuario_avaliador = Usuario.buscar_por_id(
                            avaliacao.usuario_id)
                        if usuario_avaliador:
                            tipo_icon = "👨‍🏫" if usuario_avaliador.tipo_usuario.lower() == 'professor' else "👨‍🎓"
                            nome_curto = usuario_avaliador.nome.split()[0]
                            avaliador_info = f"{tipo_icon} {nome_curto}"
                        else:
                            avaliador_info = "👤 Usuário"
                    except BaseException:
                        avaliador_info = "👤 Usuário"

                    ctk.CTkLabel(
                        av_header,
                        text=avaliador_info,
                        font=ctk.CTkFont(size=10),
                        text_color="gray"
                    ).pack(side="right", padx=(5, 10))

                    data_str = avaliacao.data_avaliacao.strftime(
                        "%d/%m/%Y") if avaliacao.data_avaliacao else "Data N/A"
                    ctk.CTkLabel(
                        av_header,
                        text=data_str,
                        font=ctk.CTkFont(size=10),
                        text_color="gray"
                    ).pack(side="right")

                    if avaliacao.comentario:
                        ctk.CTkLabel(
                            av_frame,
                            text=avaliacao.comentario,
                            font=ctk.CTkFont(size=12),
                            wraplength=500,
                            justify="left"
                        ).pack(fill="x", padx=15, pady=(0, 10))

            else:
                ctk.CTkLabel(
                    main_frame,
                    text="😔 Este livro ainda não possui avaliações",
                    font=ctk.CTkFont(size=14)
                ).pack(expand=True, pady=50)

        except Exception as e:
            print(f"Erro ao carregar avaliações: {e}")
            ctk.CTkLabel(
                main_frame,
                text="❌ Erro ao carregar avaliações",
                font=ctk.CTkFont(size=14)
            ).pack(expand=True, pady=50)

        ctk.CTkButton(
            main_frame,
            text="✅ Fechar",
            command=modal.destroy,
            width=100
        ).pack(pady=10)

    def pegar_emprestado(self, livro):
        """Realiza empréstimo do livro"""
        try:
            from Backend.Emprestimo import Emprestimo, StatusEmprestimo
            from datetime import datetime, timedelta

            emprestimos_ativos = Emprestimo.listar_por_usuario(
                self.usuario_logado.id)
            ja_tem_emprestimo = any(
                emp.livro_id == livro.id and emp.status in [
                    StatusEmprestimo.ATIVO,
                    StatusEmprestimo.ATRASADO] for emp in emprestimos_ativos)

            if ja_tem_emprestimo:
                messagebox.showwarning(
                    "Empréstimo Duplicado",
                    "Você já possui um empréstimo ativo deste livro!")
                return

            disponivel = getattr(livro, 'quantidade_disponivel', 0)
            print(
                f"🔍 DEBUG: Livro {livro.nome} - Quantidade disponível: {disponivel}")
            print(f"🔍 DEBUG: Livro ativo: {livro.ativo}")
            print(
                f"🔍 DEBUG: Disponível para empréstimo: {livro.disponivel_para_emprestimo}")

            if disponivel <= 0:
                messagebox.showwarning(
                    "Indisponível",
                    "Este livro não está disponível no momento. Deseja fazer uma reserva?")
                return

            data_emprestimo = datetime.now()
            data_devolucao_prevista = data_emprestimo + timedelta(days=14)

            novo_emprestimo = Emprestimo(
                usuario_id=self.usuario_logado.id,
                livro_id=livro.id,
                biblioteca_id=1,
                data_emprestimo=data_emprestimo,
                data_prevista_devolucao=data_devolucao_prevista
            )

            sucesso, mensagem = novo_emprestimo.salvar()

            if sucesso:
                messagebox.showinfo(
                    "Sucesso", f"Empréstimo realizado com sucesso!\n\n"
                    f"📚 Livro: {livro.nome}\n"
                    f"📅 Data de devolução: {data_devolucao_prevista.strftime('%d/%m/%Y')}\n"
                    f"⏰ Prazo: 14 dias")

                self.carregar_catalogo_livros()
            else:

                if "limite" in mensagem.lower() or "atingiu" in mensagem.lower():
                    resposta = messagebox.askyesno(
                        "Limite Atingido", f"Você atingiu o limite de empréstimos.\n\n"
                        f"Deseja fazer uma reserva do livro '{livro.nome}'?\n\n"
                        f"Você será notificado quando o livro estiver disponível.")
                    if resposta:
                        self.fazer_reserva_livro(livro)
                else:
                    messagebox.showerror(
                        "Erro", f"Falha ao realizar empréstimo: {mensagem}")

        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao processar empréstimo: {str(e)}")
            print(f"Erro detalhado: {e}")
            import traceback
            traceback.print_exc()

    def devolver_livro(self, emprestimo_id):
        """Realiza devolução do livro"""
        try:
            from Backend.Emprestimo import Emprestimo
            from datetime import datetime
            from tkinter import messagebox

            resposta = messagebox.askyesno(
                "Confirmar Devolução",
                "Deseja confirmar a devolução deste livro?"
            )

            if not resposta:
                return

            emprestimo_obj = Emprestimo.buscar_por_id(emprestimo_id)

            if not emprestimo_obj:
                messagebox.showerror("Erro", "Empréstimo não encontrado!")
                return

            sucesso, mensagem = emprestimo_obj.devolver(datetime.now())

            if sucesso:
                messagebox.showinfo(
                    "Sucesso",
                    "Livro devolvido com sucesso!\n\n"
                    "📚 O livro já está disponível para outros usuários."
                )

                self.recarregar_historico_se_ativo()

                if hasattr(self, 'carregar_catalogo_livros'):
                    self.carregar_catalogo_livros()
            else:
                messagebox.showerror("Erro", f"Falha na devolução: {mensagem}")

        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao processar devolução: {str(e)}")
            print(f"Erro detalhado: {e}")
            import traceback
            traceback.print_exc()

    def fazer_reserva_livro(self, livro):
        """Faz reserva de um livro"""
        try:
            from Backend.Reserva import Reserva, StatusReserva

            reservas_ativas = Reserva.listar_ativas(livro.id)
            ja_reservou = any(
                r.usuario_id == self.usuario_logado.id for r in reservas_ativas)

            if ja_reservou:
                messagebox.showwarning(
                    "Reserva Duplicada",
                    "Você já possui uma reserva ativa para este livro!")
                return

            nova_reserva = Reserva(
                usuario_id=self.usuario_logado.id,
                livro_id=livro.id
            )

            sucesso, mensagem = nova_reserva.salvar()

            if sucesso:

                from Backend.Notificacao import Notificacao

                if self.usuario_logado.tipo_usuario.lower() == 'professor':
                    mensagem_notif = f"Sua reserva PRIORITÁRIA para o livro '{livro.nome}' foi registrada. Como professor, você tem prioridade na fila de espera."
                    titulo_dialog = "Reserva Prioritária Realizada"
                else:
                    mensagem_notif = f"Sua reserva para o livro '{livro.nome}' foi registrada com sucesso. Você será notificado quando o livro estiver disponível."
                    titulo_dialog = "Reserva Realizada"

                Notificacao.criar_notificacao_sistema(
                    usuario_id=self.usuario_logado.id,
                    titulo=f"📋 Reserva Confirmada: {livro.nome}",
                    mensagem=mensagem_notif,
                    livro_id=livro.id
                )

                messagebox.showinfo(
                    titulo_dialog,
                    f"Reserva do livro '{livro.nome}' realizada com sucesso!\n\n{mensagem}")
            else:
                messagebox.showerror(
                    "Erro", f"Erro ao fazer reserva: {mensagem}")

        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao processar reserva: {str(e)}")

    def criar_aba_avaliacoes_usuario(self, parent):
        """Cria aba para o usuário gerenciar suas avaliações"""

        main_frame = ctk.CTkFrame(parent, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        titulo_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", pady=20)

        ctk.CTkLabel(
            titulo_frame,
            text="⭐ Minhas Avaliações de Livros",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left")

        ctk.CTkButton(
            titulo_frame,
            text="🔄 Atualizar",
            width=100,
            command=lambda: self.atualizar_aba_avaliacoes(),
            fg_color="#17A2B8",
            hover_color="#117A8B"
        ).pack(side="right")

        if not BACKEND_DISPONIVEL:
            ctk.CTkLabel(
                main_frame,
                text="⚠️ Funcionalidade disponível apenas com backend conectado",
                font=ctk.CTkFont(
                    size=14)).pack(
                pady=50)
            return

        try:
            from Backend.Avaliacao import Avaliacao
            from Backend.Livro import Livro

            avaliacoes_usuario = self.buscar_avaliacoes_usuario(
                self.usuario_logado.id)

            if avaliacoes_usuario:

                stats_frame = ctk.CTkFrame(main_frame)
                stats_frame.pack(fill="x", padx=20, pady=(0, 15))

                total_avaliacoes = len(avaliacoes_usuario)
                media_usuario = sum(
                    av['nota'] for av in avaliacoes_usuario) / total_avaliacoes

                ctk.CTkLabel(
                    stats_frame,
                    text=f"📊 Você fez {total_avaliacoes} avaliação(ões) | Sua média: {media_usuario:.1f}/5.0",
                    font=ctk.CTkFont(
                        size=14,
                        weight="bold")).pack(
                    pady=10)

                avaliacoes_frame = ctk.CTkScrollableFrame(
                    main_frame, height=400)
                avaliacoes_frame.pack(
                    fill="both",
                    expand=True,
                    padx=20,
                    pady=(
                        0,
                        20))

                for avaliacao in avaliacoes_usuario:
                    self.criar_item_avaliacao_usuario(
                        avaliacoes_frame, avaliacao)

            else:

                ctk.CTkLabel(
                    main_frame,
                    text="📭 Você ainda não fez nenhuma avaliação",
                    font=ctk.CTkFont(size=16)
                ).pack(expand=True)

                ctk.CTkLabel(
                    main_frame,
                    text="💡 Dica: Você pode avaliar livros que já devolveu na aba 'Meus Empréstimos'",
                    font=ctk.CTkFont(
                        size=12),
                    text_color="#6C757D").pack(
                    pady=10)

        except Exception as e:
            print(f"Erro ao carregar avaliações do usuário: {e}")
            ctk.CTkLabel(
                main_frame,
                text="❌ Erro ao carregar suas avaliações",
                font=ctk.CTkFont(size=14)
            ).pack(expand=True)

    def buscar_avaliacoes_usuario(self, usuario_id):
        """Busca todas as avaliações feitas por um usuário"""
        if not BACKEND_DISPONIVEL:
            return []
            
        try:
            from Backend.Avaliacao import Avaliacao
            return Avaliacao.listar_por_usuario(usuario_id)
            
        except Exception as e:
            print(f"Erro ao buscar avaliações do usuário: {e}")
            return []

    def atualizar_aba_avaliacoes(self):
        """Atualiza a aba de avaliações do usuário"""
        try:

            for nome_tab in self.notebook_usuario.get():
                if "Minhas Avaliações" in nome_tab:

                    tab = self.notebook_usuario.tab(nome_tab)
                    for widget in tab.winfo_children():
                        widget.destroy()
                    self.criar_aba_avaliacoes_usuario(tab)
                    break
        except Exception as e:
            print(f"Erro ao atualizar aba de avaliações: {e}")

            import tkinter.messagebox as messagebox
            messagebox.showinfo("Atualizar",
                                "Avaliações atualizadas com sucesso!")

    def criar_item_avaliacao_usuario(self, parent, avaliacao):
        """Cria um item da lista de avaliações do usuário"""

        item_frame = ctk.CTkFrame(parent)
        item_frame.pack(fill="x", pady=5, padx=5)

        header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=10)

        livro_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        livro_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            livro_frame,
            text=f"📚 {avaliacao['livro_nome']}",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            livro_frame,
            text=f"👤 {avaliacao['livro_autor']}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w")

        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="right")

        estrelas = "⭐" * avaliacao['nota'] + "☆" * (5 - avaliacao['nota'])
        ctk.CTkLabel(
            info_frame,
            text=f"{estrelas} {avaliacao['nota']}/5",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack()

        data_str = avaliacao['data_avaliacao'].strftime(
            "%d/%m/%Y") if avaliacao['data_avaliacao'] else "Data N/A"
        ctk.CTkLabel(
            info_frame,
            text=data_str,
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).pack()

        if avaliacao['comentario']:
            comentario_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            comentario_frame.pack(fill="x", padx=15, pady=(0, 10))

            ctk.CTkLabel(
                comentario_frame,
                text=f"💬 \"{avaliacao['comentario']}\"",
                font=ctk.CTkFont(size=12),
                wraplength=400,
                justify="left"
            ).pack(anchor="w")

    def mostrar_formulario_avaliacao(
            self, livro_id, livro_titulo, emprestimo_id):
        """Mostra formulário para avaliar um livro usando ID do empréstimo como chave"""

        try:
            from Backend.Avaliacao import Avaliacao

            avaliacoes = Avaliacao.listar_por_emprestimo(emprestimo_id)

            if avaliacoes:
                messagebox.showinfo(
                    "Avaliação Existente",
                    "Você já avaliou este empréstimo!")
                return

        except Exception as e:
            print(f"Erro ao verificar avaliação: {e}")

        modal = ctk.CTkToplevel(self.root)
        modal.title(f"⭐ Avaliar: {livro_titulo}")
        modal.geometry("480x550")
        modal.transient(self.root)
        modal.grab_set()
        modal.resizable(False, False)

        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (480 // 2)
        y = (modal.winfo_screenheight() // 2) - (550 // 2)
        modal.geometry(f"480x550+{x}+{y}")

        main_frame = ctk.CTkFrame(modal)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            main_frame,
            text=f"⭐ Avaliar Livro",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            main_frame,
            text=livro_titulo[:50] + "..." if len(livro_titulo) > 50 else livro_titulo,
            font=ctk.CTkFont(size=14),
            wraplength=350
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            main_frame,
            text="Nota:",
            font=ctk.CTkFont(
                size=14,
                weight="bold")).pack(
            anchor="w",
            padx=20)

        nota_var = ctk.IntVar(value=5)
        nota_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        nota_frame.pack(pady=10)

        for i in range(1, 6):
            ctk.CTkRadioButton(
                nota_frame,
                text=f"{i} {'⭐' * i}",
                variable=nota_var,
                value=i
            ).pack(anchor="w", padx=20, pady=2)

        ctk.CTkLabel(
            main_frame,
            text="Comentário (opcional):",
            font=ctk.CTkFont(
                size=14,
                weight="bold")).pack(
            anchor="w",
            padx=20,
            pady=(
                15,
                5))

        comentario_text = ctk.CTkTextbox(main_frame, height=100, width=380)
        comentario_text.pack(padx=20, pady=(5, 15))

        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=(0, 10))

        def salvar_avaliacao():
            try:
                from Backend.Avaliacao import Avaliacao

                comentario = comentario_text.get("1.0", "end-1c").strip()
                comentario = comentario if comentario else None

                nova_avaliacao = Avaliacao(
                    livro_id=livro_id,
                    usuario_id=self.usuario_logado.id,
                    nota=nota_var.get(),
                    comentario=comentario,
                    emprestimo_id=emprestimo_id
                )

                sucesso, mensagem = nova_avaliacao.salvar()

                if sucesso:
                    messagebox.showinfo(
                        "Sucesso", "Avaliação salva com sucesso!")
                    modal.destroy()

                    self.recarregar_historico_se_ativo()
                else:
                    messagebox.showerror("Erro", mensagem)

            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Erro ao salvar avaliação: {str(e)}")
                import traceback
                traceback.print_exc()

        ctk.CTkButton(
            buttons_frame,
            text="⭐ Salvar Avaliação",
            command=salvar_avaliacao,
            width=150,
            fg_color="#FFC107",
            hover_color="#E0A800",
            text_color="black"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=modal.destroy,
            width=100,
            fg_color="#6C757D",
            hover_color="#545B62"
        ).pack(side="left")

    def mostrar_notificacoes(self):
        """Mostra janela com notificações do usuário"""

        modal = ctk.CTkToplevel(self.root)
        modal.title("🔔 Notificações")
        modal.geometry("600x500")
        modal.transient(self.root)
        modal.grab_set()

        modal.update_idletasks()
        x = (modal.winfo_screenwidth() // 2) - (600 // 2)
        y = (modal.winfo_screenheight() // 2) - (500 // 2)
        modal.geometry(f"600x500+{x}+{y}")

        main_frame = ctk.CTkFrame(modal)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(10, 20))

        ctk.CTkLabel(
            header_frame,
            text="🔔 Suas Notificações",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkButton(
            header_frame,
            text="✅ Marcar Todas como Lidas",
            command=lambda: self.marcar_todas_como_lidas(modal),
            width=180,
            fg_color="#28A745",
            hover_color="#1E7E34"
        ).pack(side="right", padx=20, pady=15)

        notif_frame = ctk.CTkScrollableFrame(main_frame)
        notif_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        try:
            from Backend.Notificacao import Notificacao
            notificacoes = Notificacao.listar_por_usuario(
                self.usuario_logado.id, apenas_nao_lidas=False)

            if not notificacoes:
                ctk.CTkLabel(
                    notif_frame,
                    text="📭 Nenhuma notificação encontrada",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=50)
            else:
                for notif in notificacoes:
                    self.criar_item_notificacao(notif_frame, notif)

        except Exception as e:
            print(f"Erro ao carregar notificações: {e}")

        ctk.CTkButton(
            main_frame,
            text="❌ Fechar",
            command=modal.destroy,
            width=120
        ).pack(pady=10)

    def criar_item_notificacao(self, parent, notificacao):
        """Cria um item de notificação"""

        notif_frame = ctk.CTkFrame(parent)
        notif_frame.pack(fill="x", pady=5, padx=5)

        cor_borda = "#FFC107" if notificacao.status.value == "NAO_LIDA" else "#E9ECEF"

        header_frame = ctk.CTkFrame(notif_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))

        titulo_texto = f"{'🆕' if notificacao.status.value == 'NAO_LIDA' else '👁️'} {notificacao.titulo}"
        ctk.CTkLabel(
            header_frame,
            text=titulo_texto,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left")

        data_texto = notificacao.data_criacao.strftime("%d/%m/%Y %H:%M")
        ctk.CTkLabel(
            header_frame,
            text=data_texto,
            font=ctk.CTkFont(size=10),
            text_color="#6C757D"
        ).pack(side="right")

        ctk.CTkLabel(
            notif_frame,
            text=notificacao.mensagem,
            font=ctk.CTkFont(size=11),
            wraplength=500,
            justify="left"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        if notificacao.status.value == "NAO_LIDA":
            ctk.CTkButton(
                notif_frame,
                text="✅ Marcar como Lida",
                command=lambda: self.marcar_notificacao_lida(notificacao),
                width=150,
                height=25,
                fg_color="#28A745",
                hover_color="#1E7E34"
            ).pack(anchor="e", padx=15, pady=(0, 10))

    def marcar_notificacao_lida(self, notificacao):
        """Marca uma notificação como lida"""
        try:
            sucesso, mensagem = notificacao.marcar_como_lida()
            if sucesso:

                messagebox.showinfo(
                    "Sucesso", "Notificação marcada como lida!")
            else:
                messagebox.showerror("Erro", mensagem)
        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao marcar notificação: {str(e)}")

    def marcar_todas_como_lidas(self, modal):
        """Marca todas as notificações como lidas"""
        try:
            from Backend.Notificacao import Notificacao
            notificacoes = Notificacao.listar_por_usuario(
                self.usuario_logado.id, apenas_nao_lidas=True)

            for notif in notificacoes:
                notif.marcar_como_lida()

            messagebox.showinfo(
                "Sucesso",
                f"{len(notificacoes)} notificação(ões) marcada(s) como lida(s)!")
            modal.destroy()

        except Exception as e:
            messagebox.showerror(
                "Erro", f"Erro ao marcar notificações: {str(e)}")

    def fazer_logout(self):
        """Realiza o logout do usuário"""
        messagebox.showinfo(
            "Logout",
            f"Logout realizado com sucesso! Até logo, {self.usuario_logado.nome}!")

        self.usuario_logado = None
        self.livro_selecionado = None
        self.livros_atuais = []
        self.criar_tela_selecao_usuario()

    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()


def main():
    app = SistemaBibliotecaCompleto()
    app.executar()


if __name__ == "__main__":
    main()
