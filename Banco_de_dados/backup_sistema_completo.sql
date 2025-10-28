-- ================================================
-- BACKUP SISTEMA DE BIBLIOTECA - VERSÃO PORTÁVEL
-- ================================================

-- Criar banco se não existir
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SistemaBiblioteca')
CREATE DATABASE SistemaBiblioteca;
GO

USE SistemaBiblioteca;
GO

-- ================================================
-- ESTRUTURA DAS TABELAS
-- ================================================

-- Tabela Usuario
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

-- Tabela Livro
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

-- ================================================
-- DADOS ESSENCIAIS PARA FUNCIONAMENTO
-- ================================================

-- Limpar dados existentes
DELETE FROM Usuario;
DELETE FROM Livro;

-- Usuários de teste (senhas são hash MD5)
INSERT INTO Usuario (Nome, Email, Senha, Tipo, Matricula, Curso, Departamento, Ativo) VALUES 
('João Bibliotecário', 'bibliotecario@biblioteca.com', '25d55ad283aa400af464c76d713c07ad', 'Bibliotecario', 'BIB001', 'Biblioteconomia', 'Biblioteca Central', 1),
('Maria Aluna', 'aluno@universidade.edu', '25d55ad283aa400af464c76d713c07ad', 'Aluno', 'ALU001', 'Ciência da Computação', 'Tecnologia', 1),
('Dr. Carlos Professor', 'professor@universidade.edu', '25d55ad283aa400af464c76d713c07ad', 'Professor', 'PROF001', 'Engenharia', 'Exatas', 1);

-- Livros de exemplo
INSERT INTO Livro (Nome, Autor, ISBN, Genero, Ativo) VALUES 
('Dom Casmurro', 'Machado de Assis', '978-85-359-0277-5', 'Romance', 1),
('O Cortiço', 'Aluísio Azevedo', '978-85-359-0276-8', 'Romance', 1),
('Iracema', 'José de Alencar', '978-85-359-0278-2', 'Romance', 1),
('O Guarani', 'José de Alencar', '978-85-359-0279-9', 'Romance', 1),
('Senhora', 'José de Alencar', '978-85-359-0280-5', 'Romance', 1),
('A Moreninha', 'Joaquim Manuel de Macedo', '978-85-359-0281-2', 'Romance', 1),
('O Ateneu', 'Raul Pompéia', '978-85-359-0282-9', 'Romance', 1),
('Casa Velha', 'Machado de Assis', '978-85-359-0283-6', 'Romance', 0),
('Lucíola', 'José de Alencar', '978-85-359-0284-3', 'Romance', 1),
('Diva', 'José de Alencar', '978-85-359-0285-0', 'Romance', 0);

GO

-- ================================================
-- VERIFICAÇÃO DOS DADOS
-- ================================================

-- Verificar usuários inseridos
SELECT 'Usuários cadastrados:' AS Info;
SELECT Id, Nome, Email, Tipo, Ativo FROM Usuario;

-- Verificar livros inseridos  
SELECT 'Livros cadastrados:' AS Info;
SELECT Id, Nome, Autor, ISBN, Genero, Ativo FROM Livro;

PRINT '✅ Backup executado com sucesso!';
PRINT '📊 3 usuários e 10 livros inseridos';
PRINT '🔐 Credenciais de teste:';
PRINT '   - bibliotecario@biblioteca.com / bibliotecario123';
PRINT '   - aluno@universidade.edu / aluno123';
PRINT '   - professor@universidade.edu / professor123';

GO