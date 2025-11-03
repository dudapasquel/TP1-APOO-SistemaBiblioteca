from datetime import datetime
from typing import Optional


class Avaliacao:

    def __init__(self, livro_id: int, usuario_id: int, nota: int,
                 comentario: Optional[str] = None, id: Optional[int] = None,
                 data_avaliacao: Optional[datetime] = None, ativa: bool = True,
                 emprestimo_id: Optional[int] = None):

        self._id = id
        self.livro_id = livro_id
        self.usuario_id = usuario_id
        self.nota = nota
        self.comentario = comentario
        self.data_avaliacao = data_avaliacao or datetime.now()
        self._ativa = ativa
        self.emprestimo_id = emprestimo_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor: int):
        self._id = valor

    @property
    def ativa(self):
        return self._ativa

    @ativa.setter
    def ativa(self, valor: bool):
        self._ativa = valor

    def validar(self) -> tuple[bool, str]:

        if not self.livro_id or self.livro_id <= 0:
            return False, "ID do livro é obrigatório"

        if not self.usuario_id or self.usuario_id <= 0:
            return False, "ID do usuário é obrigatório"

        if not self.nota or not (1 <= self.nota <= 5):
            return False, "Nota deve ser entre 1 e 5"

        if self.comentario and len(self.comentario) > 500:
            return False, "Comentário deve ter no máximo 500 caracteres"

        return True, "Avaliação válida"

    def salvar(self) -> tuple[bool, str]:

        from Banco_de_dados.connection import DatabaseConnection

        valido, mensagem = self.validar()
        if not valido:
            return False, f"Erro de validação: {mensagem}"

        db = DatabaseConnection()

        if self._usuario_ja_avaliou(db):
            return False, "Usuário já avaliou este livro"

        try:
            query = """INSERT INTO Avaliacao (LivroId, UsuarioId, Nota, Comentario, DataAvaliacao, EmprestimoId)
                      VALUES (?, ?, ?, ?, ?, ?)"""
            params = (self.livro_id, self.usuario_id, self.nota,
                      self.comentario, self.data_avaliacao, self.emprestimo_id)

            if db.execute_non_query(query, params):
                self.id = self._buscar_ultimo_id(db)
                return True, "Avaliação salva com sucesso!"
            else:
                return False, "Falha ao salvar avaliação"

        except Exception as e:
            return False, f"Erro ao salvar avaliação: {e}"

    def excluir(self) -> tuple[bool, str]:

        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID da avaliação é obrigatório"

        db = DatabaseConnection()

        try:
            query = "UPDATE Avaliacao SET Ativa = 0 WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                self.ativa = False
                return True, "Avaliação removida com sucesso!"
            else:
                return False, "Falha ao remover avaliação"

        except Exception as e:
            return False, f"Erro ao remover avaliação: {e}"

    @staticmethod
    def listar_por_livro(livro_id: int) -> list['Avaliacao']:

        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query = """SELECT Id, LivroId, UsuarioId, Nota, Comentario, DataAvaliacao, Ativa, EmprestimoId
                      FROM Avaliacao WHERE LivroId = ? AND Ativa = 1 ORDER BY DataAvaliacao DESC"""
            resultados = db.execute_query(query, (livro_id,))

            if resultados:
                return [Avaliacao._from_db_row(row) for row in resultados]
            else:
                return []

        except Exception as e:
            print(f"✗ Erro ao listar avaliações: {e}")
            return []

    @staticmethod
    def listar_por_emprestimo(emprestimo_id: int) -> list['Avaliacao']:
        """Lista avaliações de um empréstimo específico"""

        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query = """SELECT Id, LivroId, UsuarioId, Nota, Comentario, DataAvaliacao, Ativa, EmprestimoId
                      FROM Avaliacao WHERE EmprestimoId = ? AND Ativa = 1 ORDER BY DataAvaliacao DESC"""
            resultados = db.execute_query(query, (emprestimo_id,))

            if resultados:
                return [Avaliacao._from_db_row(row) for row in resultados]
            else:
                return []

        except Exception as e:
            print(f"✗ Erro ao listar avaliações por empréstimo: {e}")
            return []

    @staticmethod
    def listar_por_usuario(usuario_id: int) -> list[dict]:
        """Lista todas as avaliações feitas por um usuário com informações do livro"""
        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()
        try:
            query = """
                SELECT
                    a.Id, a.Nota, a.Comentario, a.DataAvaliacao, a.EmprestimoId,
                    l.Nome as LivroNome, l.Autor as LivroAutor, l.Id as LivroId
                FROM Avaliacao a
                INNER JOIN Livro l ON a.LivroId = l.Id
                WHERE a.UsuarioId = ? AND a.Ativa = 1
                ORDER BY a.DataAvaliacao DESC
            """

            resultados = db.execute_query(query, (usuario_id,))

            avaliacoes = []
            if resultados:
                for row in resultados:
                    if isinstance(row, dict):
                        avaliacao = {
                            'id': row.get('Id'),
                            'nota': row.get('Nota'),
                            'comentario': row.get('Comentario'),
                            'data_avaliacao': row.get('DataAvaliacao'),
                            'emprestimo_id': row.get('EmprestimoId'),
                            'livro_nome': row.get('LivroNome'),
                            'livro_autor': row.get('LivroAutor'),
                            'livro_id': row.get('LivroId')
                        }
                    else:
                        avaliacao = {
                            'id': row[0] if len(row) > 0 else None,
                            'nota': row[1] if len(row) > 1 else 0,
                            'comentario': row[2] if len(row) > 2 else None,
                            'data_avaliacao': row[3] if len(row) > 3 else None,
                            'emprestimo_id': row[4] if len(row) > 4 else None,
                            'livro_nome': row[5] if len(row) > 5 else 'N/A',
                            'livro_autor': row[6] if len(row) > 6 else 'N/A',
                            'livro_id': row[7] if len(row) > 7 else None
                        }
                    avaliacoes.append(avaliacao)

            return avaliacoes

        except Exception as e:
            print(f"Erro ao buscar avaliações do usuário: {e}")
            return []

    @staticmethod
    def calcular_media_livro(livro_id: int) -> float:

        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query = "SELECT AVG(CAST(Nota AS FLOAT)) as Media FROM Avaliacao WHERE LivroId = ? AND Ativa = 1"
            resultado = db.execute_query(query, (livro_id,))

            if resultado and len(resultado) > 0:
                if isinstance(resultado[0], dict):
                    media = resultado[0].get('Media') or resultado[0].get('')
                else:
                    media = resultado[0][0]

                if media is not None:
                    return round(float(media), 1)

            return 0.0

        except Exception as e:
            print(f"✗ Erro ao calcular média: {e}")
            return 0.0

    @staticmethod
    def _from_db_row(row) -> 'Avaliacao':

        if isinstance(row, dict):
            return Avaliacao(
                id=row.get('Id'),
                livro_id=row.get('LivroId'),
                usuario_id=row.get('UsuarioId'),
                nota=row.get('Nota'),
                comentario=row.get('Comentario'),
                data_avaliacao=row.get('DataAvaliacao'),
                ativa=bool(row.get('Ativa', True)),
                emprestimo_id=row.get('EmprestimoId')
            )
        else:
            return Avaliacao(
                id=row[0] if len(row) > 0 else None,
                livro_id=row[1] if len(row) > 1 else None,
                usuario_id=row[2] if len(row) > 2 else None,
                nota=row[3] if len(row) > 3 else None,
                comentario=row[4] if len(row) > 4 else None,
                data_avaliacao=row[5] if len(row) > 5 else None,
                ativa=bool(row[6]) if len(row) > 6 else True,
                emprestimo_id=row[7] if len(row) > 7 else None
            )

    def _usuario_ja_avaliou(self, db) -> bool:

        try:
            if self.emprestimo_id:
                query = "SELECT COUNT(*) FROM Avaliacao WHERE EmprestimoId = ? AND Ativa = 1"
                resultado = db.execute_query(query, (self.emprestimo_id,))
            else:
                query = "SELECT COUNT(*) FROM Avaliacao WHERE LivroId = ? AND UsuarioId = ? AND Ativa = 1"
                resultado = db.execute_query(
                    query, (self.livro_id, self.usuario_id))

            if resultado:
                if isinstance(resultado[0], dict):
                    return resultado[0].get('', 0) > 0
                else:
                    return resultado[0][0] > 0
            return False
        except Exception as e:
            print(f"Erro ao verificar duplicação: {e}")
            return False

    def _buscar_ultimo_id(self, db) -> Optional[int]:

        try:
            query = "SELECT SCOPE_IDENTITY()"
            resultado = db.execute_query(query)
            return int(resultado[0][0]) if resultado else None
        except BaseException:
            return None

    def __str__(self) -> str:
        return f"Avaliacao(id={self.id}, livro_id={self.livro_id}, nota={self.nota})"

    def __repr__(self) -> str:
        return f"Avaliacao(id={self.id}, livro_id={self.livro_id}, usuario_id={self.usuario_id}, nota={self.nota})"
