# 📖 Guia de Uso da API - Controle Financeiro

## 🔗 Base URL
```
https://{api_url}
```
ou localmente:
```
http://localhost:8000
```

## 📚 Documentação Interativa
- **Swagger UI**: `https://{api_url}/docs`
- **ReDoc**: `https://{api_url}/redoc`

---

## 🏦 Endpoints Principais

### 1️⃣ **Transações (Extrato)**

#### 📋 Listar Transações
```http
GET /api/transacoes?page=1&page_size=10
```

**Filtros disponíveis:**
- `tipo` - RECEITA ou DESPESA
- `categoria` - Nome da categoria/descritivo
- `data_inicio` - Data inicial (DD/MM/YYYY)
- `data_fim` - Data final (DD/MM/YYYY)
- `mes` - Mês por extenso (01 - JANEIRO, 02 - FEVEREIRO, etc.)
- `situacao` - A pagar, Pago, A receber, Recebido
- `conta` - Nome da conta
- `order_by` - Campo para ordenar (data, tipo, categoria, valor, situacao, conta)

**Exemplo:**
```bash
curl "https://{api_url}/api/transacoes?tipo=DESPESA&mes=Janeiro&situacao=Pago&order_by=data"
```

**Resposta:**
```json
{
  "total": 100,
  "page": 1,
  "page_size": 10,
  "total_pages": 10,
  "items": [
    {
      "tipo": "DESPESA",
      "descritivo": "Supermercado",
      "valor": "R$ 150,00",
      "data": "15/01/2026",
      "mes": "Janeiro",
      "detalhes": "Compras mensais",
      "situacao": "Pago",
      "conta": "Conta Nubank",
      "row_index": 2
    }
  ]
}
```

#### ➕ Criar Transação
```http
POST /api/transacoes
Content-Type: application/json
```

**Body:**
```json
{
  "tipo": "Despesa",
  "descritivo": "Supermercado",
  "valor": "R$ 150,00",
  "data": "02/01/2026",
  "mes": "Janeiro",
  "detalhes": "Compras mensais",
  "situacao": "Pago",
  "conta": "Conta Corrente"
}
```

**Exemplo:**
```bash
curl -X POST "https://{api_url}/api/transacoes" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Despesa",
    "descritivo": "Supermercado",
    "valor": "R$ 150,00",
    "data": "02/01/2026",
    "mes": "Janeiro",
    "detalhes": "Compras mensais",
    "situacao": "Pago",
    "conta": "Conta Corrente"
  }'
```

#### ✏️ Atualizar Transação
```http
PUT /api/transacoes/{row_index}
Content-Type: application/json
```

**Parâmetros:**
- `row_index` - Índice da linha na planilha (vem do GET, ex: 2, 3, 4...)

**Body:**
```json
{
  "tipo": "Despesa",
  "descritivo": "Supermercado Extra",
  "valor": "R$ 200,00",
  "data": "02/01/2026",
  "mes": "Janeiro",
  "detalhes": "Compras mensais - atualizado",
  "situacao": "Pago",
  "conta": "Conta Corrente"
}
```

**Exemplo:**
```bash
curl -X PUT "https://{api_url}/api/transacoes/2" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Despesa",
    "descritivo": "Supermercado Extra",
    "valor": "R$ 200,00",
    "data": "02/01/2026",
    "mes": "Janeiro",
    "detalhes": "Compras mensais - atualizado",
    "situacao": "Pago",
    "conta": "Conta Corrente"
  }'
```

#### 🗑️ Deletar Transação
```http
DELETE /api/transacoes/{row_index}
```

**Exemplo:**
```bash
curl -X DELETE "https://{api_url}/api/transacoes/2"
```

---

### 2️⃣ **Transações de Crédito (Extrato Crédito)**

#### 📋 Listar Transações de Crédito
```http
GET /api/transacoes-credito?page=1&page_size=10
```

**Filtros disponíveis:**
- `tipo` - RECEITA ou DESPESA
- `categoria` - Nome da categoria/descritivo
- `data_inicio` - Data inicial (DD/MM/YYYY)
- `data_fim` - Data final (DD/MM/YYYY)
- `mes` - Mês por extenso
- `situacao` - A pagar, Pago, A receber, Recebido
- `cartao` - Nome do cartão de crédito
- `order_by` - Campo para ordenar (data, tipo, categoria, valor, situacao, cartao)

