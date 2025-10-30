from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum
from Reserva import Reserva
from Notificacao import Notificacao, TipoNotificacao


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


class TipoUsuario(Enum):
    ALUNO = "Aluno"
    PROFESSOR = "Professor"


class Emprestimo:

    LIMITE_EMPRESTIMOS = {
        TipoUsuario.ALUNO: 3,
        TipoUsuario.PROFESSOR: 5
    }

    def __init__(self, usuario_id: int, livro_id: int, biblioteca_id: int,
                 dias_emprestimo: Optional[int] = None,
                 tipo: TipoEmprestimo = TipoEmprestimo.NORMAL,
                 tipo_usuario: TipoUsuario = TipoUsuario.ALUNO,
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
        self.tipo_usuario = tipo_usuario
        self.livro_id = livro_id
        self.biblioteca_id = biblioteca_id
        self.data_emprestimo = data_emprestimo or datetime.now()
        self.dias_emprestimo = self._definir_dias_emprestimo(dias_emprestimo)
        self.data_prevista_devolucao = data_prevista_devolucao or (
            self.data_emprestimo + timedelta(days=self.dias_emprestimo)
        )
        self.data_devolucao = data_devolucao
        self.status = status
        self.tipo = tipo
        self.valor_multa = valor_multa
        self.renovacoes = renovacoes
        self.max_renovacoes = max_renovacoes
        self.observacoes = observacoes

    
    def _definir_dias_emprestimo(self, dias: Optional[int]) -> int:
        if dias is not None:
            return dias
        if self.tipo_usuario == TipoUsuario.ALUNO:
            return 7
        return 14  # Professor

    @staticmethod
    def pode_emprestar(usuario_id: int, tipo_usuario: TipoUsuario, livro_id: int) -> tuple[bool, str]:
       
        emprestimos_ativos = Emprestimo.buscar_por_usuario(usuario_id, apenas_ativos=True)
        limite = Emprestimo.LIMITE_EMPRESTIMOS.get(tipo_usuario, 3)
        if len(emprestimos_ativos) >= limite:
            return False, f"Limite de {limite} empréstimos ativos atingido"

       
        reservas_ativas = Reserva.listar_ativas(livro_id)
        if reservas_ativas:
            primeira_reserva = reservas_ativas[0]
            if primeira_reserva.usuario_id != usuario_id:
                return False, "Livro reservado para outro usuário"
            #  Envia notificação de liberação
            Notificacao.enviar(
                usuario_id=usuario_id,
                tipo=TipoNotificacao.RESERVA,
                mensagem=f"O livro {livro_id} está disponível! Pode retirá-lo 😊"
            )

        return True, "Pode emprestar"

    def validar_dados(self) -> tuple[bool, str]:
        if self.usuario_id <= 0:
            return False, "ID do usuário inválido"
        if self.livro_id <= 0:
            return False, "ID do livro inválido"
        if self.biblioteca_id <= 0:
            return False, "ID da biblioteca inválido"
        if self.dias_emprestimo <= 0:
            return False, "Dias de empréstimo deve ser > 0"
        if self.renovacoes > self.max_renovacoes:
            return False, "Número de renovações excede o máximo"
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
        return max(0, dias * valor_diario)

    def atualizar_status(self) -> None:
        if self.data_devolucao:
            self.status = StatusEmprestimo.DEVOLVIDO
        elif self.esta_em_atraso():
            self.status = StatusEmprestimo.ATRASADO
            #  Notificação automática
            Notificacao.criar_notificacao_sistema(
                usuario_id=self.usuario_id,
                titulo="Empréstimo em atraso ⚠️",
                mensagem=f"O prazo para devolver o livro {self.livro_id} expirou.",
                livro_id=self.livro_id
            )
        else:
            self.status = StatusEmprestimo.ATIVO

  
    def pode_renovar(self) -> tuple[bool, str]:
        if self.status != StatusEmprestimo.ATIVO:
            return False, "Empréstimo não está ativo"

        reservas_ativas = Reserva.listar_ativas(self.livro_id)
        if reservas_ativas and reservas_ativas[0].usuario_id != self.usuario_id:
            return False, "Livro reservado para outro usuário"

        if self.renovacoes >= self.max_renovacoes:
            return False, "Limite de renovações atingido"

        return True, "Pode renovar"

    def renovar(self, dias_adicionais: int = 14) -> tuple[bool, str]:
        pode, motivo = self.pode_renovar()
        if not pode:
            return False, motivo
        self.renovacoes += 1
        self.data_prevista_devolucao += timedelta(days=dias_adicionais)
        self.status = StatusEmprestimo.RENOVADO
        Notificacao.criar_notificacao_sistema(
            usuario_id=self.usuario_id,
            titulo="Renovação confirmada 🔁",
            mensagem=f"Empréstimo do livro {self.livro_id} renovado por mais {dias_adicionais} dias.",
            livro_id=self.livro_id
        )
        return True, "Renovação registrada"

    
    def devolver(self, observacoes_devolucao: Optional[str] = None) -> tuple[bool, str]:
        if self.status in [StatusEmprestimo.DEVOLVIDO, StatusEmprestimo.CANCELADO]:
            return False, "Empréstimo já encerrado"

        self.data_devolucao = datetime.now()
        self.status = StatusEmprestimo.DEVOLVIDO

        if observacoes_devolucao:
            self.observacoes = (self.observacoes or "") + f"\nDevolução: {observacoes_devolucao}"

        if self.esta_em_atraso():
            self.valor_multa = self.calcular_multa()

        #  Notificação de devolução
        Notificacao.criar_notificacao_sistema(
            usuario_id=self.usuario_id,
            titulo="Devolução confirmada 📚",
            mensagem=f"O livro {self.livro_id} foi devolvido com sucesso! Obrigado 😊",
            livro_id=self.livro_id
        )

        proxima_reserva = Reserva.proxima_para_livro(self.livro_id)
        if proxima_reserva:
            Notificacao.criar_notificacao_sistema(
                usuario_id=proxima_reserva.usuario_id,
                titulo="📚 Livro disponível para retirada",
                mensagem=f"O livro {self.livro_id} está disponível! Retire em até 24h.",
                livro_id=self.livro_id
            )

        return True, "Devolução registrada com sucesso"

    
    def cancelar(self, motivo: str) -> tuple[bool, str]:
        if self.status == StatusEmprestimo.DEVOLVIDO:
            return False, "Não é possível cancelar empréstimo devolvido"
        self.status = StatusEmprestimo.CANCELADO
        self.observacoes = (self.observacoes or "") + f"\nCancelado: {motivo}"
        return True, "Empréstimo cancelado"

    def salvar(self) -> tuple[bool, str]:
        valido, msg = self.validar_dados()
        if not valido:
            return False, msg
        self.atualizar_status()
        return True, "Empréstimo salvo com sucesso"

    
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

    @staticmethod
    def verificar_vencimentos_proximos(lista_emprestimos: List['Emprestimo'], dias_aviso: int = 1):
        hoje = datetime.now()
        for emp in lista_emprestimos:
            if emp.status == StatusEmprestimo.ATIVO:
                dias_restantes = (emp.data_prevista_devolucao - hoje).days
                if dias_restantes == dias_aviso:
                    Notificacao.criar_notificacao_sistema(
                        usuario_id=emp.usuario_id,
                        titulo="Vencimento próximo ⏳",
                        mensagem=f"O prazo do livro {emp.livro_id} termina em {dias_restantes} dia(s).",
                        livro_id=emp.livro_id
                    )
