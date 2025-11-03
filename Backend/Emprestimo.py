
from datetime import datetime, timedelta
from typing import Optional, List
from enum import Enum


class StatusEmprestimo(Enum):
    ATIVO = "Emprestado"
    EMPRESTADO = "Emprestado"
    DEVOLVIDO = "Devolvido"
    ATRASADO = "Atrasado"
    RENOVADO = "Renovado"
    CANCELADO = "Cancelado"


class TipoEmprestimo(Enum):

    NORMAL = "Normal"
    RESERVA = "Reserva"
    RENOVACAO = "Renovação"


class Emprestimo:

    def __init__(
            self,
            usuario_id: int,
            livro_id: int,
            biblioteca_id: int,
            dias_emprestimo: int = 14,
            tipo: TipoEmprestimo = TipoEmprestimo.NORMAL,
            observacoes: Optional[str] = None,
            id: Optional[int] = None,
            data_emprestimo: Optional[datetime] = None,
            data_prevista_devolucao: Optional[datetime] = None,
            data_devolucao: Optional[datetime] = None,
            status: StatusEmprestimo = StatusEmprestimo.ATIVO,
            valor_multa: float = 0.0,
            renovacoes: int = 0,
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

    def devolver(self,
                 data_devolucao: Optional[datetime] = None,
                 observacoes_devolucao: Optional[str] = None) -> tuple[bool,
                                                                       str]:
        """Marca o empréstimo como devolvido e salva no banco"""
        if self.status == StatusEmprestimo.DEVOLVIDO:
            return False, "Livro já foi devolvido"

        if self.status == StatusEmprestimo.CANCELADO:
            return False, "Empréstimo foi cancelado"

        try:
            from Banco_de_dados.connection import DatabaseConnection

            self.data_devolucao = data_devolucao or datetime.now()
            self.status = StatusEmprestimo.DEVOLVIDO

            if observacoes_devolucao:
                self.observacoes = (self.observacoes or "") + \
                    f"\nDevolução: {observacoes_devolucao}"

            db = DatabaseConnection()
            query = """
            UPDATE Emprestimo
            SET DataDevolucao = ?, Status = 'Devolvido', Observacoes = ?
            WHERE Id = ?
            """

            if db.execute_non_query(
                    query, (self.data_devolucao, self.observacoes, self.id)):
                return True, "Devolução registrada com sucesso"
            else:
                return False, "Erro ao salvar devolução no banco"
        except Exception as e:
            return False, f"Erro ao registrar devolução: {e}"

    def cancelar(self, motivo: str) -> tuple[bool, str]:

        if self.status == StatusEmprestimo.DEVOLVIDO:
            return False, "Não é possível cancelar empréstimo devolvido"

        try:
            self.status = StatusEmprestimo.CANCELADO
            self.observacoes = (self.observacoes or "") + \
                f"\nCancelado: {motivo}"
            self.data_atualizacao = datetime.now()

            return True, "Empréstimo cancelado com sucesso"
        except Exception as e:
            return False, f"Erro ao cancelar empréstimo: {e}"

    def salvar(self) -> tuple[bool, str]:
        """Salva o empréstimo no banco de dados"""
        valido, mensagem = self.validar_dados()
        if not valido:
            return False, f"Erro de validação: {mensagem}"

        try:
            from Banco_de_dados.connection import DatabaseConnection

            self.atualizar_status()
            db = DatabaseConnection()

            if self.id:

                query = """
                UPDATE Emprestimo
                SET UsuarioId = ?, LivroId = ?, DataEmprestimo = ?,
                    DataPrevistaDevolucao = ?, DataDevolucao = ?,
                    Status = ?, Observacoes = ?
                WHERE Id = ?
                """
                params = (
                    self.usuario_id, self.livro_id, self.data_emprestimo,
                    self.data_prevista_devolucao, self.data_devolucao,
                    self.status.value, self.observacoes, self.id
                )

                if db.execute_non_query(query, params):
                    return True, "Empréstimo atualizado com sucesso"
                else:
                    return False, "Erro ao atualizar empréstimo no banco"
            else:

                limite_check_query = """
                SELECT COUNT(*) as TotalAtivos
                FROM Emprestimo
                WHERE UsuarioId = ? AND Status IN ('Emprestado', 'Atrasado')
                """
                limite_result = db.execute_query(
                    limite_check_query, (self.usuario_id,))

                if limite_result and len(limite_result) > 0:
                    total_ativos = limite_result[0].get('TotalAtivos', 0)
                    limite_emprestimos = 3

                    if total_ativos >= limite_emprestimos:
                        return False, f"Usuário já atingiu o limite de {limite_emprestimos} empréstimos simultâneos"

                disponibilidade_query = """
                SELECT
                    l.Quantidade,
                    ISNULL((SELECT COUNT(*) FROM Emprestimo e WHERE e.LivroId = l.Id AND e.Status IN ('Emprestado', 'Atrasado')), 0) as Emprestados
                FROM Livro l
                WHERE l.Id = ?
                """
                disp_result = db.execute_query(
                    disponibilidade_query, (self.livro_id,))

                if disp_result and len(disp_result) > 0:
                    quantidade_total = disp_result[0].get('Quantidade', 0)
                    emprestados = disp_result[0].get('Emprestados', 0)
                    disponivel = quantidade_total - emprestados

                    if disponivel <= 0:
                        return False, "Livro não está disponível para empréstimo"

                query = """
                INSERT INTO Emprestimo (UsuarioId, LivroId, DataEmprestimo, DataPrevistaDevolucao, Status, Observacoes)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                params = (
                    self.usuario_id,
                    self.livro_id,
                    self.data_emprestimo,
                    self.data_prevista_devolucao,
                    self.status.value,
                    self.observacoes)

                result = db.execute_non_query(query, params)
                if result:

                    id_query = "SELECT @@IDENTITY as NovoId"
                    id_result = db.execute_query(id_query)
                    if id_result and len(id_result) > 0:
                        self.id = id_result[0].get('NovoId')
                    return True, "Empréstimo registrado com sucesso"
                else:
                    return False, "Erro ao salvar empréstimo no banco"

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
    def listar_todos(
            limite: int = 100,
            incluir_devolvidos: bool = False) -> List['Emprestimo']:

        return []

    @staticmethod
    def buscar_por_usuario(
            usuario_id: int,
            apenas_ativos: bool = True) -> List['Emprestimo']:
        """Busca empréstimos por usuário - alias para listar_por_usuario"""
        return Emprestimo.listar_por_usuario(usuario_id, apenas_ativos)

    @staticmethod
    def listar_por_usuario(
            usuario_id: int,
            apenas_ativos: bool = True) -> List['Emprestimo']:
        """Lista empréstimos de um usuário específico"""
        try:
            from Banco_de_dados.connection import DatabaseConnection

            db = DatabaseConnection()
            if apenas_ativos:
                query = """
                SELECT Id, UsuarioId, LivroId, DataEmprestimo, DataPrevistaDevolucao,
                       DataDevolucao, Status, Observacoes
                FROM Emprestimo
                WHERE UsuarioId = ? AND Status != 'Devolvido'
                ORDER BY DataEmprestimo DESC
                """
            else:
                query = """
                SELECT Id, UsuarioId, LivroId, DataEmprestimo, DataPrevistaDevolucao,
                       DataDevolucao, Status, Observacoes
                FROM Emprestimo
                WHERE UsuarioId = ?
                ORDER BY DataEmprestimo DESC
                """

            result = db.execute_query(query, (usuario_id,))

            emprestimos = []
            if result:
                for row in result:
                    emprestimo = Emprestimo(
                        usuario_id=row['UsuarioId'],
                        livro_id=row['LivroId'],
                        biblioteca_id=1
                    )
                    emprestimo.id = row['Id']
                    emprestimo.data_emprestimo = row['DataEmprestimo']
                    emprestimo.data_prevista_devolucao = row['DataPrevistaDevolucao']
                    emprestimo.data_devolucao = row['DataDevolucao']
                    emprestimo.status = StatusEmprestimo.DEVOLVIDO if row[
                        'Status'] == 'Devolvido' else StatusEmprestimo.ATIVO
                    emprestimo.observacoes = row['Observacoes']

                    emprestimos.append(emprestimo)

            return emprestimos
        except Exception as e:
            print(f"Erro ao buscar empréstimos do usuário {usuario_id}: {e}")
            return []

    @staticmethod
    def buscar_por_livro(livro_id: int) -> List['Emprestimo']:

        return []

    @staticmethod
    def buscar_atrasados() -> List['Emprestimo']:

        return []

    @staticmethod
    def buscar_por_id(emprestimo_id: int) -> Optional['Emprestimo']:
        """Busca um empréstimo pelo ID no banco de dados"""
        try:
            from Banco_de_dados.connection import DatabaseConnection

            db = DatabaseConnection()
            query = """
            SELECT Id, UsuarioId, LivroId, DataEmprestimo, DataPrevistaDevolucao,
                   DataDevolucao, Status, Observacoes
            FROM Emprestimo
            WHERE Id = ?
            """
            result = db.execute_query(query, (emprestimo_id,))

            if result and len(result) > 0:
                row = result[0]

                emprestimo = Emprestimo(
                    usuario_id=row['UsuarioId'],
                    livro_id=row['LivroId'],
                    biblioteca_id=1
                )
                emprestimo.id = row['Id']
                emprestimo.data_emprestimo = row['DataEmprestimo']
                emprestimo.data_prevista_devolucao = row['DataPrevistaDevolucao']
                emprestimo.data_devolucao = row['DataDevolucao']
                emprestimo.status = StatusEmprestimo.DEVOLVIDO if row[
                    'Status'] == 'Devolvido' else StatusEmprestimo.ATIVO
                emprestimo.observacoes = row['Observacoes']

                return emprestimo
            return None
        except Exception as e:
            print(f"Erro ao buscar empréstimo: {e}")
            return None

    @staticmethod
    def obter_historico_usuario_completo(usuario_id: int) -> List[dict]:
        """Obtém histórico completo de empréstimos do usuário com status detalhado"""
        try:
            from Banco_de_dados.connection import DatabaseConnection

            db = DatabaseConnection()
            query = """
                SELECT
                    e.Id,
                    e.LivroId,
                    e.DataEmprestimo,
                    e.DataPrevistaDevolucao,
                    e.DataDevolucao,
                    e.Status,
                    l.Nome as LivroTitulo,
                    l.Autor as LivroAutor
                FROM Emprestimo e
                INNER JOIN Livro l ON e.LivroId = l.Id
                WHERE e.UsuarioId = ?
                ORDER BY e.DataEmprestimo DESC
            """

            result = db.execute_query(query, (usuario_id,))

            historico = []
            if result:
                hoje = datetime.now().date()

                for row in result:
                    try:

                        emprestimo_id = row.get('Id')
                        livro_id = row.get('LivroId')
                        data_emprestimo = row.get('DataEmprestimo')
                        data_devolucao_prevista = row.get(
                            'DataPrevistaDevolucao')
                        data_devolucao = row.get('DataDevolucao')
                        status = row.get('Status')
                        livro_titulo = row.get('LivroTitulo')
                        livro_autor = row.get('LivroAutor')

                        if data_devolucao_prevista and hasattr(
                                data_devolucao_prevista, 'date'):
                            data_devolucao_prevista_date = data_devolucao_prevista.date()
                        else:
                            data_devolucao_prevista_date = None

                        if data_devolucao and hasattr(data_devolucao, 'date'):
                            data_devolucao_date = data_devolucao.date()
                        else:
                            data_devolucao_date = None

                        if data_devolucao_date:
                            status_visual = "devolvido"
                            cor_status = "blue"
                            icone_status = "📘"
                        elif data_devolucao_prevista_date:
                            if hoje > data_devolucao_prevista_date:
                                status_visual = "atrasado"
                                cor_status = "red"
                                icone_status = "🔴"
                            elif hoje == data_devolucao_prevista_date:
                                status_visual = "vence_hoje"
                                cor_status = "yellow"
                                icone_status = "🟡"
                            else:
                                status_visual = "em_dia"
                                cor_status = "green"
                                icone_status = "🟢"
                        else:
                            status_visual = "sem_data"
                            cor_status = "gray"
                            icone_status = "⚪"

                        emprestimo = {
                            'id': emprestimo_id,
                            'livro_id': livro_id,
                            'livro_titulo': livro_titulo,
                            'livro_autor': livro_autor,
                            'data_emprestimo': data_emprestimo,
                            'data_devolucao_prevista': data_devolucao_prevista,
                            'data_devolucao': data_devolucao,
                            'status': status,
                            'status_visual': status_visual,
                            'cor_status': cor_status,
                            'icone_status': icone_status
                        }
                        historico.append(emprestimo)

                    except Exception as row_error:
                        print(
                            f"Erro ao processar linha do empréstimo: {row_error}")
                        continue

            return historico

        except Exception as e:
            print(f"Erro ao obter histórico do usuário {usuario_id}: {e}")
            return []

    @staticmethod
    def verificar_emprestimos_atrasados(usuario_id: int) -> List[dict]:
        """Verifica se o usuário tem empréstimos em atraso"""
        try:
            from Banco_de_dados.connection import DatabaseConnection

            db = DatabaseConnection()
            query = """
            SELECT
                e.Id,
                e.DataEmprestimo,
                e.DataPrevistaDevolucao,
                e.DataDevolucao,
                e.Status,
                l.Nome as livro_titulo,
                l.Autor as livro_autor
            FROM Emprestimo e
            INNER JOIN Livro l ON e.LivroId = l.Id
            WHERE e.UsuarioId = ?
                AND e.Status != 'Devolvido'
                AND e.DataPrevistaDevolucao < GETDATE()
            ORDER BY e.DataPrevistaDevolucao ASC
            """

            result = db.execute_query(query, (usuario_id,))

            emprestimos_atrasados = []
            if result:
                for row in result:
                    data_prevista = row.get('DataPrevistaDevolucao')
                    if data_prevista and hasattr(data_prevista, 'date'):
                        dias_atraso = (
                            datetime.now().date() -
                            data_prevista.date()).days
                    else:
                        dias_atraso = 0

                    emprestimo = {
                        'id': row.get('Id'),
                        'data_emprestimo': row.get('DataEmprestimo'),
                        'data_devolucao_prevista': row.get('DataPrevistaDevolucao'),
                        'livro_titulo': row.get('livro_titulo'),
                        'livro_autor': row.get('livro_autor'),
                        'dias_atraso': dias_atraso}
                    emprestimos_atrasados.append(emprestimo)

            return emprestimos_atrasados
        except Exception as e:
            print(f"Erro ao verificar empréstimos atrasados: {e}")
            return []

    @staticmethod
    def contar_emprestimos_ativos_por_livro(livro_id: int) -> int:
        """Conta quantos empréstimos ativos existem para um livro específico"""
        try:
            from Banco_de_dados.connection import DatabaseConnection
            
            db = DatabaseConnection()
            query = """
            SELECT COUNT(*) as total_ativos
            FROM Emprestimo 
            WHERE LivroId = ? AND Status IN ('Emprestado', 'Atrasado')
            """
            
            result = db.execute_query(query, (livro_id,))
            
            if result and len(result) > 0:
                return result[0].get('total_ativos', 0)
            
            return 0
            
        except Exception as e:
            print(f"Erro ao contar empréstimos ativos do livro {livro_id}: {e}")
            return 0

    @staticmethod
    def estatisticas_biblioteca(biblioteca_id: int) -> dict:

        return {
            'total_emprestimos': 0,
            'emprestimos_ativos': 0,
            'emprestimos_atrasados': 0,
            'total_multas': 0.0
        }
