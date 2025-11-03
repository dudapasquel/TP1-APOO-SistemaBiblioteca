from Backend.Usuario import Usuario


class Bibliotecario(Usuario):

    def __init__(
            self,
            nome: str,
            email: str,
            senha: str,
            id=None,
            ativo=True,
            data_cadastro=None,
            data_atualizacao=None):
        super().__init__(nome, email, senha, id, ativo, data_cadastro, data_atualizacao)

    @property
    def tipo_usuario(self):
        return "Bibliotecario"

    def validar_dados_especificos(self) -> tuple[bool, str]:
        return True, "Dados válidos"

    def obter_dados_para_banco(self) -> dict:
        return {
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'tipo_usuario': self.tipo_usuario,
            'matricula': None,
            'curso': None,
            'departamento': None
        }