**Exemplo:**
```bash
curl "https://{api_url}/api/transacoes-credito?cartao=Nubank&mes=Janeiro"
```

#### ➕ Criar Transação de Crédito
```http
POST /api/transacoes-credito
Content-Type: application/json
```

**Body:**
```json
{
  "tipo": "Despesa",
  "descritivo": "Restaurante",
  "valor": "R$ 85,00",
  "data": "02/01/2026",
  "mes": "Janeiro",
  "detalhes": "Almoço",
  "situacao": "Pago",
  "cartao": "Nubank"
}
```

#### ✏️ Atualizar Transação de Crédito
```http
PUT /api/transacoes-credito/{row_index}
Content-Type: application/json
```

#### 🗑️ Deletar Transação de Crédito
```http
DELETE /api/transacoes-credito/{row_index}
```

---

### 3️⃣ **Configurações**

#### 📂 Categorias
```http
GET /api/configuracoes/categorias
POST /api/configuracoes/categorias
DELETE /api/configuracoes/categorias/{nome}
```

**Exemplo - Criar Categoria:**
```bash
curl -X POST "https://{api_url}/api/configuracoes/categorias" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Alimentação"}'
```

#### 📊 Status
```http
GET /api/configuracoes/status?tipo=DESPESA
```

**Tipos disponíveis:**
- `RECEITA` - Retorna: A receber, Recebido
- `DESPESA` - Retorna: A pagar, Pago

#### 📅 Meses
```http
GET /api/configuracoes/meses
```

**Resposta:**
```json
[
  {"nome": "Janeiro"},
  {"nome": "Fevereiro"},
  {"nome": "Março"},
  ...
]
```

#### 🏦 Contas
```http
GET /api/configuracoes/contas
POST /api/configuracoes/contas
PUT /api/configuracoes/contas/{nome_antigo}
DELETE /api/configuracoes/contas/{nome}
```

**Exemplo - Criar Conta:**
```bash
curl -X POST "https://{api_url}/api/configuracoes/contas" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Conta Corrente"}'
```

**Exemplo - Atualizar Conta:**
```bash
curl -X PUT "https://{api_url}/api/configuracoes/contas/Conta%20Corrente" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Conta Corrente Itaú"}'
```

#### 💳 Cartões
```http
GET /api/configuracoes/cartoes
POST /api/configuracoes/cartoes
PUT /api/configuracoes/cartoes/{nome_antigo}
DELETE /api/configuracoes/cartoes/{nome}
```

---

### 4️⃣ **Saldos**

#### 💰 Obter Saldo Geral
```http
GET /api/saldos
```

Retorna o saldo geral consolidado de todas as contas (célula A2 da página API).

**Resposta:**
```json
{
  "valor": "R$ 5.432,10"
}
```

**Exemplo:**
```bash
curl "https://{api_url}/api/saldos"
```

#### 🏦 Obter Saldo por Conta
```http
GET /api/saldos/contas
```

Retorna uma lista com o saldo de cada conta (tabela O:P da página API).

**Resposta:**
```json
[
  {
    "conta": "Conta Corrente",
    "saldo": "R$ 2.543,50"
  },
  {
    "conta": "Poupança",
    "saldo": "R$ 1.888,60"
  },
  {
    "conta": "Carteira",
    "saldo": "R$ 1.000,00"
  }
]
```

**Exemplo:**
```bash
curl "https://{api_url}/api/saldos/contas"
```

**Exemplo com JavaScript:**
```javascript
fetch('https://{api_url}/api/saldos/contas')
  .then(response => response.json())
  .then(contas => {
    contas.forEach(conta => {
      console.log(`${conta.conta}: ${conta.saldo}`);
    });
  });
```

---

### 5️⃣ **Health Check**

#### 🏥 Verificar Saúde da API
```http
GET /api/health
```

**Resposta (OK):**
```json
{
  "status": "ok",
  "google_sheets": "connected"
}
```

**Resposta (Erro):**
```json
{
  "status": "error",
  "google_sheets": "disconnected",
  "error": "mensagem de erro"
}
```

---

## 🔄 Fluxo Completo de Uso

### Exemplo: Adicionar e Editar uma Despesa

