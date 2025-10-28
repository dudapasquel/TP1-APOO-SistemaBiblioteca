# TP1-APOO-SistemaBiblioteca
Primeiro trabalho da disciplina ANÁLISE, PROJETO E PROGRAMAÇÃO ORIENTADOS A OBJETOS

## Sistema de Biblioteca

Sistema completo de gerenciamento de biblioteca com interfaces diferenciadas para bibliotecário e usuários (alunos/professores).

### 📁 Estrutura do Projeto

```
TP1-APOO-SistemaBiblioteca/
├── Backend/                     # Modelos de dados e lógica de negócio
│   ├── usuario.py              # Classe Usuario e subclasses
│   ├── livro.py                # Classe Livro
│   ├── biblioteca.py           # Classe Biblioteca
│   ├── emprestimo.py           # Classe Emprestimo
│   ├── avaliacao.py            # Classe Avaliacao
│   └── notificacao.py          # Classes de Notificacao
├── Banco_de_dados/             # Conexão e configurações do banco
│   ├── connection.py           # Gerenciamento de conexão
│   ├── docker-compose.yml      # Container SQL Server
│   └── init-biblioteca.sql     # Script de inicialização
├── Frontend/                   # Interface do usuário
│   └── sistema_completo.py     # Sistema integrado com autenticação
└── README.md                   # Documentação do projeto

```

### 🎯 Funcionalidades Principais

#### Interface do Bibliotecário
- Controle de estoque de livros
- Gerenciamento de empréstimos
- Histórico de usuários
- Acompanhamento de atrasos e multas

#### Interface dos Usuários
- Empréstimos de livros
- Verificação de atrasos
- Consulta de pendências
- Lista de espera
- Sistema de avaliação

#### Funcionalidades Implementadas (Fase 1)
- ✅ **Banco de dados SQL Server com Docker**
- ✅ **Tabela Livro** (nome, autor, ISBN, gênero)
- ✅ **Operações INSERT e UPDATE** via backend
- ✅ **Validação de dados**
- ✅ **Conexão com banco de dados**
- ✅ **Sistema de logs e controle**
- ✅ **Interface gráfica com CustomTkinter**
- ✅ **Demonstração de conceitos POO**

### 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11+
- **Frontend**: CustomTkinter (interface moderna)
- **Banco de dados**: SQL Server 2022 (Docker)
- **ORM**: pyodbc
- **Configuração**: python-dotenv

### 🚀 Como Executar

#### **🏛️ Sistema Completo e Integrado (RECOMENDADO)**
```bash
# 1. Clonar repositório
git clone https://github.com/dudapasquel/TP1-APOO-SistemaBiblioteca
cd TP1-APOO-SistemaBiblioteca

# 2. Instalar dependências
pip install customtkinter pillow pyodbc python-dotenv

# 3. Inicializar banco de dados
cd banco_de_dados
docker-compose up -d

# 4. Iniciar sistema integrado
python Frontend/sistema_completo.py
```

#### **🎯 Funcionalidades do Sistema Integrado:**
- ✅ **Seleção de Tipo de Usuário**: Bibliotecário/Aluno/Professor
- ✅ **Autenticação Real**: Login com banco SQL Server
- ✅ **CRUD Completo**: Adicionar, editar, inativar, reativar livros
- ✅ **Visualização Avançada**: Livros ativos e inativos
- ✅ **Interfaces Específicas**: Diferentes funcionalidades por role
- ✅ **Gerenciamento Completo**: Usuários e livros integrados

#### **📋 Credenciais de Teste:**
| Tipo | Email | Senha |
|------|-------|-------|
| 📚 **Bibliotecário** | `bibliotecario@biblioteca.com` | `bibliotecario123` |
| 🎓 **Aluno** | `aluno@universidade.edu` | `aluno123` |
| 👨‍🏫 **Professor** | `professor@universidade.edu` | `professor123` |

#### **Sistema Simplificado:**
```bash
# Executar o sistema diretamente
python Frontend/sistema_completo.py
```

### 📊 Funcionalidades Implementadas

- **Sistema de Autenticação**: Login com validação de credenciais
- **Gestão de Usuários**: Bibliotecários, alunos e professores
- **CRUD de Livros**: Criação, leitura, atualização e desativação
- **Interface Gráfica**: Interface moderna com CustomTkinter
- **Banco de Dados**: Integração com SQL Server

### 🔧 Configuração

Configurações no arquivo `.env`:
```
DB_SERVER=localhost,1433
DB_DATABASE=SistemaBiblioteca
DB_USERNAME=sa
DB_PASSWORD=BibliotecaFort3!
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### 🎓 Conceitos de POO Implementados

#### 1. **Classes**
- `Livro`: Representa livros com atributos e métodos específicos
- `Usuario`: Classe base para diferentes tipos de usuários
- `Biblioteca`: Gerencia o sistema como um todo
- `DatabaseConnection`: Encapsula conexão com banco

#### 2. **Herança**
- `Usuario` → `Aluno`, `Professor`, `Bibliotecario`
- Cada subclasse herda atributos comuns mas tem comportamentos específicos
- Diferentes prazos de empréstimo e limites por tipo de usuário

#### 3. **Polimorfismo**
- Método `emprestar()` se comporta diferente para Aluno vs Professor
- `Notificacao.enviar()` implementado diferente para cada tipo
- Interface única, comportamentos variados

#### 4. **Classes Abstratas**
- `Notificacao`: Define estrutura mas não é instanciada diretamente
- `NotificacaoAluno`, `NotificacaoProfessor` implementam métodos abstratos
- Garante padrão mas permite customização

### 📋 Próximas Etapas

- [x] ~~Interface de usuário (Frontend)~~ ✅ **Concluído**
- [ ] Tabelas de usuários e empréstimos
- [ ] Sistema de autenticação real
- [ ] APIs RESTful
- [ ] Sistema de notificações
- [ ] Relatórios e dashboards

### 👥 Equipe

Projeto desenvolvido para a disciplina Análise, Projeto e Programação Orientados a Objetos.
