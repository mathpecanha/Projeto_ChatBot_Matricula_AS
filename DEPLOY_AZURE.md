# 🚀 Deploy do Backend no Azure

Este guia explica como fazer o deploy do backend Flask no Azure App Service.

## 📋 Pré-requisitos

1. **Conta Azure** - Crie uma conta gratuita em [azure.microsoft.com](https://azure.microsoft.com)
2. **Azure CLI** - Instale em [docs.microsoft.com/cli/azure/install-azure-cli](https://docs.microsoft.com/cli/azure/install-azure-cli)
3. **Git** - Instale em [git-scm.com](https://git-scm.com)

## 🔧 Método 1: Deploy Automatizado (Recomendado)

### 1. Execute o script PowerShell:

```powershell
# Navegue até a pasta do projeto
cd "AP2-Big-data-main/AP2-Big-data-main"

# Execute o script de deploy
.\deploy-azure.ps1
```

### 2. Parâmetros opcionais:

```powershell
.\deploy-azure.ps1 -ResourceGroupName "meu-rg" -AppName "minha-api" -Location "Brazil South" -Sku "B1"
```

## 🔧 Método 2: Deploy Manual

### 1. Login no Azure:

```bash
az login
```

### 2. Criar Resource Group:

```bash
az group create --name ibmec-backend-rg --location "East US"
```

### 3. Criar App Service Plan:

```bash
az appservice plan create --name ibmec-backend-plan --resource-group ibmec-backend-rg --sku B1 --is-linux
```

### 4. Criar Web App:

```bash
az webapp create --resource-group ibmec-backend-rg --plan ibmec-backend-plan --name ibmec-backend-api --runtime "PYTHON|3.9"
```

### 5. Configurar variáveis de ambiente:

```bash
az webapp config appsettings set --resource-group ibmec-backend-rg --name ibmec-backend-api --settings FLASK_ENV=production FLASK_APP=run.py
```

### 6. Configurar startup command:

```bash
az webapp config set --resource-group ibmec-backend-rg --name ibmec-backend-api --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 run:app"
```

### 7. Fazer deploy do código:

```bash
# Configurar Git
git init
git add .
git commit -m "Deploy inicial"

# Configurar deploy
az webapp deployment source config-local-git --resource-group ibmec-backend-rg --name ibmec-backend-api

# Fazer push
git remote add azure <URL_DO_GIT>
git push azure master
```

## 🔧 Método 3: Deploy via Azure Portal

### 1. Acesse o [Azure Portal](https://portal.azure.com)

### 2. Crie um novo App Service:
- **Runtime Stack**: Python 3.9
- **Operating System**: Linux
- **Region**: East US (ou sua preferência)
- **Pricing Plan**: Basic B1

### 3. Configure as variáveis de ambiente:
- `FLASK_ENV` = `production`
- `FLASK_APP` = `run.py`

### 4. Configure o startup command:
```
gunicorn --bind=0.0.0.0 --timeout 600 run:app
```

### 5. Faça upload dos arquivos via FTP ou Git

## 🌐 URLs Importantes

Após o deploy, você terá acesso a:

- **API Base**: `https://seu-app-name.azurewebsites.net`
- **Documentação Swagger**: `https://seu-app-name.azurewebsites.net/docs`
- **Endpoint Matrículas**: `https://seu-app-name.azurewebsites.net/api/matriculas`

## 🔄 Atualizar o Bot

Após o deploy, atualize a configuração do bot:

### 1. Via variável de ambiente:

```bash
export API_BASE_URL="https://seu-app-name.azurewebsites.net"
export ENVIRONMENT="production"
```

### 2. Ou edite o arquivo `bot/config.py`:

```python
API_BASE_URL = "https://seu-app-name.azurewebsites.net"
ENVIRONMENT = "production"
```

## 🧪 Testar o Deploy

### 1. Teste a API:

```bash
# Teste GET
curl https://seu-app-name.azurewebsites.net/api/matriculas

# Teste POST
curl -X POST https://seu-app-name.azurewebsites.net/api/matriculas \
  -H "Content-Type: application/json" \
  -d '{"nome":"Teste","email":"teste@exemplo.com","curso":"Engenharia"}'
```

### 2. Teste no navegador:
- Acesse: `https://seu-app-name.azurewebsites.net/docs`
- Teste os endpoints via Swagger UI

## 📊 Monitoramento

### 1. Logs da aplicação:
```bash
az webapp log tail --resource-group ibmec-backend-rg --name ibmec-backend-api
```

### 2. Métricas no Azure Portal:
- Acesse o App Service no portal
- Vá para "Métricas"
- Monitore CPU, memória, requisições

## 🔒 Segurança

### 1. Configurar HTTPS:
- O Azure já fornece HTTPS automaticamente
- Certificado SSL gratuito incluído

### 2. Configurar CORS (se necessário):
```python
# No arquivo app/__init__.py
from flask_cors import CORS

CORS(app, origins=['https://seu-bot-domain.com'])
```

## 💰 Custos

- **Basic B1**: ~$13/mês
- **Free F1**: Gratuito (com limitações)
- **Standard S1**: ~$73/mês

## 🆘 Troubleshooting

### Problema: App não inicia
**Solução**: Verifique os logs:
```bash
az webapp log tail --resource-group ibmec-backend-rg --name ibmec-backend-api
```

### Problema: Erro de dependências
**Solução**: Verifique se o `requirements.txt` está correto

### Problema: Timeout
**Solução**: Aumente o timeout no startup command:
```
gunicorn --bind=0.0.0.0 --timeout 1200 run:app
```

## 📞 Suporte

- **Azure Support**: [support.microsoft.com](https://support.microsoft.com)
- **Documentação**: [docs.microsoft.com/azure/app-service](https://docs.microsoft.com/azure/app-service)
- **Community**: [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-app-service) 