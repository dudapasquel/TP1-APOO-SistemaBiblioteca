
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoNotificacao(Enum):

    EMPRESTIMO = "EMPRESTIMO"
    DEVOLUCAO = "DEVOLUCAO"
    RESERVA = "RESERVA"
    MULTA = "MULTA"
    SISTEMA = "SISTEMA"
    PROMOCAO = "PROMOCAO"

class StatusNotificacao(Enum):

    NAO_LIDA = "NAO_LIDA"
    LIDA = "LIDA"
    ARQUIVADA = "ARQUIVADA"

class Notificacao:

    def __init__(self, usuario_id: int, tipo: TipoNotificacao, titulo: str, mensagem: str,
                 id: Optional[int] = None, status: StatusNotificacao = StatusNotificacao.NAO_LIDA,
                 data_criacao: Optional[datetime] = None, data_leitura: Optional[datetime] = None,
                 ativa: bool = True, livro_id: Optional[int] = None):

        self.id = id
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.titulo = titulo
        self.mensagem = mensagem
        self.status = status
        self.data_criacao = data_criacao or datetime.now()
        self.data_leitura = data_leitura
        self.ativa = ativa
        self.livro_id = livro_id

    def validar(self) -> tuple[bool, str]:

        if not self.usuario_id or self.usuario_id <= 0:
            return False, "ID do usuário é obrigatório"

        if not self.titulo or len(self.titulo.strip()) < 3:
            return False, "Título deve ter pelo menos 3 caracteres"

        if not self.mensagem or len(self.mensagem.strip()) < 5:
            return False, "Mensagem deve ter pelo menos 5 caracteres"

        if len(self.titulo) > 100:
            return False, "Título deve ter no máximo 100 caracteres"

        if len(self.mensagem) > 1000:
            return False, "Mensagem deve ter no máximo 1000 caracteres"

        return True, "Notificação válida"

    def salvar(self) -> tuple[bool, str]:

        from Banco_de_dados.connection import DatabaseConnection

        valido, mensagem = self.validar()
        if not valido:
            return False, f"Erro de validação: {mensagem}"

        db = DatabaseConnection()

        try:
            query =
            params = (self.usuario_id, self.tipo.value, self.titulo, self.mensagem,
                     self.status.value, self.data_criacao, self.livro_id)

            if db.execute_non_query(query, params):
                self.id = self._buscar_ultimo_id(db)
                return True, "Notificação criada com sucesso!"
            else:
                return False, "Falha ao criar notificação"

        except Exception as e:
            return False, f"Erro ao criar notificação: {e}"

    def marcar_como_lida(self) -> tuple[bool, str]:

        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID da notificação é obrigatório"

        db = DatabaseConnection()

        try:
            query =
            self.data_leitura = datetime.now()
            self.status = StatusNotificacao.LIDA

            params = (self.status.value, self.data_leitura, self.id)

            if db.execute_non_query(query, params):
                return True, "Notificação marcada como lida!"
            else:
                return False, "Falha ao marcar como lida"

        except Exception as e:
            return False, f"Erro ao marcar como lida: {e}"

    def arquivar(self) -> tuple[bool, str]:

        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID da notificação é obrigatório"

        db = DatabaseConnection()

        try:
            query = "UPDATE Notificacao SET Status = ? WHERE Id = ?"
            self.status = StatusNotificacao.ARQUIVADA

            if db.execute_non_query(query, (self.status.value, self.id)):
                return True, "Notificação arquivada!"
            else:
                return False, "Falha ao arquivar notificação"

        except Exception as e:
            return False, f"Erro ao arquivar: {e}"

    def excluir(self) -> tuple[bool, str]:

        from Banco_de_dados.connection import DatabaseConnection

        if not self.id:
            return False, "ID da notificação é obrigatório"

        db = DatabaseConnection()

        try:
            query = "UPDATE Notificacao SET Ativa = 0 WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                self.ativa = False
                return True, "Notificação excluída!"
            else:
                return False, "Falha ao excluir notificação"

        except Exception as e:
            return False, f"Erro ao excluir: {e}"

    @staticmethod
    def listar_por_usuario(usuario_id: int, apenas_nao_lidas: bool = False) -> list['Notificacao']:

        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            if apenas_nao_lidas:
                query =
                params = (usuario_id, StatusNotificacao.NAO_LIDA.value)
            else:
                query =
                params = (usuario_id,)

            resultados = db.execute_query(query, params)

            if resultados:
                return [Notificacao._from_db_row(row) for row in resultados]
            else:
                return []

        except Exception as e:
            print(f"✗ Erro ao listar notificações: {e}")
            return []

    @staticmethod
    def contar_nao_lidas(usuario_id: int) -> int:

        from Banco_de_dados.connection import DatabaseConnection

        db = DatabaseConnection()

        try:
            query =
            resultado = db.execute_query(query, (usuario_id, StatusNotificacao.NAO_LIDA.value))

            return resultado[0][0] if resultado else 0

        except Exception as e:
            print(f"✗ Erro ao contar notificações: {e}")
            return 0

    @staticmethod
    def criar_notificacao_sistema(usuario_id: int, titulo: str, mensagem: str,
                                 livro_id: Optional[int] = None) -> 'Notificacao':

        notificacao = Notificacao(
            usuario_id=usuario_id,
            tipo=TipoNotificacao.SISTEMA,
            titulo=titulo,
            mensagem=mensagem,
            livro_id=livro_id
        )
        notificacao.salvar()
        return notificacao

    @staticmethod
    def _from_db_row(row) -> 'Notificacao':

        return Notificacao(
            id=row[0],
            usuario_id=row[1],
            tipo=TipoNotificacao(row[2]),
            titulo=row[3],
            mensagem=row[4],
            status=StatusNotificacao(row[5]),
            data_criacao=row[6],
            data_leitura=row[7],
            ativa=bool(row[8]),
            livro_id=row[9]
        )

    def _buscar_ultimo_id(self, db) -> Optional[int]:

        try:
            query = "SELECT SCOPE_IDENTITY()"
            resultado = db.execute_query(query)
            return int(resultado[0][0]) if resultado else None
        except:
            return None

    def __str__(self) -> str:
        return f"Notificacao(id={self.id}, usuario_id={self.usuario_id}, tipo={self.tipo.value})"

    def __repr__(self) -> str:
        return f"Notificacao(id={self.id}, usuario_id={self.usuario_id}, titulo='{self.titulo}', status={self.status.value})"
