
from datetime import datetime, time
from typing import Optional, List
from enum import Enum

class StatusBiblioteca(Enum):

    ABERTA = "Aberta"
    FECHADA = "Fechada"
    MANUTENCAO = "Manutenção"

class Biblioteca:

    def __init__(self, nome: str, endereco: str, telefone: str, email: str,
                 id: Optional[int] = None):

        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.email = email

    def validar_dados(self) -> tuple[bool, str]:

        if not self.nome or len(self.nome.strip()) < 3:
            return False, "Nome deve ter pelo menos 3 caracteres"

        if not self.endereco or len(self.endereco.strip()) < 10:
            return False, "Endereço deve ter pelo menos 10 caracteres"

        if not self.telefone or len(self.telefone.strip()) < 10:
            return False, "Telefone deve ter pelo menos 10 dígitos"

        if not self.email or '@' not in self.email:
            return False, "Email deve ter formato válido"

        return True, "Dados válidos"

    def salvar(self) -> tuple[bool, str]:

        valido, mensagem = self.validar_dados()
        if not valido:
            return False, f"Erro de validação: {mensagem}"

        try:
            if self.id:
                return True, "Biblioteca atualizada com sucesso"
            else:
                self.id = 1
                return True, "Biblioteca cadastrada com sucesso"
        except Exception as e:
            return False, f"Erro ao salvar biblioteca: {e}"

    def __str__(self) -> str:

        return f"Biblioteca {self.nome}"

    def __repr__(self) -> str:

        return f"Biblioteca(id={self.id}, nome='{self.nome}')"

    @staticmethod
    def listar_todas(incluir_inativas: bool = False) -> List['Biblioteca']:

        return []

    @staticmethod
    def buscar_por_id(biblioteca_id: int) -> Optional['Biblioteca']:

        return None

    @staticmethod
    def buscar_por_nome(nome: str) -> Optional['Biblioteca']:

        return None
