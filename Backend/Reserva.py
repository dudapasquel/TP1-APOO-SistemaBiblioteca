from datetime import datetime
from typing import Optional, List
from enum import Enum


class StatusReserva(Enum):
    ATIVA = "Ativa"
    ATENDIDA = "Atendida"
    CANCELADA = "Cancelada"
    EXPIRADA = "Expirada"


class Reserva:
    FILAS_POR_LIVRO = {}

    def __init__(self, usuario_id: int, livro_id: int,
                 data_reserva: Optional[datetime] = None,
                 status: StatusReserva = StatusReserva.ATIVA,
                 id: Optional[int] = None):

        self.id = id
        self.usuario_id = usuario_id
        self.livro_id = livro_id
        self.data_reserva = data_reserva or datetime.now()
        self.status = status

    def salvar(self) -> tuple[bool, str]:
        """Registra a reserva no banco de dados."""
        try:
            from Banco_de_dados.connection import DatabaseConnection

            db = DatabaseConnection()

            check_query = """
                SELECT Id FROM Reserva
                WHERE UsuarioId = ? AND LivroId = ? AND Status = 'Ativa'
            """
            existing = db.execute_query(
                check_query, (self.usuario_id, self.livro_id))

            if existing:
                return False, "Usuário já possui uma reserva ativa para este livro"

            if self.id:

                update_query = """
                    UPDATE Reserva
                    SET Status = ?, DataReserva = ?
                    WHERE Id = ?
                """
                if db.execute_non_query(
                        update_query, (self.status.value, self.data_reserva, self.id)):
                    return True, "Reserva atualizada com sucesso"
                else:
                    return False, "Erro ao atualizar reserva"
            else:

                insert_query = """
                    INSERT INTO Reserva (UsuarioId, LivroId, DataReserva, Status)
                    VALUES (?, ?, ?, ?)
                """
                if db.execute_non_query(
                    insert_query,
                    (self.usuario_id,
                     self.livro_id,
                     self.data_reserva,
                     self.status.value)):

                    id_query = "SELECT @@IDENTITY as NovoId"
                    id_result = db.execute_query(id_query)
                    if id_result and len(id_result) > 0:
                        self.id = id_result[0].get('NovoId')
                    return True, "Reserva registrada com sucesso"
                else:
                    return False, "Erro ao salvar reserva no banco"

        except Exception as e:
            return False, f"Erro ao processar reserva: {e}"

    @staticmethod
    def proxima_para_livro(livro_id: int) -> Optional['Reserva']:
        """Retorna a próxima reserva ativa (primeiro da fila)."""
        fila = Reserva.FILAS_POR_LIVRO.get(livro_id, [])
        for reserva in fila:
            if reserva.status == StatusReserva.ATIVA:
                return reserva
        return None

    def cancelar(self) -> tuple[bool, str]:
        """Cancela uma reserva ativa."""
        if self.status != StatusReserva.ATIVA:
            return False, "Reserva não está ativa"
        self.status = StatusReserva.CANCELADA
        return True, "Reserva cancelada com sucesso"

    def marcar_atendida(self) -> tuple[bool, str]:
        """Marca a reserva como atendida (quando o livro é emprestado ao usuário)."""
        if self.status != StatusReserva.ATIVA:
            return False, "Reserva não está ativa"
        self.status = StatusReserva.ATENDIDA
        return True, "Reserva atendida com sucesso"

    @staticmethod
    def listar_por_livro(livro_id: int) -> List['Reserva']:
        """Lista todas as reservas (ativas, canceladas ou atendidas) de um livro."""
        return Reserva.FILAS_POR_LIVRO.get(livro_id, [])

    @staticmethod
    def listar_ativas(livro_id: int) -> List['Reserva']:
        """Lista apenas as reservas ativas do livro."""
        try:
            from Banco_de_dados.connection import DatabaseConnection

            db = DatabaseConnection()
            query = """
                SELECT Id, UsuarioId, LivroId, DataReserva, Status
                FROM Reserva
                WHERE LivroId = ? AND Status = 'Ativa'
                ORDER BY DataReserva ASC
            """

            result = db.execute_query(query, (livro_id,))
            reservas = []

            if result:
                for row in result:
                    reserva = Reserva(
                        usuario_id=row['UsuarioId'],
                        livro_id=row['LivroId'],
                        data_reserva=row['DataReserva'],
                        status=StatusReserva.ATIVA,
                        id=row['Id']
                    )
                    reservas.append(reserva)

            return reservas

        except Exception as e:
            print(f"Erro ao listar reservas ativas: {e}")
            return []

    def __repr__(self):
        return f"Reserva(usuario={self.usuario_id}, livro={self.livro_id}, status={self.status.value})"
