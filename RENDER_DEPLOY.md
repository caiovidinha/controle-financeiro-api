# Configuração do Render

## Build Command
```bash
pip install -r requirements.txt
```

## Start Command
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables
Você precisa adicionar as seguintes variáveis de ambiente no Render Dashboard:

### Obrigatórias (para funcionalidade completa):
- `GOOGLE_SHEETS_ID` - ID da planilha do Google Sheets (encontrado na URL da planilha)
- `GOOGLE_SERVICE_ACCOUNT_EMAIL` - Email da conta de serviço do Google (ex: `xxx@xxx.iam.gserviceaccount.com`)
- `GOOGLE_PRIVATE_KEY` - Chave privada da conta de serviço (incluindo `-----BEGIN PRIVATE KEY-----` e `-----END PRIVATE KEY-----`)
  - **IMPORTANTE**: No Render, cole a chave completa com as quebras de linha. Se tiver problemas, substitua `\n` por quebras de linha reais.

### Opcionais (com valores padrão):
- `PORT` - Porta do servidor (padrão: 10000 no Render)
- `APP_NAME` - Nome da aplicação (padrão: "API Controle Financeiro")
- `GOOGLE_SHEET_NAME` - Nome da aba principal (padrão: "Extrato")
- `CORS_ORIGINS` - Lista de origens permitidas para CORS (padrão: "*")

### Como configurar no Render:
1. Vá para o seu serviço no Dashboard
2. Clique em "Environment" no menu lateral
3. Adicione cada variável clicando em "Add Environment Variable"
4. Para `GOOGLE_PRIVATE_KEY`, use o tipo "Secret" ao invés de "Plain Text"

## Python Version
O projeto usa Python 3.12.0 (definido em `.python-version` e `runtime.txt`)

## Instance Type
Recomendado: **Web Service** (não Private Service)

## Region
Escolha a região mais próxima dos seus usuários (ex: Oregon para Brasil)

## Passos para Deploy:

1. **Crie um novo Web Service no Render Dashboard**
   - Vá em: https://dashboard.render.com
   - Clique em "New +" > "Web Service"
   - Conecte seu repositório GitHub

2. **Configure o serviço:**
   - **Name**: `controle-financeiro-api` (ou o nome que preferir)
   - **Language**: Python
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Adicione as variáveis de ambiente:**
   - Clique em "Advanced"
   - Adicione cada variável de ambiente listada acima

4. **Escolha o Instance Type:**
   - Free (para testes) ou Starter/Standard (para produção)

5. **Clique em "Create Web Service"**

## Verificar Deploy

Após o deploy, você pode verificar se a API está funcionando acessando:
- `https://seu-servico.onrender.com/` - Endpoint raiz
- `https://seu-servico.onrender.com/docs` - Documentação Swagger
- `https://seu-servico.onrender.com/api/health` - Health check

## Troubleshooting

### Erro: "Build failed - pydantic-core compilation error"
✅ **Solução**: As versões foram atualizadas no `requirements.txt` para usar wheels pré-compilados

### Erro: "Service not binding to port"
✅ **Solução**: O `main.py` já está configurado para usar `PORT` do ambiente e bind em `0.0.0.0`

### Erro: "Google Sheets authentication failed"
- Verifique se a variável `GOOGLE_SHEETS_CREDENTIALS_JSON` contém o JSON completo
- Verifique se o `GOOGLE_SHEET_ID` está correto
- Verifique se as permissões da conta de serviço estão configuradas corretamente

### Free Instance Limitations
- O serviço pode "dormir" após 15 minutos de inatividade
- O primeiro request após inatividade pode levar ~30 segundos
- Considere usar um serviço de ping (ex: UptimeRobot) ou upgrade para Starter