1. **Listar transações para ver o estado atual:**
```bash
curl "https://{api_url}/api/transacoes?mes=Janeiro"
```

2. **Criar nova transação:**
```bash
curl -X POST "https://{api_url}/api/transacoes" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Despesa",
    "descritivo": "Farmácia",
    "valor": "R$ 50,00",
    "data": "02/01/2026",
    "mes": "Janeiro",
    "detalhes": "Medicamentos",
    "situacao": "A pagar",
    "conta": "Conta Corrente"
  }'
```

3. **Listar novamente para pegar o row_index:**
```bash
curl "https://{api_url}/api/transacoes?categoria=Farmácia"
```
Resposta incluirá `"row_index": 5`

4. **Atualizar a transação para "Pago":**
```bash
curl -X PUT "https://{api_url}/api/transacoes/5" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "Despesa",
    "descritivo": "Farmácia",
    "valor": "R$ 50,00",
    "data": "02/01/2026",
    "mes": "Janeiro",
    "detalhes": "Medicamentos - pago",
    "situacao": "Pago",
    "conta": "Conta Corrente"
  }'
```

5. **Se precisar deletar:**
```bash
curl -X DELETE "https://{api_url}/api/transacoes/5"
```

---

## 📝 Notas Importantes

### row_index
- O `row_index` é o índice da linha na planilha do Google Sheets
- Sempre vem nos responses do GET
- Use esse valor para UPDATE (PUT) e DELETE
- **Atenção**: Se você deletar uma linha, os índices das linhas abaixo mudam! Sempre liste novamente após deletar

### Formatos de Data
- Use sempre o formato brasileiro: `DD/MM/YYYY`
- Exemplo: `02/01/2026` para 2 de janeiro de 2026

### Valores Monetários
- Use o formato: `R$ 150,00`
- Com cifrão, espaço e vírgula para centavos

### Paginação
- `page`: número da página (começa em 1)
- `page_size`: itens por página (máximo 100)
- `total_pages`: total de páginas disponíveis

### Ordenação
- Use `order_by` para ordenar resultados
- Valores válidos: `data`, `tipo`, `categoria`, `valor`, `situacao`, `conta` (ou `cartao` para crédito)
- Padrão: ordenado por `data`

---

## 🚀 Exemplos com JavaScript/Fetch

### Listar Transações
```javascript
fetch('https://{api_url}/api/transacoes?mes=Janeiro')
  .then(response => response.json())
  .then(data => console.log(data.items));
```

### Criar Transação
```javascript
fetch('https://{api_url}/api/transacoes', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    tipo: 'Despesa',
    descritivo: 'Supermercado',
    valor: 'R$ 150,00',
    data: '02/01/2026',
    mes: 'Janeiro',
    detalhes: 'Compras mensais',
    situacao: 'Pago',
    conta: 'Conta Corrente'
  })
})
  .then(response => response.json())
  .then(data => console.log('Criado:', data));
```

### Atualizar Transação
```javascript
fetch('https://{api_url}/api/transacoes/2', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    tipo: 'Despesa',
    descritivo: 'Supermercado Extra',
    valor: 'R$ 200,00',
    data: '02/01/2026',
    mes: 'Janeiro',
    detalhes: 'Atualizado',
    situacao: 'Pago',
    conta: 'Conta Corrente'
  })
})
  .then(response => response.json())
  .then(data => console.log('Atualizado:', data));
```

### Deletar Transação
```javascript
fetch('https://{api_url}/api/transacoes/2', {
  method: 'DELETE'
})
  .then(response => response.json())
  .then(data => console.log('Deletado:', data.message));
```

---

## 🐛 Troubleshooting

### Erro 400 (Bad Request)
- Verifique se todos os campos obrigatórios estão preenchidos
- Verifique o formato da data (DD/MM/YYYY)
- Verifique se o valor está no formato correto

### Erro 404 (Not Found)
- Verifique se o `row_index` existe
- Liste as transações para ver os índices atuais

### Erro 500 (Internal Server Error)
- Verifique se as configurações do Google Sheets estão corretas
- Verifique os logs da aplicação
- Teste o endpoint `/api/health`

---

## 📞 Suporte

Para mais informações, acesse a documentação interativa em `/docs` 🚀
