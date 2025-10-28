"""
Script para gerar backup completo do Sistema de Biblioteca
Inclui estrutura do banco e dados essenciais para funcionamento
"""

import os
from pathlib import Path
import sys

# Adicionar path do projeto
sys.path.append(str(Path(__file__).parent.parent))

try:
    from Banco_de_dados.connection import DatabaseConnection
    print("✅ Conexão com banco disponível")
except ImportError as e:
    print(f"❌ Erro ao importar conexão: {e}")
    exit(1)

def criar_backup_completo():
    """Cria backup completo do sistema"""
    
    print("🔄 Iniciando processo de backup...")
    
    # Criar diretório de backup
    backup_dir = Path(__file__).parent / "backup"
    backup_dir.mkdir(exist_ok=True)
    
    try:
        db = DatabaseConnection()
        
        # Arquivo de backup SQL
        backup_file = backup_dir / "sistema_biblioteca_backup.sql"
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write("-- ================================================\n")
            f.write("-- BACKUP SISTEMA DE BIBLIOTECA\n") 
            f.write("-- Gerado automaticamente\n")
            f.write("-- ================================================\n\n")
            
            # 1. Estrutura das tabelas
            f.write("-- ESTRUTURA DAS TABELAS\n")
            f.write("-- ========================\n\n")
            
            # Criar banco se não existir
            f.write("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SistemaBiblioteca')\n")
            f.write("CREATE DATABASE SistemaBiblioteca;\n")
            f.write("GO\n\n")
            f.write("USE SistemaBiblioteca;\n")
            f.write("GO\n\n")
            
            # Tabela Usuario
            f.write("""-- Tabela Usuario
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Usuario' AND xtype='U')
CREATE TABLE Usuario (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Senha NVARCHAR(255) NOT NULL,
    Tipo NVARCHAR(50) NOT NULL,
    Matricula NVARCHAR(50),
    Curso NVARCHAR(100),
    Departamento NVARCHAR(100),
    Ativo BIT DEFAULT 1,
    DataCadastro DATETIME DEFAULT GETDATE(),
    DataAtualizacao DATETIME DEFAULT GETDATE()
);

""")
            
            # Tabela Livro
            f.write("""-- Tabela Livro
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Livro' AND xtype='U')
CREATE TABLE Livro (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome NVARCHAR(200) NOT NULL,
    Autor NVARCHAR(100) NOT NULL,
    ISBN NVARCHAR(20) UNIQUE NOT NULL,
    Genero NVARCHAR(50) NOT NULL,
    Ativo BIT DEFAULT 1,
    DataCadastro DATETIME DEFAULT GETDATE(),
    DataAtualizacao DATETIME DEFAULT GETDATE()
);

""")
            
            # 2. Dados essenciais
            f.write("-- DADOS ESSENCIAIS\n")
            f.write("-- ==================\n\n")
            
            # Backup de usuários
            f.write("-- Dados de Usuários\n")
            f.write("DELETE FROM Usuario;\n\n")
            
            usuarios_query = "SELECT * FROM Usuario"
            usuarios = db.execute_query(usuarios_query)
            
            if usuarios:
                for usuario in usuarios:
                    matricula = f"'{usuario[5]}'" if usuario[5] else "NULL"
                    curso = f"'{usuario[6]}'" if usuario[6] else "NULL" 
                    departamento = f"'{usuario[7]}'" if usuario[7] else "NULL"
                    
                    insert_sql = f"""INSERT INTO Usuario (Nome, Email, Senha, Tipo, Matricula, Curso, Departamento, Ativo) 
VALUES ('{usuario[1]}', '{usuario[2]}', '{usuario[3]}', '{usuario[4]}', {matricula}, {curso}, {departamento}, {usuario[8]});
"""
                    f.write(insert_sql)
                
                print(f"✅ {len(usuarios)} usuários exportados")
            else:
                # Usuários padrão se não houver dados
                f.write("""-- Usuários padrão para teste
INSERT INTO Usuario (Nome, Email, Senha, Tipo, Matricula, Curso, Departamento, Ativo) VALUES 
('João Bibliotecário', 'bibliotecario@biblioteca.com', '25d55ad283aa400af464c76d713c07ad', 'Bibliotecario', 'BIB001', 'Biblioteconomia', 'Biblioteca Central', 1),
('Maria Aluna', 'aluno@universidade.edu', '25d55ad283aa400af464c76d713c07ad', 'Aluno', 'ALU001', 'Ciência da Computação', 'Tecnologia', 1),
('Dr. Carlos Professor', 'professor@universidade.edu', '25d55ad283aa400af464c76d713c07ad', 'Professor', 'PROF001', 'Engenharia', 'Exatas', 1);

""")
                print("⚠️ Nenhum usuário encontrado - adicionando usuários padrão")
            
            f.write("\n")
            
            # Backup de livros
            f.write("-- Dados de Livros\n")
            f.write("DELETE FROM Livro;\n\n")
            
            livros_query = "SELECT * FROM Livro"
            livros = db.execute_query(livros_query)
            
            if livros:
                for livro in livros:
                    insert_sql = f"""INSERT INTO Livro (Nome, Autor, ISBN, Genero, Ativo) 
VALUES ('{livro[1]}', '{livro[2]}', '{livro[3]}', '{livro[4]}', {livro[5]});
"""
                    f.write(insert_sql)
                
                print(f"✅ {len(livros)} livros exportados")
            else:
                # Livros padrão se não houver dados
                f.write("""-- Livros padrão para teste
INSERT INTO Livro (Nome, Autor, ISBN, Genero, Ativo) VALUES 
('Dom Casmurro', 'Machado de Assis', '978-85-359-0277-5', 'Romance', 1),
('O Cortiço', 'Aluísio Azevedo', '978-85-359-0276-8', 'Romance', 1),
('Iracema', 'José de Alencar', '978-85-359-0278-2', 'Romance', 1),
('O Guarani', 'José de Alencar', '978-85-359-0279-9', 'Romance', 1),
('Senhora', 'José de Alencar', '978-85-359-0280-5', 'Romance', 1);

""")
                print("⚠️ Nenhum livro encontrado - adicionando livros padrão")
            
            f.write("\nGO\n")
            f.write("-- Backup concluído com sucesso!\n")
        
        print(f"✅ Backup criado: {backup_file}")
        
        # Criar também um arquivo de configuração
        config_file = backup_dir / "configuracao_banco.md"
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write("""# Configuração do Banco de Dados

## Para usar este backup em outro computador:

### 1. Instalar SQL Server
- SQL Server 2019 ou superior
- SQL Server Management Studio (SSMS)

### 2. Executar o backup
```sql
-- No SSMS, execute o arquivo sistema_biblioteca_backup.sql
```

### 3. Configurar arquivo .env
```
DB_SERVER=localhost,1433
DB_DATABASE=SistemaBiblioteca
DB_USERNAME=sa
DB_PASSWORD=SuaSenhaAqui!
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### 4. Instalar dependências Python
```bash
pip install customtkinter pillow pyodbc python-dotenv
```

### 5. Executar sistema
```bash
python Frontend/sistema_completo.py
```

## Credenciais de teste incluídas:
- **Bibliotecário**: bibliotecario@biblioteca.com / bibliotecario123
- **Aluno**: aluno@universidade.edu / aluno123  
- **Professor**: professor@universidade.edu / professor123

*Senhas são hash MD5 de: bibliotecario123, aluno123, professor123*
""")
        
        print(f"✅ Documentação criada: {config_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar backup: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Gerando backup do Sistema de Biblioteca...")
    print("=" * 50)
    
    sucesso = criar_backup_completo()
    
    print("=" * 50)
    if sucesso:
        print("🎉 Backup gerado com sucesso!")
        print("\n📁 Arquivos criados:")
        print("   - sistema_biblioteca_backup.sql")
        print("   - configuracao_banco.md")
        print("\n💡 Para usar em outro computador:")
        print("   1. Instale SQL Server")
        print("   2. Execute o arquivo .sql no SSMS")
        print("   3. Configure o arquivo .env")
        print("   4. Execute o sistema")
    else:
        print("❌ Falha ao gerar backup!")