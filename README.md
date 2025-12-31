# API Controle Financeiro 💰

API REST desenvolvida com FastAPI para gerenciar transações financeiras através de uma planilha do Google Sheets.

Arquitetura baseada em **Clean Architecture** com separação clara de responsabilidades em camadas.

## 📋 Funcionalidades

- ✅ Listagem paginada de transações do extrato
- ✅ Integração com Google Sheets
- ✅ Documentação automática com Swagger UI
- ✅ Health check para monitoramento
- ✅ Arquitetura em camadas (Domain, Data, Use Cases, API)
- ✅ Injeção de dependências

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Python 3.8+** - Linguagem de programação
- **Google Sheets API** - Integração com planilhas
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture**, organizado em camadas:

```
controle-financeiro/
├── app/
│   ├── __init__.py
│   ├── domain/              # 🎯 Camada de Domínio
│   │   ├── entities.py      # Entidades de negócio
│   │   └── schemas.py       # DTOs (Data Transfer Objects)
│   │
│   ├── data/                # 💾 Camada de Dados
│   │   └── repositories/
│   │       ├── transacao_repository_interface.py  # Interface
│   │       └── google_sheets_repository.py        # Implementação
│   │
│   ├── use_cases/           # 📋 Casos de Uso (Lógica de Negócio)
│   │   ├── listar_transacoes_paginadas.py
│   │   └── verificar_saude.py
│   │
│   ├── api/                 # 🌐 Camada de API
│   │   ├── routes/          # Rotas/Controllers
│   │   │   ├── transacoes.py
│   │   │   └── health.py
│   │   └── dependencies.py  # Injeção de dependências
│   │
│   └── core/                # ⚙️ Configurações e Utilitários
│       └── config.py        # Configurações centralizadas
│
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt         # Dependências
├── .env                     # Variáveis de ambiente
├── .gitignore              # Arquivos ignorados
└── README.md               # Este arquivo
```

### 📐 Camadas da Arquitetura

#### 🎯 Domain (Domínio)
- **Entidades**: Objetos de negócio puros (ex: `Transacao`)
- **Schemas**: Modelos de entrada/saída da API (DTOs)
- Não depende de nenhuma outra camada

#### 💾 Data (Dados)
- **Repositories**: Interfaces e implementações para acesso a dados
- Implementação atual: `GoogleSheetsTransacaoRepository`
- Facilita troca de fonte de dados (ex: banco de dados)

#### 📋 Use Cases (Casos de Uso)
- Lógica de negócio da aplicação
- Orquestra chamadas aos repositórios
- Independente de framework ou biblioteca externa

#### 🌐 API
- **Routes**: Endpoints HTTP
- **Dependencies**: Injeção de dependências (factories)
- Camada de apresentação/interface com usuário

#### ⚙️ Core
- Configurações centralizadas
- Utilitários compartilhados
- Gerenciamento de variáveis de ambiente

## 📦 Instalação

### 1. Clone o repositório (ou navegue até a pasta do projeto)

```bash
cd /home/caiovidinha/projetos/controle-financeiro
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual

```bash
# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

O arquivo `.env` já está configurado com suas credenciais do Google Sheets:

- `GOOGLE_SHEETS_ID`: ID da planilha
- `GOOGLE_SERVICE_ACCOUNT_EMAIL`: Email da conta de serviço
- `GOOGLE_PRIVATE_KEY`: Chave privada da conta de serviço

⚠️ **Importante**: Certifique-se de que a conta de serviço tem permissão para acessar a planilha!

### 6. Execute a API

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 📚 Endpoints

### Listar Transações (Paginado)

```http
GET /api/transacoes?page=1&page_size=10
```

**Parâmetros de Query:**
- `page` (opcional): Número da página (padrão: 1)
- `page_size` (opcional): Itens por página (padrão: 10, máximo: 100)

**Resposta:**
```json
{
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "items": [
    {
      "tipo": "Despesa",
      "descritivo": "Supermercado",
      "valor": "R$ 150,00",
      "data": "15/12/2025",
      "mes": "Dezembro",
      "detalhes": "Compras mensais",
      "situacao": "Pago",
      "conta": "Conta Corrente"
    }
  ]
}
```

### Health Check

```http
GET /api/health
```

Verifica o status da API e a conexão com o Google Sheets.

### Documentação Interativa

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📊 Estrutura da Planilha

A API espera que a aba **"Extrato"** contenha as seguintes colunas:

| TIPO | DESCRITIVO | VALOR | DATA | MÊS | DETALHES | SITUAÇÃO | CONTA |
|------|------------|-------|------|-----|----------|----------|-------|

## 🗂️ Estrutura Detalhada do Projeto

