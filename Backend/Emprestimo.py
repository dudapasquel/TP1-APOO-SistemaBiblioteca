
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum

class StatusEmprestimo(Enum):

    ATIVO = "Ativo"
    DEVOLVIDO = "Devolvido"
    ATRASADO = "Atrasado"
    RENOVADO = "Renovado"
    CANCELADO = "Cancelado"

class TipoEmprestimo(Enum):

    NORMAL = "Normal"
    RESERVA = "Reserva"
    RENOVACAO = "Renovação"

class Emprestimo:

    def __init__(self, usuario_id: int, livro_id: int, biblioteca_id: int,
                 dias_emprestimo: int = 14, tipo: TipoEmprestimo = TipoEmprestimo.NORMAL,
                 observacoes: Optional[str] = None,
                 id: Optional[int] = None,
                 data_emprestimo: Optional[datetime] = None,
                 data_prevista_devolucao: Optional[datetime] = None,
                 data_devolucao: Optional[datetime] = None,
                 status: StatusEmprestimo = StatusEmprestimo.ATIVO,
                 valor_multa: float = 0.0, renovacoes: int = 0,
                 max_renovacoes: int = 2):

        self.id = id
        self.usuario_id = usuario_id
        self.livro_id = livro_id
        self.biblioteca_id = biblioteca_id
        self.data_emprestimo = data_emprestimo or datetime.now()
        self.dias_emprestimo = dias_emprestimo
        self.data_prevista_devolucao = data_prevista_devolucao or (
            self.data_emprestimo + timedelta(days=dias_emprestimo)
        )
        self.data_devolucao = data_devolucao
        self.status = status
        self.tipo = tipo
        self.valor_multa = valor_multa
        self.renovacoes = renovacoes
        self.max_renovacoes = max_renovacoes
        self.observacoes = observacoes

    def validar_dados(self) -> tuple[bool, str]:

        if self.usuario_id <= 0:
            return False, "ID do usuário deve ser válido"

        if self.livro_id <= 0:
            return False, "ID do livro deve ser válido"

        if self.biblioteca_id <= 0:
            return False, "ID da biblioteca deve ser válido"

        if self.dias_emprestimo <= 0:
            return False, "Dias de empréstimo deve ser maior que zero"

        if self.max_renovacoes < 0:
            return False, "Máximo de renovações não pode ser negativo"

        if self.renovacoes < 0:
            return False, "Número de renovações não pode ser negativo"

        if self.renovacoes > self.max_renovacoes:
            return False, "Número de renovações excede o máximo permitido"

        if self.valor_multa < 0:
            return False, "Valor da multa não pode ser negativo"

        return True, "Dados válidos"

    def esta_em_atraso(self) -> bool:

        if self.status == StatusEmprestimo.DEVOLVIDO:
            return False

        return datetime.now() > self.data_prevista_devolucao

    def dias_atraso(self) -> int:

        if not self.esta_em_atraso():
            return 0

        return (datetime.now() - self.data_prevista_devolucao).days

    def calcular_multa(self, valor_diario: float = 2.0) -> float:

        dias = self.dias_atraso()
        if dias <= 0:
            return 0.0

        return dias * valor_diario

    def atualizar_status(self) -> None:

        if self.data_devolucao:
            self.status = StatusEmprestimo.DEVOLVIDO
        elif self.esta_em_atraso():
            self.status = StatusEmprestimo.ATRASADO
        else:
            self.status = StatusEmprestimo.ATIVO

    def pode_renovar(self) -> tuple[bool, str]:

        if self.status == StatusEmprestimo.DEVOLVIDO:
            return False, "Empréstimo já foi devolvido"

        if self.status == StatusEmprestimo.CANCELADO:
            return False, "Empréstimo foi cancelado"

        if self.renovacoes >= self.max_renovacoes:
            return False, f"Limite de renovações atingido ({self.max_renovacoes})"

        if self.esta_em_atraso():
            return False, "Não é possível renovar empréstimo em atraso"

        return True, "Pode ser renovado"

    def renovar(self, dias_adicionais: int = 14) -> tuple[bool, str]:

        pode, motivo = self.pode_renovar()
        if not pode:
            return False, motivo

        try:
            self.renovacoes += 1
            self.data_prevista_devolucao += timedelta(days=dias_adicionais)
            self.status = StatusEmprestimo.RENOVADO
            self.data_atualizacao = datetime.now()

            return True, f"Empréstimo renovado por {dias_adicionais} dias"
        except Exception as e:
            return False, f"Erro ao renovar empréstimo: {e}"

    def devolver(self, observacoes_devolucao: Optional[str] = None) -> tuple[bool, str]:

        if self.status == StatusEmprestimo.DEVOLVIDO:
            return False, "Livro já foi devolvido"

        if self.status == StatusEmprestimo.CANCELADO:
            return False, "Empréstimo foi cancelado"

        try:
            self.data_devolucao = datetime.now()
            self.status = StatusEmprestimo.DEVOLVIDO

            if observacoes_devolucao:
                self.observacoes = (self.observacoes or "") + f"\nDevolução: {observacoes_devolucao}"

            if self.esta_em_atraso():
                self.valor_multa = self.calcular_multa()

            return True, "Devolução registrada com sucesso"
        except Exception as e:
            return False, f"Erro ao registrar devolução: {e}"

    def cancelar(self, motivo: str) -> tuple[bool, str]:

        if self.status == StatusEmprestimo.DEVOLVIDO:
            return False, "Não é possível cancelar empréstimo devolvido"

        try:
            self.status = StatusEmprestimo.CANCELADO
            self.observacoes = (self.observacoes or "") + f"\nCancelado: {motivo}"
            self.data_atualizacao = datetime.now()

            return True, "Empréstimo cancelado com sucesso"
        except Exception as e:
            return False, f"Erro ao cancelar empréstimo: {e}"

    def salvar(self) -> tuple[bool, str]:

        valido, mensagem = self.validar_dados()
        if not valido:
            return False, f"Erro de validação: {mensagem}"

        try:
            self.atualizar_status()

            if self.id:
                self.data_atualizacao = datetime.now()
                return True, "Empréstimo atualizado com sucesso"
            else:
                self.id = 1
                return True, "Empréstimo registrado com sucesso"
        except Exception as e:
            return False, f"Erro ao salvar empréstimo: {e}"

    def obter_dias_restantes(self) -> int:

        if self.status == StatusEmprestimo.DEVOLVIDO:
            return 0

        return (self.data_prevista_devolucao - datetime.now()).days

    def __str__(self) -> str:

        return f"Empréstimo {self.id} - Usuário {self.usuario_id} - Livro {self.livro_id} - {self.status.value}"

    def __repr__(self) -> str:

        return f"Emprestimo(id={self.id}, usuario_id={self.usuario_id}, livro_id={self.livro_id}, status='{self.status.value}')"

    @staticmethod
    def listar_todos(limite: int = 100, incluir_devolvidos: bool = False) -> List['Emprestimo']:

        return []

    @staticmethod
    def buscar_por_usuario(usuario_id: int, apenas_ativos: bool = True) -> List['Emprestimo']:

        return []

    @staticmethod
    def buscar_por_livro(livro_id: int) -> List['Emprestimo']:

        return []

    @staticmethod
    def buscar_atrasados() -> List['Emprestimo']:

        return []

    @staticmethod
    def buscar_por_id(emprestimo_id: int) -> Optional['Emprestimo']:

        return None

    @staticmethod
    def estatisticas_biblioteca(biblioteca_id: int) -> dict:

        return {
            'total_emprestimos': 0,
            'emprestimos_ativos': 0,
            'emprestimos_atrasados': 0,
            'total_multas': 0.0
        }
