# 🗃️ Backup e Instalação do Sistema de Biblioteca

## 📋 **Problema Identificado**
O sistema funciona neste computador porque tem:
- SQL Server instalado e configurado
- Banco de dados "SistemaBiblioteca" com dados
- Usuários de teste cadastrados

## 💾 **Arquivos de Backup Incluídos**
- `backup_sistema_completo.sql` - Script completo para recriar o banco
- `init-biblioteca.sql` - Script de inicialização original
- `docker-compose.yml` - Para usar com Docker

## 🚀 **Como usar em outro computador**

### **Como Fazer Backup do Banco via Docker**

Se você já está usando o Docker para rodar o SQL Server, pode gerar um backup atualizado do banco de dados facilmente. Siga os passos abaixo:

#### 1️⃣ Gere o backup do banco atual

No terminal, dentro da pasta `Banco_de_dados`, execute:

```bash
# Gere o backup do banco 'SistemaBiblioteca' para um arquivo dentro do container
docker exec -it sqlserver \
	/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "BibliotecaFort3!" \
	-Q "BACKUP DATABASE [SistemaBiblioteca] TO DISK = N'/var/opt/mssql/backup/sistema_biblioteca_backup.sql' WITH INIT"
```

#### 2️⃣ Copie o arquivo de backup do container para sua máquina

```bash
# Crie a pasta local se necessário
mkdir -p Banco_de_dados/backup

# Copie o arquivo do container para a pasta local
docker cp sqlserver:/var/opt/mssql/backup/sistema_biblioteca_backup.sql Banco_de_dados/backup/
```

O arquivo `sistema_biblioteca_backup.sql` estará disponível em `Banco_de_dados/backup/`.

#### 3️⃣ (Opcional) Restaure o backup em outro ambiente

Para restaurar o backup em outro container ou servidor SQL Server, use:

```bash
docker exec -it sqlserver \
	/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "BibliotecaFort3!" \
	-Q "RESTORE DATABASE [SistemaBiblioteca] FROM DISK = N'/var/opt/mssql/backup/sistema_biblioteca_backup.sql' WITH REPLACE"
```

---

### **Opção 1: SQL Server**

#### 2️⃣ **Executar o Backup**
1. Abrir SQL Server Management Studio (SSMS)
2. Conectar ao servidor local
3. Abrir o arquivo `backup_sistema_completo.sql`
4. Executar o script (F5)

#### 3️⃣ **Configurar arquivo .env**
```env
DB_SERVER=localhost,1433
DB_DATABASE=SistemaBiblioteca
DB_USERNAME=sa
DB_PASSWORD=SuaSenhaDoSQLServer
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### **Opção 2: Docker (Mais Fácil)**

#### 1️⃣ **Instalar Docker Desktop**
- Baixar em: https://www.docker.com/products/docker-desktop

#### 2️⃣ **Executar com Docker**
```bash
# Na pasta do projeto
cd Banco_de_dados

# Subir container SQL Server
docker-compose up -d

# Aguardar 30 segundos para inicializar

# Executar backup
docker exec -it sqlserver sqlcmd -S localhost -U sa -P "BibliotecaFort3!" -i /backup/backup_sistema_completo.sql
```

#### 3️⃣ **Arquivo .env já está configurado**
```env
DB_SERVER=localhost,1433
DB_DATABASE=SistemaBiblioteca
DB_USERNAME=sa
DB_PASSWORD=BibliotecaFort3!
DB_DRIVER=ODBC Driver 17 for SQL Server
```
## 🔧 **Dependências Python (Todos os casos)**

```bash
pip install customtkinter pillow pyodbc python-dotenv
```

## 🎯 **Executar o Sistema**

```bash
# Na pasta raiz do projeto
python Frontend/sistema_completo.py
```

## 🔐 **Credenciais de Teste**

| Tipo | Email | Senha |
|------|-------|-------|
| 📚 **Bibliotecário** | `bibliotecario@biblioteca.com` | `bibliotecario123` |
| 🎓 **Aluno** | `aluno@universidade.edu` | `aluno123` |
| 👨‍🏫 **Professor** | `professor@universidade.edu` | `professor123` |

## 📊 **Dados Incluídos no Backup**

### **Usuários:** 3
- 1 Bibliotecário (acesso completo)
- 1 Aluno (visualização)
- 1 Professor (visualização + privilégios)

### **Livros:** 10
- 8 livros ativos
- 2 livros inativos (para testar filtros)
- Dados completos: título, autor, ISBN, gênero

## ✅ **Verificar se funcionou**

Após executar o sistema, você deve ver:
- ✅ "Backend disponível - Modo integrado completo"
- Interface com 3 botões de usuário
- Login funcional com as credenciais acima
- CRUD de livros funcionando (como bibliotecário)

## 🆘 **Solução de Problemas**

### **Erro de conexão com banco:**
- Verificar se SQL Server está rodando
- Conferir credenciais no arquivo `.env`
- Testar conexão no SSMS primeiro

### **Erro "pyodbc not found":**
```bash
pip install pyodbc
```

### **Erro "customtkinter not found":**
```bash
pip install customtkinter pillow
```

### **Sistema abre mas não faz login:**
- Verificar se o script SQL foi executado completamente
- Conferir se a tabela Usuario tem dados:
```sql
SELECT * FROM Usuario;
```

## 📞 **Suporte**

Se ainda tiver problemas:
1. Verificar logs de erro no terminal
2. Testar modo simulação primeiro
3. Confirmar versão do Python (3.8+)
4. Verificar se todas as dependências estão instaladas