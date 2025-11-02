from datetime import datetime
from typing import Optional

class Avaliacao:
    
    def __init__(self, livro_id: int, usuario_id: int, nota: int,
                 comentario: Optional[str] = None, id: Optional[int] = None,
                 data_avaliacao: Optional[datetime] = None, ativa: bool = True):
        
        self._id = id
        self.livro_id = livro_id
        self.usuario_id = usuario_id
        self.nota = nota
        self.comentario = comentario
        self.data_avaliacao = data_avaliacao or datetime.now()
        self._ativa = ativa

    @property
    def id(self):
        return self._id

    @property
    def ativa(self):
        return self._ativa

    @ativa.setter
    def ativa(self, valor: bool):
        self._ativa = valor
    
    def validar(self) -> tuple[bool, str]:
        
        if not self.livro_id or self.livro_id <= 0:
            return False, "ID do livro é obrigatório"
        
        if not self.usuario_id or self.usuario_id <= 0:
            return False, "ID do usuário é obrigatório"
        
        if not self.nota or not (1 <= self.nota <= 5):
            return False, "Nota deve ser entre 1 e 5"
        
        if self.comentario and len(self.comentario) > 500:
            return False, "Comentário deve ter no máximo 500 caracteres"
        
        return True, "Avaliação válida"
    
    def salvar(self) -> tuple[bool, str]:
        
        from Banco_de_dados.connection import DatabaseConnection
        
        valido, mensagem = self.validar()
        if not valido:
            return False, f"Erro de validação: {mensagem}"
        
        db = DatabaseConnection()
        
        if self._usuario_ja_avaliou(db):
            return False, "Usuário já avaliou este livro"
        
        try:
            query = 
            params = (self.livro_id, self.usuario_id, self.nota, 
                     self.comentario, self.data_avaliacao)
            
            if db.execute_non_query(query, params):
                self.id = self._buscar_ultimo_id(db)
                return True, "Avaliação salva com sucesso!"
            else:
                return False, "Falha ao salvar avaliação"
                
        except Exception as e:
            return False, f"Erro ao salvar avaliação: {e}"
    
    def excluir(self) -> tuple[bool, str]:
        
        from Banco_de_dados.connection import DatabaseConnection
        
        if not self.id:
            return False, "ID da avaliação é obrigatório"
        
        db = DatabaseConnection()
        
        try:
            query = "UPDATE Avaliacao SET Ativa = 0 WHERE Id = ?"
            if db.execute_non_query(query, (self.id,)):
                self.ativa = False
                return True, "Avaliação removida com sucesso!"
            else:
                return False, "Falha ao remover avaliação"
                
        except Exception as e:
            return False, f"Erro ao remover avaliação: {e}"
    
    @staticmethod
    def listar_por_livro(livro_id: int) -> list['Avaliacao']:
        
        from Banco_de_dados.connection import DatabaseConnection
        
        db = DatabaseConnection()
        
        try:
            query = 
            resultados = db.execute_query(query, (livro_id,))
            
            if resultados:
                return [Avaliacao._from_db_row(row) for row in resultados]
            else:
                return []
                
        except Exception as e:
            print(f"✗ Erro ao listar avaliações: {e}")
            return []
    
    @staticmethod
    def calcular_media_livro(livro_id: int) -> float:
        
        from Banco_de_dados.connection import DatabaseConnection
        
        db = DatabaseConnection()
        
        try:
            query = 
            resultado = db.execute_query(query, (livro_id,))
            
            if resultado and resultado[0][0] is not None:
                return round(float(resultado[0][0]), 1)
            else:
                return 0.0
                
        except Exception as e:
            print(f"✗ Erro ao calcular média: {e}")
            return 0.0
    
    @staticmethod
    def _from_db_row(row) -> 'Avaliacao':
        
        return Avaliacao(
            id=row[0],
            livro_id=row[1],
            usuario_id=row[2],
            nota=row[3],
            comentario=row[4],
            data_avaliacao=row[5],
            ativa=bool(row[6])
        )
    
    def _usuario_ja_avaliou(self, db) -> bool:
        
        try:
            query = "SELECT COUNT(*) FROM Avaliacao WHERE LivroId = ? AND UsuarioId = ? AND Ativa = 1"
            resultado = db.execute_query(query, (self.livro_id, self.usuario_id))
            return resultado and resultado[0][0] > 0
        except:
            return False
    
    def _buscar_ultimo_id(self, db) -> Optional[int]:
        
        try:
            query = "SELECT SCOPE_IDENTITY()"
            resultado = db.execute_query(query)
            return int(resultado[0][0]) if resultado else None
        except:
            return None
    
    def __str__(self) -> str:
        return f"Avaliacao(id={self.id}, livro_id={self.livro_id}, nota={self.nota})"
    
    def __repr__(self) -> str:
        return f"Avaliacao(id={self.id}, livro_id={self.livro_id}, usuario_id={self.usuario_id}, nota={self.nota})"
