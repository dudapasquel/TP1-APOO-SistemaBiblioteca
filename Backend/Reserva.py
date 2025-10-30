from datetime import datetime
from typing import Optional, List
from enum import Enum


class StatusReserva(Enum):
    ATIVA = "Ativa"
    ATENDIDA = "Atendida"
    CANCELADA = "Cancelada"
    EXPIRADA = "Expirada"


class Reserva:
    # Fila de reservas por livro: {livro_id: [reservas em ordem de chegada]}
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

    # ---------- MÉTODOS PRINCIPAIS ----------

    def salvar(self) -> tuple[bool, str]:
        """Registra a reserva e adiciona o usuário à fila do livro."""
        if self.livro_id not in Reserva.FILAS_POR_LIVRO:
            Reserva.FILAS_POR_LIVRO[self.livro_id] = []

        fila = Reserva.FILAS_POR_LIVRO[self.livro_id]

        # Evita duplicidade de reservas ativas para o mesmo livro e usuário
        for r in fila:
            if r.usuario_id == self.usuario_id and r.status == StatusReserva.ATIVA:
                return False, "Usuário já possui uma reserva ativa para este livro"

        fila.append(self)
        fila.sort(key=lambda r: r.data_reserva)
        return True, "Reserva registrada com sucesso"

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

    # ---------- MÉTODOS AUXILIARES ----------

    @staticmethod
    def listar_por_livro(livro_id: int) -> List['Reserva']:
        """Lista todas as reservas (ativas, canceladas ou atendidas) de um livro."""
        return Reserva.FILAS_POR_LIVRO.get(livro_id, [])

    @staticmethod
    def listar_ativas(livro_id: int) -> List['Reserva']:
        """Lista apenas as reservas ativas do livro."""
        return [r for r in Reserva.FILAS_POR_LIVRO.get(livro_id, []) if r.status == StatusReserva.ATIVA]

    def __repr__(self):
        return f"Reserva(usuario={self.usuario_id}, livro={self.livro_id}, status={self.status.value})"

    # dicionário {livro_id: [Reservas em ordem de chegada]}
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

    # ---------- MÉTODOS PRINCIPAIS ----------

    def salvar(self) -> tuple[bool, str]:
        """Registra a reserva e adiciona o usuário à fila do livro."""
        if self.livro_id not in Reserva.FILAS_POR_LIVRO:
            Reserva.FILAS_POR_LIVRO[self.livro_id] = []

        fila = Reserva.FILAS_POR_LIVRO[self.livro_id]

        # evitar reservas duplicadas
        for r in fila:
            if r.usuario_id == self.usuario_id and r.status == StatusReserva.ATIVA:
                return False, "Usuário já possui uma reserva ativa para este livro"

        fila.append(self)
        fila.sort(key=lambda r: r.data_reserva)
        return True, "Reserva registrada com sucesso"

    @staticmethod
    def proxima_reserva(livro_id: int) -> Optional['Reserva']:
        """Retorna a próxima reserva ativa (primeiro da fila)."""
        fila = Reserva.FILAS_POR_LIVRO.get(livro_id, [])
        for reserva in fila:
            if reserva.status == StatusReserva.ATIVA:
                return reserva
        return None

    def cancelar(self) -> tuple[bool, str]:
        """Cancela a reserva."""
        if self.status != StatusReserva.ATIVA:
            return False, "Reserva não está ativa"
        self.status = StatusReserva.CANCELADA
        return True, "Reserva cancelada com sucesso"

    def marcar_atendida(self) -> tuple[bool, str]:
        """Marca a reserva como atendida (quando o usuário pega o livro)."""
        if self.status != StatusReserva.ATIVA:
            return False, "Reserva não está ativa"
        self.status = StatusReserva.ATENDIDA
        return True, "Reserva atendida com sucesso"

    # ---------- MÉTODOS AUXILIARES ----------

    @staticmethod
    def listar_por_livro(livro_id: int) -> List['Reserva']:
        """Lista todas as reservas (ativas, canceladas ou atendidas) de um livro."""
        return Reserva.FILAS_POR_LIVRO.get(livro_id, [])

    @staticmethod
    def listar_ativas(livro_id: int) -> List['Reserva']:
        """Lista apenas as reservas ativas do livro."""
        return [r for r in Reserva.FILAS_POR_LIVRO.get(livro_id, []) if r.status == StatusReserva.ATIVA]

    def __repr__(self):
        return f"Reserva(usuario={self.usuario_id}, livro={self.livro_id}, status={self.status.value})"
