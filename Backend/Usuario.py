from datetime import datetime
from typing import Optional
import hashlib
from abc import ABC, abstractmethod


class Usuario(ABC):

    def __init__(
        self, nome: str, email: str, senha: str, id: Optional[int] = None,
        ativo: bool = True, data_cadastro: Optional[datetime] = None,
        data_atualizacao: Optional[datetime] = None
    ):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = self._criptografar_senha(
            senha) if not self._eh_senha_criptografada(senha) else senha
        self._ativo = ativo
        self._data_cadastro = data_cadastro
        self._data_atualizacao = data_atualizacao

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        if len(novo_nome.strip()) < 2:
            raise ValueError("Nome deve ter pelo menos 2 caracteres")
        self._nome = novo_nome

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, novo_email):
        if '@' not in novo_email:
            raise ValueError("Email inválido")
        self._email = novo_email

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, nova_senha):
        self._senha = self._criptografar_senha(nova_senha)

    @property
    @abstractmethod
    def tipo_usuario(self):
        pass

    @property
    def ativo(self):
        return self._ativo

    @ativo.setter
    def ativo(self, valor):
        self._ativo = valor

    @property
    def data_cadastro(self):
        return self._data_cadastro

    @property
    def data_atualizacao(self):
        return self._data_atualizacao

    @abstractmethod
    def validar_dados_especificos(self) -> tuple[bool, str]:
        pass

    @abstractmethod
    def obter_dados_para_banco(self) -> dict:
        pass

    @property
    def matricula(self):
        return getattr(self, '_matricula', None)

    @property
    def curso(self):
        return getattr(self, '_curso', None)

    @property
    def departamento(self):
        return getattr(self, '_departamento', None)

    def _criptografar_senha(self, senha: str) -> str:
        return hashlib.md5(senha.encode()).hexdigest()

    def _eh_senha_criptografada(self, senha: str) -> bool:
        return len(senha) == 32 and all(
            c in '0123456789abcdef' for c in senha.lower())

    def verificar_senha(self, senha: str) -> bool:
        senha_criptografada = self._criptografar_senha(senha)
        return senha_criptografada == self.senha

    def __str__(self) -> str:
        return f"Usuario(id={self.id}, nome='{self.nome}', tipo='{self.tipo_usuario}')"

    def __repr__(self) -> str:
        return (
            f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email}', "
            f"tipo='{self.tipo_usuario}', ativo={self.ativo})")

    def to_dict(self) -> dict:
        dados = self.obter_dados_para_banco()
        dados.update({
            'id': self.id,
            'ativo': self.ativo,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None
        })
        return dados

    def validar(self) -> tuple[bool, str]:
        if not self.nome or len(self.nome.strip()) < 2:
            return False, "Nome deve ter pelo menos 2 caracteres"

        if not self.email or '@' not in self.email:
            return False, "Email deve ser válido"

        return self.validar_dados_especificos()

    def salvar(self) -> tuple[bool, str]:
        from Banco_de_dados.connection import DatabaseConnection

        valido, mensagem = self.validar()
        if not valido:
            return False, f"Erro de validação: {mensagem}"

        db = DatabaseConnection()

        if self.id is None:
            return self._inserir(db)
        else:
            return self._atualizar(db)

    def _inserir(self, db) -> tuple[bool, str]:
        if self._email_existe(db, self.email):
            return False, f"Email {self.email} já está em uso"

        try:
            dados = self.obter_dados_para_banco()
            query = "INSERT INTO Usuario (Nome, Email, Senha, TipoUsuario, Matricula, Curso, Departamento) VALUES (?, ?, ?, ?, ?, ?, ?)"
            params = (
                dados['nome'],
                dados['email'],
                dados['senha'],
                dados['tipo_usuario'],
                dados.get('matricula'),
                dados.get('curso'),
                dados.get('departamento'))

            if db.execute_non_query(query, params):
                self.id = self._buscar_ultimo_id(db)
                mensagem = f"Usuário '{self.nome}' cadastrado com sucesso!"
                print(f"✓ {mensagem}")
                return True, mensagem
            else:
                mensagem = f"Falha ao cadastrar usuário '{self.nome}'"
                return False, mensagem

        except Exception as e:
            mensagem = f"Erro ao cadastrar usuário: {e}"
            print(f"✗ {mensagem}")
            return False, mensagem

    def _atualizar(self, db) -> tuple[bool, str]:
        if not self._existe_por_id(db, self.id):
            return False, f"Usuário com ID {self.id} não encontrado"

        usuario_existente = self.buscar_por_email(self.email)
        if usuario_existente and usuario_existente.id != self.id:
            return False, f"Email {self.email} já está sendo usado por outro usuário"

        try:
            dados = self.obter_dados_para_banco()
            query = "UPDATE Usuario SET Nome = ?, Email = ?, TipoUsuario = ?, Matricula = ?, Curso = ?, Departamento = ? WHERE Id = ?"
            params = (
                dados['nome'],
                dados['email'],
                dados['tipo_usuario'],
                dados.get('matricula'),
                dados.get('curso'),
                dados.get('departamento'),
                self.id)

            if db.execute_non_query(query, params):
                mensagem = f"Usuário '{self.nome}' atualizado com sucesso!"
                return True, mensagem
            else:
                return False, f"Falha ao atualizar usuário '{self.nome}'"

        except Exception as e:
            return False, f"Erro ao atualizar usuário: {e}"

    def excluir(self) -> tuple[bool, str]:
        """Inativa o usuário (soft delete)"""
        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID do usuário é obrigatório para exclusão"

        db = DatabaseConnection()

        try:
            query = "UPDATE Usuario SET Ativo = 0 WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                self.ativo = False
                return True, f"Usuário '{self.nome}' inativado com sucesso!"
            else:
                return False, f"Falha ao inativar usuário '{self.nome}'"

        except Exception as e:
            return False, f"Erro ao inativar usuário: {e}"

    def ativar(self) -> tuple[bool, str]:
        """Ativa o usuário"""
        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID do usuário é obrigatório para ativação"

        db = DatabaseConnection()

        try:
            query = "UPDATE Usuario SET Ativo = 1 WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                self.ativo = True
                return True, f"Usuário '{self.nome}' ativado com sucesso!"
            else:
                return False, f"Falha ao ativar usuário '{self.nome}'"

        except Exception as e:
            return False, f"Erro ao ativar usuário: {e}"

    @staticmethod
    def autenticar(email: str,
                   senha: str) -> tuple[bool,
                                        Optional['Usuario'],
                                        str]:
        usuario = Usuario.buscar_por_email(email)

        if not usuario:
            return False, None, "Email não encontrado"

        if not usuario.ativo:
            return False, None, "Usuário inativo"

        if not usuario.verificar_senha(senha):
            return False, None, "Senha incorreta"

        return True, usuario, "Login realizado com sucesso"

    @staticmethod
    def listar_todos(
            limite: int = 100,
            incluir_inativos: bool = False) -> list['Usuario']:
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            if incluir_inativos:
                query = "SELECT * FROM Usuario ORDER BY Nome OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY"
                params = (limite,)
            else:
                query = "SELECT * FROM Usuario WHERE Ativo = 1 ORDER BY Nome OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY"
                params = (limite,)

            resultados = db.execute_query(query, params)

            if resultados:
                return [Usuario._from_db_row(row) for row in resultados]
            else:
                return []

        except Exception as e:
            print(f"✗ Erro ao listar usuários: {e}")
            return []

    @staticmethod
    def buscar_por_email(email: str) -> Optional['Usuario']:
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query = "SELECT * FROM Usuario WHERE Email = ?"
            resultados = db.execute_query(query, (email,))

            if resultados:
                return Usuario._from_db_row(resultados[0])
            else:
                return None

        except Exception as e:
            print(f"✗ Erro ao buscar usuário por email: {e}")
            return None

    @staticmethod
    def buscar_por_id(usuario_id: int) -> Optional['Usuario']:
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query = "SELECT * FROM Usuario WHERE Id = ?"
            resultados = db.execute_query(query, (usuario_id,))

            if resultados:
                return Usuario._from_db_row(resultados[0])
            else:
                return None

        except Exception as e:
            print(f"✗ Erro ao buscar usuário por ID: {e}")
            return None

    @staticmethod
    def _from_db_row(row) -> 'Usuario':
        tipo = row['TipoUsuario']

        kwargs = {
            'id': row['Id'],
            'ativo': bool(row['Ativo']),
            'data_cadastro': row['DataCadastro'],
            'data_atualizacao': row['DataAtualizacao']
        }

        if tipo == "Aluno":
            from Backend.Aluno import Aluno
            return Aluno(
                nome=row['Nome'],
                email=row['Email'],
                senha=row['Senha'],
                matricula=row['Matricula'],
                curso=row['Curso'],
                **kwargs
            )
        elif tipo == "Professor":
            from Backend.Professor import Professor
            return Professor(
                nome=row['Nome'],
                email=row['Email'],
                senha=row['Senha'],
                matricula=row['Matricula'],
                departamento=row['Departamento'],
                **kwargs
            )
        elif tipo == "Bibliotecario":
            from Backend.Bibliotecario import Bibliotecario
            return Bibliotecario(
                nome=row['Nome'],
                email=row['Email'],
                senha=row['Senha'],
                **kwargs
            )
        else:
            raise ValueError(f"Tipo de usuário '{tipo}' não reconhecido")

    def _email_existe(self, db, email: str) -> bool:
        try:
            query = "SELECT COUNT(*) FROM Usuario WHERE Email = ?"
            resultado = db.execute_scalar(query, (email,))
            return resultado and resultado > 0
        except BaseException:
            return False

    def _existe_por_id(self, db, usuario_id: int) -> bool:
        try:
            query = "SELECT COUNT(*) FROM Usuario WHERE Id = ?"
            resultado = db.execute_scalar(query, (usuario_id,))
            return resultado and resultado > 0
        except BaseException:
            return False

    def _buscar_ultimo_id(self, db) -> Optional[int]:
        try:
            query = "SELECT SCOPE_IDENTITY()"
            resultado = db.execute_query(query)
            return int(resultado[0][0]) if resultado else None
        except BaseException:
            return None
