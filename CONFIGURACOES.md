# API de Configurações - Documentação

## 📋 Estrutura da Planilha "Configurações"

A aba **Configurações** deve ter 5 colunas:

| Coluna A | Coluna B | Coluna C | Coluna D | Coluna E |
|----------|----------|----------|----------|----------|
| CATEGORIAS | STATUS RECEITA | STATUS DESPESA | CONTAS | CARTÕES |

### Formato dos dados:

- **Categorias (A)**: Nome simples (ex: "Alimentação")
- **Status Receita (B)**: Nome simples (ex: "Recebido", "Pendente")
- **Status Despesa (C)**: Nome simples (ex: "Pago", "Vencido")
- **Contas (D)**: `Nome|Tipo|Saldo` (ex: "Nubank|Banco|R$ 1.000,00")
- **Cartões (E)**: `Nome|Limite|DiaFechamento|DiaVencimento` (ex: "Visa|R$ 5.000|15|25")

## 🌐 Endpoints Disponíveis

### 📂 Categorias

#### Listar todas as categorias
```http
GET /api/configuracoes/categorias
```

**Resposta:**
```json
[
  {"nome": "Alimentação"},
  {"nome": "Transporte"},
  {"nome": "Lazer"}
]
```

#### Criar categoria
```http
POST /api/configuracoes/categorias
Content-Type: application/json

{
  "nome": "Educação"
}
```

**Resposta:** `201 Created`
```json
{"nome": "Educação"}
```

#### Deletar categoria
```http
DELETE /api/configuracoes/categorias/{nome}
```

**Resposta:**
```json
{"message": "Categoria 'Educação' deletada com sucesso"}
```

---

### 📊 Status

#### Listar todos os status
```http
GET /api/configuracoes/status
```

**Resposta:**
```json
[
  {"nome": "Recebido", "tipo": "RECEITA"},
  {"nome": "Pendente", "tipo": "RECEITA"},
  {"nome": "Pago", "tipo": "DESPESA"},
  {"nome": "Vencido", "tipo": "DESPESA"}
]
```

#### Listar status filtrados por tipo
```http
GET /api/configuracoes/status?tipo=RECEITA
```

**Resposta:**
```json
[
  {"nome": "Recebido", "tipo": "RECEITA"},
  {"nome": "Pendente", "tipo": "RECEITA"}
]
```

```http
GET /api/configuracoes/status?tipo=DESPESA
```

**Resposta:**
```json
[
  {"nome": "Pago", "tipo": "DESPESA"},
  {"nome": "Vencido", "tipo": "DESPESA"}
]
```

> ⚠️ **Nota**: Status é apenas leitura (GET). Para adicionar novos status, edite diretamente a planilha nas colunas B (Receita) ou C (Despesa).

---

### 💳 Contas

#### Listar todas as contas
```http
GET /api/configuracoes/contas
```

**Resposta:**
```json
[
  {
    "nome": "Nubank",
    "tipo": "Banco",
    "saldo_inicial": "R$ 1.000,00"
  }
]
```

#### Criar conta
```http
POST /api/configuracoes/contas
Content-Type: application/json

{
  "nome": "Caixa Econômica",
  "tipo": "Banco",
  "saldo_inicial": "R$ 5.000,00"
}
```

**Resposta:** `201 Created`

#### Atualizar conta
```http
PUT /api/configuracoes/contas/{nome}
Content-Type: application/json

{
  "tipo": "Poupança",
  "saldo_inicial": "R$ 10.000,00"
}
```

#### Deletar conta
```http
DELETE /api/configuracoes/contas/{nome}
```

---

### 💳 Cartões

#### Listar todos os cartões
```http
GET /api/configuracoes/cartoes
```

**Resposta:**
```json
[
  {
    "nome": "Visa Platinum",
    "limite": "R$ 10.000,00",
    "dia_fechamento": "15",
    "dia_vencimento": "25"
  }
]
```

#### Criar cartão
```http
POST /api/configuracoes/cartoes
Content-Type: application/json

{
  "nome": "Mastercard Gold",
  "limite": "R$ 8.000,00",
  "dia_fechamento": "10",
  "dia_vencimento": "20"
}
```

**Resposta:** `201 Created`

#### Atualizar cartão
```http
PUT /api/configuracoes/cartoes/{nome}
Content-Type: application/json

{
  "limite": "R$ 15.000,00",
  "dia_fechamento": "12",
  "dia_vencimento": "22"
}
```

#### Deletar cartão
```http
DELETE /api/configuracoes/cartoes/{nome}
```

---

## 🧪 Exemplos de Uso

### cURL

```bash
# Listar categorias
curl http://localhost:8000/api/configuracoes/categorias

# Listar status de receita
curl http://localhost:8000/api/configuracoes/status?tipo=RECEITA

# Listar status de despesa
curl http://localhost:8000/api/configuracoes/status?tipo=DESPESA

# Listar todos os status
curl http://localhost:8000/api/configuracoes/status

# Criar categoria
curl -X POST http://localhost:8000/api/configuracoes/categorias \
  -H "Content-Type: application/json" \
  -d '{"nome": "Saúde"}'

# Deletar categoria
curl -X DELETE http://localhost:8000/api/configuracoes/categorias/Saúde
```

### Python

```python
import requests

base_url = "http://localhost:8000/api/configuracoes"

# Listar categorias
response = requests.get(f"{base_url}/categorias")
print(response.json())

# Listar status de receita
response = requests.get(f"{base_url}/status", params={"tipo": "RECEITA"})
print(response.json())

# Listar status de despesa
response = requests.get(f"{base_url}/status", params={"tipo": "DESPESA"})
print(response.json())

# Criar conta
nova_conta = {
    "nome": "Inter",
    "tipo": "Banco Digital",
    "saldo_inicial": "R$ 2.500,00"
}
response = requests.post(f"{base_url}/contas", json=nova_conta)
print(response.json())

# Atualizar cartão
update = {"limite": "R$ 20.000,00"}
response = requests.put(f"{base_url}/cartoes/Visa", json=update)
print(response.json())
```

---

## 📝 Validações

### Categorias
- ✅ Nome obrigatório
- ✅ Não permite duplicados

### Contas
- ✅ Nome obrigatório
- ✅ Não permite duplicados
- ℹ️ Tipo e saldo são opcionais

### Cartões
- ✅ Nome obrigatório
- ✅ Não permite duplicados
- ℹ️ Limite, dia de fechamento e vencimento são opcionais

---

## 🎯 Códigos de Status HTTP

| Código | Significado |
|--------|-------------|
| 200 | ✅ Sucesso (GET, PUT) |
| 201 | ✅ Criado com sucesso (POST) |
| 400 | ❌ Dados inválidos ou duplicados |
| 404 | ❌ Recurso não encontrado |
| 500 | ❌ Erro interno do servidor |