```
controle-financeiro/
├── app/                     # Código principal da aplicação
│   ├── __init__.py
│   │
│   ├── domain/              # 🎯 Domínio - Regras de negócio
│   │   ├── __init__.py
│   │   ├── entities.py      # Entidades (ex: Transacao)
│   │   └── schemas.py       # Schemas Pydantic (DTOs)
│   │
│   ├── data/                # 💾 Dados - Acesso a fontes de dados
│   │   ├── __init__.py
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── transacao_repository_interface.py
│   │       └── google_sheets_repository.py
│   │
│   ├── use_cases/           # 📋 Casos de Uso - Lógica de negócio
│   │   ├── __init__.py
│   │   ├── listar_transacoes_paginadas.py
│   │   └── verificar_saude.py
│   │
│   ├── api/                 # 🌐 API - Camada de apresentação
│   │   ├── __init__.py
│   │   ├── dependencies.py  # Injeção de dependências
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── transacoes.py
│   │       └── health.py
│   │
│   └── core/                # ⚙️ Core - Configurações
│       ├── __init__.py
│       └── config.py
│
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente
├── .gitignore             # Arquivos a ignorar no Git
└── README.md              # Documentação
```

## 🎯 Fluxo de Requisição

```
Cliente HTTP
    ↓
[API Layer] routes/transacoes.py
    ↓
[Use Case] listar_transacoes_paginadas.py
    ↓
[Repository Interface] transacao_repository_interface.py
    ↓
[Repository Implementation] google_sheets_repository.py
    ↓
[Domain Entity] entities.py
    ↓
[API Layer] schemas.py (DTO) → Response
```

## 🔧 Comandos Úteis

### Executar em modo de desenvolvimento
```bash
uvicorn main:app --reload
```

### Executar em produção
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Atualizar dependências
```bash
pip install -r requirements.txt --upgrade
```

## 🧪 Testando a API

### Usando cURL
```bash
curl http://localhost:8000/api/transacoes?page=1&page_size=5
```

### Usando Python
```python
import requests

response = requests.get("http://localhost:8000/api/transacoes", params={"page": 1, "page_size": 10})
print(response.json())
```

## ⚠️ Notas Importantes

1. **Permissões no Google Sheets**: Compartilhe a planilha com o email da conta de serviço (`novo-controle-financeiro@controle-financeiro-450717.iam.gserviceaccount.com`)

2. **Segurança**: O arquivo `.env` contém informações sensíveis e está no `.gitignore`. Nunca commite credenciais!

3. **CORS**: A API está configurada para aceitar requisições de qualquer origem. Em produção, configure adequadamente os domínios permitidos.

## 🐛 Troubleshooting

### Erro de autenticação no Google Sheets
- Verifique se a conta de serviço tem acesso à planilha
- Confirme que as credenciais no `.env` estão corretas

### Erro ao importar módulos
- Certifique-se de que o ambiente virtual está ativado
- Execute: `pip install -r requirements.txt`

## 📝 Próximos Passos

- [ ] Adicionar endpoint POST para criar transações
- [ ] Adicionar endpoint PUT para atualizar transações
- [ ] Adicionar endpoint DELETE para remover transações
- [ ] Implementar filtros (por tipo, data, conta, etc.)
- [ ] Adicionar autenticação/autorização
- [ ] Criar testes automatizados
- [ ] Implementar cache para melhorar performance
- [ ] Adicionar logs estruturados

## 💡 Benefícios da Arquitetura

### ✨ Separação de Responsabilidades
Cada camada tem uma responsabilidade clara e bem definida

### 🔄 Testabilidade
Casos de uso e repositórios podem ser testados independentemente

### 🔌 Flexibilidade
Fácil trocar implementações (ex: Google Sheets → Banco de Dados)

### 📦 Manutenibilidade
Código organizado e fácil de entender e modificar

### 🎯 Independência de Framework
Lógica de negócio não depende de FastAPI ou bibliotecas externas

## 🤝 Contribuindo

Para adicionar novas funcionalidades, siga o padrão da arquitetura:

1. **Domain**: Crie/atualize entidades e schemas
2. **Repository**: Implemente métodos no repositório
3. **Use Case**: Crie o caso de uso com a lógica de negócio
4. **API**: Adicione a rota que usa o caso de uso

Exemplo para adicionar criação de transação:
```
1. app/domain/schemas.py → CreateTransacaoRequest
2. app/data/repositories/transacao_repository_interface.py → create()
3. app/use_cases/criar_transacao.py → CriarTransacao
4. app/api/routes/transacoes.py → POST endpoint
```

## 👨‍💻 Autor

Desenvolvido com ❤️ usando FastAPI e Python

---

**Dúvidas?** Consulte a documentação interativa em `http://localhost:8000/docs`
