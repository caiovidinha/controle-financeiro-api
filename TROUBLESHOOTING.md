# Troubleshooting: "No open ports detected on 0.0.0.0"

## O que significa esse erro?
O Render não conseguiu detectar que sua aplicação está escutando em uma porta. Isso pode acontecer por vários motivos.

## Soluções (em ordem de prioridade):

### 1. ✅ Verificar o Start Command
No Render Dashboard, verifique se o **Start Command** está correto:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

**NÃO use**:
- ~~`uvicorn main:app --host 0.0.0.0 --port $PORT`~~ (pode não funcionar)
- ~~`python main.py`~~ (não recomendado para produção)

### 2. ✅ Verificar variáveis de ambiente obrigatórias
Se as variáveis de ambiente obrigatórias não estiverem configuradas, a aplicação pode falhar ao iniciar:

**Configure no Render Dashboard > Environment:**
- `GOOGLE_SHEETS_ID`
- `GOOGLE_SERVICE_ACCOUNT_EMAIL`
- `GOOGLE_PRIVATE_KEY` (tipo: Secret)

### 3. ✅ Verificar os logs de build
No Render Dashboard, vá em **Logs** e procure por:

#### Erros de build:
```
ERROR: Could not install packages due to...
```
**Solução**: Verifique se `requirements.txt` está correto e com versões compatíveis.

#### Erros de importação:
```
ModuleNotFoundError: No module named 'xxx'
```
**Solução**: Adicione o módulo ao `requirements.txt`.

#### Erros de configuração:
```
pydantic.error_wrappers.ValidationError
```
**Solução**: Configure as variáveis de ambiente obrigatórias.

### 4. ✅ Verificar a versão do Python
Certifique-se de que está usando Python 3.12:

Arquivos que definem a versão:
- `.python-version` → `3.12.0`
- `runtime.txt` → `python-3.12.0`

### 5. ✅ Verificar o Build Command
No Render Dashboard, o **Build Command** deve ser:

```bash
pip install -r requirements.txt
```

### 6. ✅ Aguardar tempo suficiente
O primeiro deploy pode levar de 2-5 minutos. Aguarde e monitore os logs.

### 7. ✅ Testar localmente primeiro
Antes de fazer deploy, teste localmente:

```bash
# Ative o ambiente virtual
source env/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute com a mesma configuração do Render
PORT=10000 python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

Se funcionar localmente, o problema está na configuração do Render.

## Checklist de Deploy:

- [ ] `.python-version` existe com `3.12.0`
- [ ] `runtime.txt` existe com `python-3.12.0`
- [ ] `requirements.txt` atualizado com versões compatíveis
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Variáveis de ambiente configuradas no Render Dashboard
- [ ] Instance Type: **Web Service** (não Private Service)
- [ ] Health Check Path: `/api/health`

## Se nada funcionar:

1. **Delete e recrie o serviço** no Render
2. **Use o `render.yaml`** para deploy automático (commit e push)
3. **Contate o suporte do Render** com os logs completos

## Comandos úteis para debug:

```bash
# Ver logs em tempo real no Render Dashboard
# Vá em: Dashboard > Seu Serviço > Logs

# Testar health check localmente
curl http://localhost:10000/api/health

# Verificar se a porta está aberta
netstat -tuln | grep 10000
```

## Causas comuns do erro:

1. ❌ Aplicação não iniciou (erro fatal ao carregar)
2. ❌ Aplicação iniciou mas travou (loop infinito, deadlock)
3. ❌ Aplicação está escutando na porta errada
4. ❌ Aplicação está escutando em 127.0.0.1 em vez de 0.0.0.0
5. ❌ Aplicação leva muito tempo para iniciar (>60s timeout)
6. ❌ Variáveis de ambiente faltando causando crash

## Solução definitiva:

Se você seguiu todos os passos acima e ainda não funciona, o problema mais provável é:

**Variáveis de ambiente não configuradas** → A aplicação tenta iniciar, falha ao conectar com Google Sheets, e trava antes de abrir a porta.

**Solução**: Configure TODAS as variáveis de ambiente no Render Dashboard ANTES de fazer o deploy.
