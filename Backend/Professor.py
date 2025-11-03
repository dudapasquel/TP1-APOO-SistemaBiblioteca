from Backend.Usuario import Usuario


class Professor(Usuario):

    def __init__(
            self,
            nome: str,
            email: str,
            senha: str,
            matricula: str,
            departamento: str,
            id=None,
            ativo=True,
            data_cadastro=None,
            data_atualizacao=None):
        super().__init__(nome, email, senha, id, ativo, data_cadastro, data_atualizacao)
        self._matricula = matricula
        self._departamento = departamento

    @property
    def tipo_usuario(self):
        return "Professor"

    @property
    def matricula(self):
        return self._matricula

    @property
    def departamento(self):
        return self._departamento

    def validar_dados_especificos(self) -> tuple[bool, str]:
        if not self._matricula:
            return False, "Professor deve ter matrícula"

        if not self._departamento:
            return False, "Professor deve ter departamento"

        return True, "Dados válidos"

    def obter_dados_para_banco(self) -> dict:
        return {
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'tipo_usuario': self.tipo_usuario,
            'matricula': self._matricula,
            'curso': None,
            'departamento': self._departamento
        }
