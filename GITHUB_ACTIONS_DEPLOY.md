# 🚀 Deploy via GitHub Actions

Este guia explica como configurar o deploy automático do backend Flask no Azure usando GitHub Actions.

## 📋 Pré-requisitos

1. **Repositório no GitHub** com seu código
2. **Conta Azure** com permissões de administrador
3. **Azure CLI** instalado localmente

## 🔧 Configuração do Azure

### 1. Criar App Service no Azure

```bash
# Login no Azure
az login

# Criar Resource Group
az group create --name ibmec-backend-rg --location "East US"

# Criar App Service Plan
az appservice plan create --name ibmec-backend-plan --resource-group ibmec-backend-rg --sku B1 --is-linux

# Criar Web App
az webapp create --resource-group ibmec-backend-rg --plan ibmec-backend-plan --name ibmec-backend-api --runtime "PYTHON|3.9"

# Configurar variáveis de ambiente
az webapp config appsettings set --resource-group ibmec-backend-rg --name ibmec-backend-api --settings FLASK_ENV=production FLASK_APP=run.py

# Configurar startup command
az webapp config set --resource-group ibmec-backend-rg --name ibmec-backend-api --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 run:app"
```

### 2. Obter Publish Profile (Método 1 - Mais Simples)

```bash
# Gerar publish profile
az webapp deployment list-publishing-profiles --resource-group ibmec-backend-rg --name ibmec-backend-api --xml
```

Copie todo o conteúdo XML gerado.

### 3. Criar Service Principal (Método 2 - Mais Seguro)

```bash
# Criar Service Principal
az ad sp create-for-rbac --name "github-actions-ibmec" --role contributor --scopes /subscriptions/{subscription-id}/resourceGroups/ibmec-backend-rg --sdk-auth
```

Copie todo o JSON gerado.

## 🔧 Configuração do GitHub

### 1. Acesse seu repositório no GitHub

### 2. Vá em Settings > Secrets and variables > Actions

### 3. Adicione os secrets:

#### **Para Publish Profile (Método 1):**
- **Name:** `AZURE_WEBAPP_PUBLISH_PROFILE`
- **Value:** Cole o XML do publish profile

#### **Para Service Principal (Método 2):**
- **Name:** `AZURE_CREDENTIALS`
- **Value:** Cole o JSON do service principal

### 4. Escolha o Workflow

#### **Opção A: Workflow Simples (Publish Profile)**
Use o arquivo: `.github/workflows/deploy-azure.yml`

#### **Opção B: Workflow Avançado (Service Principal)**
Use o arquivo: `.github/workflows/deploy-azure-advanced.yml`

### 5. Personalize o Workflow

Edite o arquivo escolhido e altere:

```yaml
env:
  AZURE_WEBAPP_NAME: seu-app-name-aqui
  RESOURCE_GROUP: seu-resource-group-aqui
```

## 🚀 Fazendo o Deploy

### 1. Commit e Push

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### 2. Verificar o Deploy

1. Vá para a aba **Actions** no GitHub
2. Clique no workflow que está rodando
3. Acompanhe os logs em tempo real

### 3. Testar a Aplicação

Após o deploy, teste:
- **API:** `https://seu-app-name.azurewebsites.net/api/matriculas`
- **Swagger:** `https://seu-app-name.azurewebsites.net/docs`

## 🔄 Deploy Automático

Agora, sempre que você fizer push para a branch `main` ou `master`, o deploy será automático!

## 📊 Monitoramento

### 1. Logs do GitHub Actions
- Acesse: `https://github.com/seu-usuario/seu-repo/actions`

### 2. Logs do Azure
```bash
az webapp log tail --resource-group ibmec-backend-rg --name ibmec-backend-api
```

### 3. Métricas no Azure Portal
- Acesse o App Service
- Vá em "Métricas"

## 🔧 Configurações Avançadas

### 1. Deploy Manual
Para executar o deploy manualmente:
1. Vá em Actions no GitHub
2. Clique no workflow
3. Clique em "Run workflow"

### 2. Deploy em Branches Específicas
Edite o workflow:

```yaml
on:
  push:
    branches: [ main, develop, staging ]
```

### 3. Deploy com Aprovação
Adicione ao workflow:

```yaml
jobs:
  deploy:
    environment: production
    needs: build
    runs-on: ubuntu-latest
    steps:
      # ... steps de deploy
```

### 4. Notificações
Adicione ao workflow:

```yaml
- name: Notify on success
  if: success()
  run: |
    echo "Deploy successful!"
    # Adicione notificação via Slack, Teams, etc.

- name: Notify on failure
  if: failure()
  run: |
    echo "Deploy failed!"
    # Adicione notificação de erro
```

## 🆘 Troubleshooting

### Problema: Erro de autenticação
**Solução:** Verifique se os secrets estão corretos no GitHub

### Problema: Erro de dependências
**Solução:** Verifique se o `requirements.txt` está correto

### Problema: App não inicia
**Solução:** Verifique os logs do Azure:
```bash
az webapp log tail --resource-group ibmec-backend-rg --name ibmec-backend-api
```

### Problema: Timeout no deploy
**Solução:** Aumente o timeout no startup command:
```
gunicorn --bind=0.0.0.0 --timeout 1200 run:app
```

## 📞 Suporte

- **GitHub Actions Docs:** [docs.github.com/actions](https://docs.github.com/actions)
- **Azure Web Apps:** [docs.microsoft.com/azure/app-service](https://docs.microsoft.com/azure/app-service)
- **Community:** [Stack Overflow](https://stackoverflow.com/questions/tagged/github-actions) 