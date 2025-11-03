from Backend.Usuario import Usuario


class Aluno(Usuario):

    def __init__(
            self,
            nome: str,
            email: str,
            senha: str,
            matricula: str,
            curso: str,
            id=None,
            ativo=True,
            data_cadastro=None,
            data_atualizacao=None):
        super().__init__(nome, email, senha, id, ativo, data_cadastro, data_atualizacao)
        self._matricula = matricula
        self._curso = curso

    @property
    def tipo_usuario(self):
        return "Aluno"

    @property
    def matricula(self):
        return self._matricula

    @property
    def curso(self):
        return self._curso

    def validar_dados_especificos(self) -> tuple[bool, str]:
        if not self._matricula:
            return False, "Aluno deve ter matrícula"

        if not self._curso:
            return False, "Aluno deve ter curso"

        return True, "Dados válidos"

    def obter_dados_para_banco(self) -> dict:
        return {
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'tipo_usuario': self.tipo_usuario,
            'matricula': self._matricula,
            'curso': self._curso,
            'departamento': None
        }
