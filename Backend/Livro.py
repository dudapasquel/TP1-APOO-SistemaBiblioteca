from datetime import datetime
from typing import Optional

import sys
sys.modules.setdefault('Backend.livro', sys.modules.get(__name__))


class Livro:

    def __init__(
            self,
            nome: str,
            autor: str,
            isbn: str,
            genero: str,
            id: Optional[int] = None,
            data_cadastro: Optional[datetime] = None,
            data_atualizacao: Optional[datetime] = None,
            ativo: bool = True,
            quantidade_total: int = 5,
            quantidade_disponivel: Optional[int] = None,
            quantidade_emprestada: Optional[int] = None):
        self._id = id
        self._nome = nome
        self.autor = autor
        self._isbn = isbn
        self.genero = genero
        self.data_cadastro = data_cadastro
        self.data_atualizacao = data_atualizacao
        self._ativo = ativo
        self.quantidade_total = quantidade_total
        self._quantidade_disponivel = quantidade_disponivel
        self._quantidade_emprestada = quantidade_emprestada

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

    @property
    def quantidade_disponivel(self) -> int:
        """Retorna a quantidade disponível para empréstimo"""
        if self._quantidade_disponivel is not None:
            return self._quantidade_disponivel

        return max(0, self.quantidade_total -
                   (self._quantidade_emprestada or 0))

    @property
    def quantidade_emprestada(self) -> int:
        """Retorna a quantidade atualmente emprestada"""
        if self._quantidade_emprestada is not None:
            return self._quantidade_emprestada

        return max(0, self.quantidade_total -
                   (self._quantidade_disponivel or self.quantidade_total))

    @property
    def disponivel_para_emprestimo(self) -> bool:
        """Verifica se há exemplares disponíveis para empréstimo"""
        return self.quantidade_disponivel > 0 and self.ativo

    def __str__(self) -> str:
        return f"Livro(id={self.id}, nome='{self.nome}', autor='{self.autor}', isbn='{self.isbn}')"

    def __repr__(self) -> str:
        return (
            f"Livro(id={self.id}, nome='{self.nome}', autor='{self.autor}', "
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
            'ativo': self.ativo,
            'quantidade_total': self.quantidade_total,
            'quantidade_disponivel': self.quantidade_disponivel,
            'quantidade_emprestada': self.quantidade_emprestada,
            'disponivel_para_emprestimo': self.disponivel_para_emprestimo}

    @classmethod
    def from_dict(cls, data: dict) -> 'Livro':
        return cls(
            id=data.get('id'),
            nome=data['nome'],
            autor=data['autor'],
            isbn=data['isbn'],
            genero=data['genero'],
            data_cadastro=datetime.fromisoformat(
                data['data_cadastro']) if data.get('data_cadastro') else None,
            data_atualizacao=datetime.fromisoformat(
                data['data_atualizacao']) if data.get('data_atualizacao') else None,
            ativo=data.get(
                'ativo',
                True))

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
    def listar_todos(
            limite: int = 100,
            incluir_inativos: bool = False) -> list['Livro']:
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:

            if incluir_inativos:
                query = """
                SELECT Id, Nome, Autor, ISBN, Genero, QuantidadeTotal,
                       QuantidadeEmprestada, QuantidadeDisponivel, Ativo, DataCadastro
                FROM VW_EstoqueLivros
                ORDER BY Nome
                OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
                """
                params = (limite,)
            else:
                query = """
                SELECT Id, Nome, Autor, ISBN, Genero, QuantidadeTotal,
                       QuantidadeEmprestada, QuantidadeDisponivel, Ativo, DataCadastro
                FROM VW_EstoqueLivros
                WHERE Ativo = 1
                ORDER BY Nome
                OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
                """
                params = (limite,)

            resultados = db.execute_query(query, params)

            if resultados:
                return [Livro._from_estoque_row(row) for row in resultados]
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

        quantidade_total = row.get(
            'QuantidadeTotal',
            5) if isinstance(
            row,
            dict) else getattr(
            row,
            'QuantidadeTotal',
            5)
        return Livro(
            id=row['Id'] if isinstance(row, dict) else row[0],
            nome=row['Nome'] if isinstance(row, dict) else row[1],
            autor=row['Autor'] if isinstance(row, dict) else row[2],
            isbn=row['ISBN'] if isinstance(row, dict) else row[3],
            genero=row['Genero'] if isinstance(row, dict) else row[4],
            data_cadastro=row['DataCadastro'] if isinstance(row, dict) else row[5],
            data_atualizacao=row['DataAtualizacao'] if isinstance(row, dict) else row[6],
            ativo=bool(row['Ativo'] if isinstance(row, dict) else row[7]),
            quantidade_total=quantidade_total
        )

    @staticmethod
    def _from_estoque_row(row) -> 'Livro':

        if isinstance(row, dict):
            return Livro(
                id=row['Id'],
                nome=row['Nome'],
                autor=row['Autor'],
                isbn=row['ISBN'],
                genero=row['Genero'],
                data_cadastro=row['DataCadastro'],
                ativo=bool(row['Ativo']),
                quantidade_total=row['QuantidadeTotal'],
                quantidade_disponivel=row['QuantidadeDisponivel'],
                quantidade_emprestada=row['QuantidadeEmprestada']
            )
        else:

            return Livro(
                id=row[0],
                nome=row[1],
                autor=row[2],
                isbn=row[3],
                genero=row[4],
                quantidade_total=row[5],
                quantidade_emprestada=row[6],
                quantidade_disponivel=row[7],
                ativo=bool(row[8]),
                data_cadastro=row[9]
            )

    def _isbn_existe(self, db, isbn: str) -> bool:
        try:
            query = "SELECT COUNT(*) FROM Livro WHERE ISBN = ?"
            resultado = db.execute_scalar(query, (isbn,))
            return resultado and resultado > 0
        except BaseException:
            return False

    def _existe_por_id(self, db, livro_id: int) -> bool:
        try:
            query = "SELECT COUNT(*) FROM Livro WHERE Id = ?"
            resultado = db.execute_scalar(query, (livro_id,))
            return resultado and resultado > 0
        except BaseException:
            return False

    def _buscar_ultimo_id(self, db) -> Optional[int]:
        try:
            query = "SELECT SCOPE_IDENTITY()"
            resultado = db.execute_scalar(query)
            return int(resultado) if resultado else None
        except BaseException:
            return None

    @staticmethod
    def listar_com_estoque() -> list['Livro']:
        """Lista todos os livros ativos com informações de estoque"""
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()
        try:
            query = """
                SELECT Id, Nome, Autor, ISBN, Genero, QuantidadeTotal,
                       QuantidadeEmprestada, QuantidadeDisponivel, Ativo, DataCadastro
                FROM VW_EstoqueLivros
                WHERE Ativo = 1
                ORDER BY Nome
            """

            resultados = db.execute_query(query)
            return [Livro._from_estoque_row(row) for row in resultados]

        except Exception as e:
            print(f"Erro ao listar livros com estoque: {e}")
            return []
        finally:
            db.close()
