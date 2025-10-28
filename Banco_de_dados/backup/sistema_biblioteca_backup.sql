-- ================================================
-- BACKUP SISTEMA DE BIBLIOTECA
-- Gerado automaticamente
-- ================================================

-- ESTRUTURA DAS TABELAS
-- ========================

IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SistemaBiblioteca')
CREATE DATABASE SistemaBiblioteca;
GO

USE SistemaBiblioteca;
GO

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

-- DADOS ESSENCIAIS
-- ==================

-- Dados de Usuários
DELETE FROM Usuario;

