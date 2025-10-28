-- Criar banco de dados SistemaBiblioteca
CREATE DATABASE SistemaBiblioteca;
GO

-- Usar o banco de dados criado
USE SistemaBiblioteca;
GO

-- Criar tabela Livro
CREATE TABLE Livro (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome NVARCHAR(255) NOT NULL,
    Autor NVARCHAR(255) NOT NULL,
    ISBN NVARCHAR(20) NOT NULL UNIQUE,
    Genero NVARCHAR(100) NOT NULL,
    DataCadastro DATETIME2 DEFAULT GETDATE(),
    DataAtualizacao DATETIME2 DEFAULT GETDATE(),
    Ativo BIT DEFAULT 1
);
GO

-- Criar tabela Usuario para autenticação
CREATE TABLE Usuario (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Nome NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    Senha NVARCHAR(255) NOT NULL, -- Senha criptografada
    TipoUsuario NVARCHAR(20) NOT NULL CHECK (TipoUsuario IN ('Bibliotecario', 'Aluno', 'Professor')),
    Matricula NVARCHAR(20) NULL, -- Para alunos e professores
    Curso NVARCHAR(100) NULL, -- Para alunos
    Departamento NVARCHAR(100) NULL, -- Para professores
    Ativo BIT DEFAULT 1,
    DataCadastro DATETIME2 DEFAULT GETDATE(),
    DataAtualizacao DATETIME2 DEFAULT GETDATE()
);
GO

-- Criar tabela Aluno (já existente, mantendo para compatibilidade)
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Aluno')
BEGIN
    CREATE TABLE Aluno (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Nome NVARCHAR(100) NOT NULL,
        Matricula NVARCHAR(20) NOT NULL UNIQUE,
        Curso NVARCHAR(100) NOT NULL,
        DataCadastro DATETIME2 DEFAULT GETDATE()
    );
END
GO

-- Inserir dados de exemplo para Livros
INSERT INTO Livro (Nome, Autor, ISBN, Genero) VALUES
('Dom Casmurro', 'Machado de Assis', '978-85-359-0277-5', 'Literatura Brasileira'),
('O Cortiço', 'Aluísio Azevedo', '978-85-359-0278-2', 'Literatura Brasileira'),
('Clean Code', 'Robert C. Martin', '978-0-13-235088-4', 'Tecnologia'),
('Design Patterns', 'Gang of Four', '978-0-20163-361-0', 'Tecnologia'),
('1984', 'George Orwell', '978-0-452-28423-4', 'Ficção Científica'),
('Algoritmos e Estruturas de Dados', 'Thomas H. Cormen', '978-85-352-3699-6', 'Computação');
GO

-- Inserir usuários de exemplo com senhas criptografadas (MD5 simples)
-- Senhas: bibliotecario123, aluno123, professor123
INSERT INTO Usuario (Nome, Email, Senha, TipoUsuario, Matricula, Curso, Departamento) VALUES
('Ana Costa', 'ana.costa@biblioteca.com', 'e3afed0047b08059d0fada10f400c1e5', 'Bibliotecario', 'BIB001', NULL, NULL),
('João Silva', 'joao.silva@estudante.com', 'c33367701511b4f6020ec61ded352059', 'Aluno', '2023001', 'Ciência da Computação', NULL),
('Maria Santos', 'maria.santos@estudante.com', 'c33367701511b4f6020ec61ded352059', 'Aluno', '2023002', 'Engenharia de Software', NULL),
('Dr. Pedro Oliveira', 'pedro.oliveira@professor.com', 'f25a2fc72690b780b2a14e140ef6a9e0', 'Professor', 'PROF001', NULL, 'Computação'),
('Dra. Carla Lima', 'carla.lima@professor.com', 'f25a2fc72690b780b2a14e140ef6a9e0', 'Professor', 'PROF002', NULL, 'Matemática');
GO

-- Inserir dados de exemplo para Alunos (se a tabela estiver vazia)
IF NOT EXISTS (SELECT 1 FROM Aluno)
BEGIN
    INSERT INTO Aluno (Nome, Matricula, Curso) VALUES
    ('João Silva', '2023001', 'Ciência da Computação'),
    ('Maria Santos', '2023002', 'Engenharia de Software'),
    ('Pedro Oliveira', '2023003', 'Sistemas de Informação'),
    ('Ana Costa', '2023004', 'Análise e Desenvolvimento de Sistemas');
END
GO

-- Criar índices para otimizar consultas
CREATE INDEX IX_Livro_ISBN ON Livro(ISBN);
CREATE INDEX IX_Livro_Autor ON Livro(Autor);
CREATE INDEX IX_Livro_Genero ON Livro(Genero);
CREATE INDEX IX_Aluno_Matricula ON Aluno(Matricula);
CREATE INDEX IX_Usuario_Email ON Usuario(Email);
CREATE INDEX IX_Usuario_TipoUsuario ON Usuario(TipoUsuario);
GO

-- Trigger para atualizar DataAtualizacao automaticamente
CREATE TRIGGER TR_Livro_UpdateTimestamp
ON Livro
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Livro 
    SET DataAtualizacao = GETDATE()
    FROM Livro l
    INNER JOIN inserted i ON l.Id = i.Id;
END
GO

PRINT 'Banco de dados SistemaBiblioteca criado com sucesso!';
PRINT 'Tabelas criadas: Livro, Aluno';
PRINT 'Dados de exemplo inseridos!';
GO