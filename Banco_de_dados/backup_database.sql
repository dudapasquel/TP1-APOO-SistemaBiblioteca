-- Script para gerar backup do banco SistemaBiblioteca
-- Execute este script no SQL Server Management Studio ou similar

-- 1. Backup completo do banco
BACKUP DATABASE SistemaBiblioteca 
TO DISK = 'C:\backup\SistemaBiblioteca_backup.bak'
WITH FORMAT, 
     INIT,  
     NAME = 'Sistema Biblioteca - Backup Completo',
     SKIP, 
     NOREWIND, 
     NOUNLOAD,
     STATS = 25;

-- 2. Script para exportar dados essenciais
USE SistemaBiblioteca;

-- Exportar estrutura e dados de usuários
SELECT 'INSERT INTO Usuario (Nome, Email, Senha, Tipo, Matricula, Curso, Departamento, Ativo) VALUES ' +
       '(''' + Nome + ''', ''' + Email + ''', ''' + Senha + ''', ''' + Tipo + ''', ''' + 
       ISNULL(Matricula, '') + ''', ''' + ISNULL(Curso, '') + ''', ''' + ISNULL(Departamento, '') + ''', ' + 
       CAST(Ativo AS VARCHAR) + ');'
FROM Usuario;

-- Exportar estrutura e dados de livros
SELECT 'INSERT INTO Livro (Nome, Autor, ISBN, Genero, Ativo) VALUES ' +
       '(''' + Nome + ''', ''' + Autor + ''', ''' + ISBN + ''', ''' + Genero + ''', ' + 
       CAST(Ativo AS VARCHAR) + ');'
FROM Livro;