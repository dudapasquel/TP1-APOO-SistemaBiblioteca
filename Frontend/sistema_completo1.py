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
    from Backend.usuario import Usuario
    from Backend.livro import Livro
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

        subtitulo = ctk.CTkLabel(
            main_frame,
            text="Sistema Integrado de Gerenciamento Bibliográfico",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#666666"
        )
        subtitulo.pack(pady=(0, 40))

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
            font=ctk.CTkFont(size=12),
            justify="left"
        )
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
            font=ctk.CTkFont(size=12),
            justify="left"
        )
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
            font=ctk.CTkFont(size=12),
            justify="left"
        )
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
                    f"Tipo de usuário incorreto. Esperado: {self.tipo_usuario_selecionado}"
                )
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

        tab_livros = notebook.add("📖 Gerenciar Livros")
        self.criar_aba_livros_completa(tab_livros)

        tab_usuarios = notebook.add("👥 Usuários")
        self.criar_aba_usuarios(tab_usuarios)

        self.carregar_livros_completo()

    def criar_aba_livros_completa(self, parent):
        """Cria a aba completa de gerenciamento de livros"""

        controls_frame = ctk.CTkFrame(parent)
        controls_frame.pack(fill="x", padx=10, pady=10)

        titulo_frame = ctk.CTkFrame(controls_frame)
        titulo_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(titulo_frame, text="📚 Gerenciamento Completo de Livros",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=10)

        self.stats_label = ctk.CTkLabel(titulo_frame, text="Carregando estatísticas...",
                                        font=ctk.CTkFont(size=12))
        self.stats_label.pack(side="right", padx=10)

        acoes_frame = ctk.CTkFrame(controls_frame)
        acoes_frame.pack(fill="x", pady=10)

        btn_frame1 = ctk.CTkFrame(acoes_frame)
        btn_frame1.pack(fill="x", pady=5)

        ctk.CTkButton(btn_frame1, text="➕ Adicionar Livro",
                      command=self.adicionar_livro_completo, width=150,
                      fg_color="#28A745", hover_color="#1E7E34").pack(side="left", padx=5)

        ctk.CTkButton(btn_frame1, text="✏️ Editar Selecionado",
                      command=self.editar_livro_completo, width=150,
                      fg_color="#FFC107", hover_color="#E0A800", text_color="black").pack(side="left", padx=5)

        self.btn_toggle_status = ctk.CTkButton(btn_frame1, text="� Alterar Status",
                                               command=self.toggle_status_livro, width=150,
                                               fg_color="#6C757D", hover_color="#5A6268")
        self.btn_toggle_status.pack(side="left", padx=5)

        btn_frame2 = ctk.CTkFrame(acoes_frame)
        btn_frame2.pack(fill="x", pady=5)

        ctk.CTkButton(btn_frame1, text="🔍 Buscar por ISBN",
                      command=self.buscar_por_isbn, width=150).pack(side="left", padx=5)

        ctk.CTkButton(btn_frame1, text="📋 Ver Detalhes",
                      command=self.mostrar_detalhes_livro, width=150,
                      fg_color="#6C757D", hover_color="#545B62").pack(side="left", padx=5)

        ctk.CTkButton(btn_frame1, text="� Atualizar Lista",
                      command=self.carregar_livros_completo, width=150).pack(side="left", padx=5)

        self.switch_inativos = ctk.CTkSwitch(
            btn_frame2,
            text="Mostrar Livros Inativos",
            command=self.toggle_livros_inativos,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.switch_inativos.pack(side="right", padx=10)

        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        headers = ["ID", "Título", "Autor", "ISBN",
                   "Gênero", "Status", "Data Cadastro"]
        header_frame = ctk.CTkFrame(list_frame)
        header_frame.pack(fill="x", padx=5, pady=5)

        for i, header in enumerate(headers):
            label = ctk.CTkLabel(header_frame, text=header,
                                 font=ctk.CTkFont(weight="bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            header_frame.grid_columnconfigure(
                i, weight=1 if i in [1, 2] else 0)

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

        for j in range(7):
            row_frame.grid_columnconfigure(j, weight=1 if j in [1, 2] else 0)

        ativo = getattr(livro, 'ativo', True)
        cor_status = "#28A745" if ativo else "#DC3545"
        status_texto = "✅ Ativo" if ativo else "❌ Inativo"

        row_frame.bind("<Button-1>", lambda e, l=livro,
                       f=row_frame: self.selecionar_livro_visual(l, f))

        id_label = ctk.CTkLabel(
            row_frame, text=str(getattr(livro, 'id', 'N/A')))
        id_label.grid(row=0, column=0, padx=5, pady=8)
        id_label.bind("<Button-1>", lambda e, l=livro,
                      f=row_frame: self.selecionar_livro_visual(l, f))

        titulo_texto = livro.nome[:35] + \
            "..." if len(livro.nome) > 35 else livro.nome
        titulo_label = ctk.CTkLabel(
            row_frame, text=titulo_texto, font=ctk.CTkFont(weight="bold"))
        titulo_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        titulo_label.bind("<Button-1>", lambda e, l=livro,
                          f=row_frame: self.selecionar_livro_visual(l, f))

        autor_label = ctk.CTkLabel(row_frame, text=livro.autor)
        autor_label.grid(row=0, column=2, padx=5, pady=8)
        autor_label.bind("<Button-1>", lambda e, l=livro,
                         f=row_frame: self.selecionar_livro_visual(l, f))

        isbn_label = ctk.CTkLabel(row_frame, text=livro.isbn)
        isbn_label.grid(row=0, column=3, padx=5, pady=8)
        isbn_label.bind("<Button-1>", lambda e, l=livro,
                        f=row_frame: self.selecionar_livro_visual(l, f))

        genero_label = ctk.CTkLabel(row_frame, text=livro.genero)
        genero_label.grid(row=0, column=4, padx=5, pady=8)
        genero_label.bind("<Button-1>", lambda e, l=livro,
                          f=row_frame: self.selecionar_livro_visual(l, f))

        status_label = ctk.CTkLabel(
            row_frame, text=status_texto, text_color=cor_status, font=ctk.CTkFont(weight="bold"))
        status_label.grid(row=0, column=5, padx=5, pady=8)
        status_label.bind("<Button-1>", lambda e, l=livro,
                          f=row_frame: self.selecionar_livro_visual(l, f))

        data_cadastro = getattr(livro, 'data_cadastro', 'N/A')
        if hasattr(data_cadastro, 'strftime'):
            data_str = data_cadastro.strftime("%d/%m/%Y")
        else:
            data_str = str(data_cadastro)[:10] if data_cadastro else "N/A"

        data_label = ctk.CTkLabel(row_frame, text=data_str)
        data_label.grid(row=0, column=6, padx=5, pady=8)
        data_label.bind("<Button-1>", lambda e, l=livro,
                        f=row_frame: self.selecionar_livro_visual(l, f))

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

    def mostrar_detalhes_livro(self):
        """Abre modal com detalhes completos do livro selecionado"""
        if not self.livro_selecionado:
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

        livro = self.livro_selecionado
        ativo = getattr(livro, 'ativo', True)
        status_cor = "#28A745" if ativo else "#DC3545"
        status_texto = "Ativo" if ativo else "Inativo"

        detalhes_info = [
            ("📋 ID:", str(getattr(livro, 'id', 'N/A'))),
            ("📚 Título:", livro.nome),
            ("✍️ Autor:", livro.autor),
            ("🔢 ISBN:", livro.isbn),
            ("🎭 Gênero:", livro.genero),
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

            cor_texto = status_cor if label.startswith("📊") else None
            valor_widget = ctk.CTkLabel(
                info_frame,
                text=valor,
                font=ctk.CTkFont(size=14),
                anchor="w",
                text_color=cor_texto
            )
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
            font=ctk.CTkFont(size=20, weight="bold")
        )
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
                    "Simulação", f"Livro {'adicionado' if modo == 'adicionar' else 'editado'} com sucesso (modo simulação)")
                janela.destroy()

        ctk.CTkButton(
            botoes_frame,
            text=f"💾 {'Adicionar' if modo == 'adicionar' else 'Salvar Alterações'}",
            command=salvar_livro,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#28A745",
            hover_color="#1E7E34"
        ).pack(side="left", padx=10)

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

    def inativar_livro(self):
        """Inativa o livro selecionado"""
        if not self.livro_selecionado:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        resposta = messagebox.askyesno(
            "Confirmar Inativação",
            f"Deseja realmente inativar o livro:\n\n'{self.livro_selecionado.nome}'?\n\nO livro ficará indisponível para empréstimos."
        )

        if resposta:
            if BACKEND_DISPONIVEL:
                sucesso, mensagem = self.livro_selecionado.excluir()

                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.carregar_livros_completo()
                    self.livro_selecionado = None
                    self.linha_selecionada = None
                else:
                    messagebox.showerror("Erro", mensagem)
            else:
                messagebox.showinfo("Operação Realizada",
                                    "Livro inativado com sucesso")

    def reativar_livro(self):
        """Reativa o livro selecionado"""
        if not self.livro_selecionado:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        if getattr(self.livro_selecionado, 'ativo', True):
            messagebox.showinfo("Informação", "Este livro já está ativo!")
            return

        resposta = messagebox.askyesno(
            "Confirmar Reativação",
            f"Deseja reativar o livro:\n\n'{self.livro_selecionado.nome}'?"
        )

        if resposta:
            if BACKEND_DISPONIVEL:
                sucesso, mensagem = self.livro_selecionado.reativar()

                if sucesso:
                    messagebox.showinfo("Sucesso", mensagem)
                    self.carregar_livros_completo()
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

    def toggle_status_livro(self):
        """Alterna o status (ativo/inativo) do livro selecionado"""
        if not self.livro_selecionado:
            messagebox.showwarning(
                "Atenção", "Por favor, selecione um livro primeiro!")
            return

        ativo = getattr(self.livro_selecionado, 'ativo', True)

        if ativo:
            self.inativar_livro()
        else:
            self.reativar_livro()

    def buscar_por_isbn(self):
        """Busca livro por ISBN"""
        isbn = simpledialog.askstring(
            "Buscar por ISBN", "Digite o ISBN do livro:")

        if isbn:
            if BACKEND_DISPONIVEL:
                livro = Livro.buscar_por_isbn(isbn.strip())
                if livro:

                    self.carregar_livros_completo()

                    for widget in self.livros_content_frame.winfo_children():

                        pass
                    messagebox.showinfo(
                        "Livro Encontrado", f"Livro '{livro.nome}' localizado na lista!")
                else:
                    messagebox.showinfo(
                        "Não Encontrado", f"Nenhum livro encontrado com ISBN: {isbn}")
            else:
                messagebox.showinfo("Busca Realizada",
                                    f"Busca por ISBN: {isbn}")

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

    def criar_aba_usuarios(self, parent):
        """Cria a aba de gerenciamento de usuários"""
        ctk.CTkLabel(parent, text="👥 Gerenciamento de Usuários",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        if BACKEND_DISPONIVEL:
            usuarios = Usuario.listar_todos()

            lista_frame = ctk.CTkScrollableFrame(parent, height=400)
            lista_frame.pack(fill="both", expand=True, padx=20, pady=20)

            for usuario in usuarios:
                user_frame = ctk.CTkFrame(lista_frame)
                user_frame.pack(fill="x", pady=5)

                info_text = f"📧 {usuario.email} | 👤 {usuario.nome} | 🏷️ {usuario.tipo_usuario}"
                ctk.CTkLabel(user_frame, text=info_text, font=ctk.CTkFont(
                    size=12)).pack(side="left", padx=10, pady=10)
        else:
            info_label = ctk.CTkLabel(
                parent, text="Funcionalidade disponível apenas com backend conectado")
            info_label.pack(pady=50)

    def tela_aluno(self):
        """Interface específica do aluno"""
        self.tela_usuario_comum("🎓 Painel do Aluno", "aluno")

    def tela_professor(self):
        """Interface específica do professor"""
        self.tela_usuario_comum("👨‍🏫 Painel do Professor", "professor")

    def tela_usuario_comum(self, titulo: str, tipo: str):
        """Interface comum para aluno e professor"""

        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=(0, 20))

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

        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(
            content_frame,
            text="📚 Catálogo de Livros Disponíveis",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        if BACKEND_DISPONIVEL:
            livros = Livro.listar_todos(incluir_inativos=False)

            lista_frame = ctk.CTkScrollableFrame(content_frame, height=400)
            lista_frame.pack(fill="both", expand=True, padx=20, pady=20)

            for livro in livros:
                livro_frame = ctk.CTkFrame(lista_frame)
                livro_frame.pack(fill="x", pady=5)

                livro_info = f"📖 {livro.nome} | ✍️ {livro.autor} | 🎭 {livro.genero}"
                ctk.CTkLabel(livro_frame, text=livro_info, font=ctk.CTkFont(
                    size=12)).pack(side="left", padx=10, pady=10)

                if tipo == "professor":
                    ctk.CTkButton(
                        livro_frame,
                        text="📋 Reservar",
                        command=lambda: messagebox.showinfo(
                            "Reserva", "Funcionalidade em desenvolvimento"),
                        width=100
                    ).pack(side="right", padx=10, pady=5)
                else:
                    ctk.CTkButton(
                        livro_frame,
                        text="📖 Solicitar",
                        command=lambda: messagebox.showinfo(
                            "Empréstimo", "Funcionalidade em desenvolvimento"),
                        width=100
                    ).pack(side="right", padx=10, pady=5)
        else:
            ctk.CTkLabel(
                content_frame, text="📊 Dados disponíveis apenas com backend conectado").pack(pady=50)

    def fazer_logout(self):
        """Realiza o logout do usuário"""
        messagebox.showinfo(
            "Logout", f"Logout realizado com sucesso! Até logo, {self.usuario_logado.nome}!")

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
