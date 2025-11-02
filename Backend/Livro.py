from datetime import datetime
from typing import Optional


# Provide a lowercase alias for the module name so imports like `from Backend.livro import Livro`
# work on systems where filenames are case-insensitive but import names are expected lowercase.
import sys
sys.modules.setdefault('Backend.livro', sys.modules.get(__name__))


class Livro:

    def __init__(self, nome: str, autor: str, isbn: str, genero: str,
                 id: Optional[int] = None, data_cadastro: Optional[datetime] = None,
                 data_atualizacao: Optional[datetime] = None, ativo: bool = True):
        self._id = id
        self._nome = nome
        self.autor = autor
        self._isbn = isbn
        self.genero = genero
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao
        self._ativo = ativo


    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        if len(novo_nome.strip()) < 2:
            raise ValueError("Nome do livro deve ter pelo menos 2 caracteres")
        self._nome = novo_nome

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, novo_isbn):
        if len(novo_isbn.strip()) < 10:
            raise ValueError("ISBN deve ter pelo menos 10 caracteres")
        self._isbn = novo_isbn

    @property
    def ativo(self):
        return self._ativo

    @ativo.setter
    def ativo(self, valor: bool):
        self._ativo = valor

    def __str__(self) -> str:
        return f"Livro(id={self.id}, nome='{self.nome}', autor='{self.autor}', isbn='{self.isbn}')"

    def __repr__(self) -> str:
        return (f"Livro(id={self.id}, nome='{self.nome}', autor='{self.autor}', "
                f"isbn='{self.isbn}', genero='{self.genero}', ativo={self.ativo})")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'autor': self.autor,
            'isbn': self.isbn,
            'genero': self.genero,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'ativo': self.ativo
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Livro':
        return cls(
            id=data.get('id'),
            nome=data['nome'],
            autor=data['autor'],
            isbn=data['isbn'],
            genero=data['genero'],
            data_cadastro=datetime.fromisoformat(data['data_cadastro']) if data.get('data_cadastro') else None,
            data_atualizacao=datetime.fromisoformat(data['data_atualizacao']) if data.get('data_atualizacao') else None,
            ativo=data.get('ativo', True)
        )

    def validar(self) -> tuple[bool, str]:
        if not self.nome or len(self.nome.strip()) < 2:
            return False, "Nome do livro deve ter pelo menos 2 caracteres"

        if not self.autor or len(self.autor.strip()) < 2:
            return False, "Nome do autor deve ter pelo menos 2 caracteres"

        if not self.isbn or len(self.isbn.strip()) < 10:
            return False, "ISBN deve ter pelo menos 10 caracteres"

        if not self.genero or len(self.genero.strip()) < 2:
            return False, "Gênero deve ter pelo menos 2 caracteres"

        return True, "Livro válido"

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
        if self._isbn_existe(db, self.isbn):
            return False, f"Livro com ISBN {self.isbn} já existe"

        try:
            query = "INSERT INTO Livro (Nome, Autor, ISBN, Genero) VALUES (?, ?, ?, ?)"
            params = (self.nome, self.autor, self.isbn, self.genero)

            if db.execute_non_query(query, params):
                self.id = self._buscar_ultimo_id(db)
                mensagem = f"Livro '{self.nome}' adicionado com sucesso!"
                print(f"✓ {mensagem}")
                return True, mensagem
            else:
                mensagem = f"Falha ao inserir livro '{self.nome}'"
                return False, mensagem

        except Exception as e:
            mensagem = f"Erro ao inserir livro: {e}"
            print(f"✗ {mensagem}")
            return False, mensagem

    def _atualizar(self, db) -> tuple[bool, str]:
        if not self._existe_por_id(db, self.id):
            return False, f"Livro com ID {self.id} não encontrado"

        livro_existente = self.buscar_por_isbn(self.isbn)
        if livro_existente and livro_existente.id != self.id:
            return False, f"ISBN {self.isbn} já está sendo usado por outro livro"

        try:
            query = "UPDATE Livro SET Nome = ?, Autor = ?, ISBN = ?, Genero = ? WHERE Id = ?"
            params = (self.nome, self.autor, self.isbn, self.genero, self.id)

            if db.execute_non_query(query, params):
                mensagem = f"Livro '{self.nome}' atualizado com sucesso!"
                return True, mensagem
            else:
                return False, f"Falha ao atualizar livro '{self.nome}'"

        except Exception as e:
            return False, f"Erro ao atualizar livro: {e}"

    def excluir(self) -> tuple[bool, str]:
        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID do livro é obrigatório para exclusão"

        db = DatabaseConnection()

        try:
            query = "UPDATE Livro SET Ativo = 0 WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                self.ativo = False
                return True, f"Livro '{self.nome}' inativado com sucesso!"
            else:
                return False, f"Falha ao inativar livro '{self.nome}'"

        except Exception as e:
            return False, f"Erro ao inativar livro: {e}"

    def reativar(self) -> tuple[bool, str]:
        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID do livro é obrigatório para reativação"

        db = DatabaseConnection()

        try:
            query = "UPDATE Livro SET Ativo = 1 WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                self.ativo = True
                return True, f"Livro '{self.nome}' reativado com sucesso!"
            else:
                return False, f"Falha ao reativar livro '{self.nome}'"

        except Exception as e:
            return False, f"Erro ao reativar livro: {e}"

    def deletar(self) -> tuple[bool, str]:
        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID do livro é obrigatório para exclusão"

        db = DatabaseConnection()

        try:
            if not self._existe_por_id(db, self.id):
                return False, "Livro não encontrado"

            query = "DELETE FROM Livro WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                nome_livro = self.nome
                self.id = None
                return True, f"Livro '{nome_livro}' deletado permanentemente!"
            else:
                return False, f"Falha ao deletar livro '{self.nome}'"

        except Exception as e:
            return False, f"Erro ao deletar livro: {e}"

    def pode_ser_deletado(self) -> tuple[bool, str]:
        if not self.id:
            return False, "Livro não foi salvo ainda"

        if self.ativo:
            return False, "Livro deve estar inativo para ser deletado. Use inativar() primeiro."

        return True, "Livro pode ser deletado"

    def deletar_com_verificacao(self) -> tuple[bool, str]:
        pode, motivo = self.pode_ser_deletado()
        if not pode:
            return False, motivo

        return self.deletar()

    @staticmethod
    def listar_todos(limite: int = 100, incluir_inativos: bool = False) -> list['Livro']:
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            if incluir_inativos:
                query = "SELECT * FROM Livro ORDER BY Nome OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY"
                params = (limite,)
            else:
                query = "SELECT * FROM Livro WHERE Ativo = 1 ORDER BY Nome OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY"
                params = (limite,)

            resultados = db.execute_query(query, params)

            if resultados:
                return [Livro._from_db_row(row) for row in resultados]
            else:
                return []

        except Exception as e:
            print(f"✗ Erro ao listar livros: {e}")
            return []

    @staticmethod
    def buscar_por_isbn(isbn: str) -> Optional['Livro']:
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query = "SELECT * FROM Livro WHERE ISBN = ?"
            resultados = db.execute_query(query, (isbn,))

            if resultados:
                return Livro._from_db_row(resultados[0])
            else:
                return None

        except Exception as e:
            print(f"✗ Erro ao buscar livro por ISBN: {e}")
            return None

    @staticmethod
    def buscar_por_id(livro_id: int) -> Optional['Livro']:
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query = "SELECT * FROM Livro WHERE Id = ?"
            resultados = db.execute_query(query, (livro_id,))

            if resultados:
                return Livro._from_db_row(resultados[0])
            else:
                return None

        except Exception as e:
            print(f"✗ Erro ao buscar livro por ID: {e}")
            return None

    @staticmethod
    def _from_db_row(row) -> 'Livro':
        return Livro(
            id=row['Id'],
            nome=row['Nome'],
            autor=row['Autor'],
            isbn=row['ISBN'],
            genero=row['Genero'],
            data_cadastro=row['DataCadastro'],
            data_atualizacao=row['DataAtualizacao'],
            ativo=bool(row['Ativo'])
        )

    def _isbn_existe(self, db, isbn: str) -> bool:
        try:
            query = "SELECT COUNT(*) FROM Livro WHERE ISBN = ?"
            resultado = db.execute_scalar(query, (isbn,))
            return resultado and resultado > 0
        except:
            return False

    def _existe_por_id(self, db, livro_id: int) -> bool:
        try:
            query = "SELECT COUNT(*) FROM Livro WHERE Id = ?"
            resultado = db.execute_scalar(query, (livro_id,))
            return resultado and resultado > 0
        except:
            return False

    def _buscar_ultimo_id(self, db) -> Optional[int]:
        try:
            query = "SELECT SCOPE_IDENTITY()"
            resultado = db.execute_scalar(query)
            return int(resultado) if resultado else None
        except:
            return None
