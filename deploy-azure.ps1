# Script de Deploy para Azure App Service
# Autor: Assistente IA
# Data: 2024

param(
    [string]$ResourceGroupName = "ibmec-backend-rg",
    [string]$AppName = "ibmec-backend-api",
    [string]$Location = "East US",
    [string]$Sku = "B1"
)

Write-Host "🚀 Iniciando Deploy do Backend no Azure..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Verificar se Azure CLI está instalado
try {
    $azVersion = az version --output json | ConvertFrom-Json
    Write-Host "✅ Azure CLI encontrado - Versão: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI não encontrado. Instale em: https://docs.microsoft.com/cli/azure/install-azure-cli" -ForegroundColor Red
    exit 1
}

# Verificar login no Azure
try {
    $account = az account show --output json | ConvertFrom-Json
    Write-Host "✅ Logado no Azure como: $($account.user.name)" -ForegroundColor Green
} catch {
    Write-Host "🔐 Fazendo login no Azure..." -ForegroundColor Yellow
    az login
}

# Criar Resource Group
Write-Host "📦 Criando Resource Group: $ResourceGroupName" -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location

# Criar App Service Plan
Write-Host "🏗️  Criando App Service Plan..." -ForegroundColor Yellow
az appservice plan create --name "$AppName-plan" --resource-group $ResourceGroupName --sku $Sku --is-linux

# Criar Web App
Write-Host "🌐 Criando Web App: $AppName" -ForegroundColor Yellow
az webapp create --resource-group $ResourceGroupName --plan "$AppName-plan" --name $AppName --runtime "PYTHON|3.9"

# Configurar variáveis de ambiente
Write-Host "⚙️  Configurando variáveis de ambiente..." -ForegroundColor Yellow
az webapp config appsettings set --resource-group $ResourceGroupName --name $AppName --settings FLASK_ENV=production FLASK_APP=run.py

# Configurar startup command
Write-Host "🚀 Configurando comando de inicialização..." -ForegroundColor Yellow
az webapp config set --resource-group $ResourceGroupName --name $AppName --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 run:app"

# Fazer deploy do código
Write-Host "📤 Fazendo deploy do código..." -ForegroundColor Yellow
az webapp deployment source config-local-git --resource-group $ResourceGroupName --name $AppName

# Obter URL do Git
$gitUrl = az webapp deployment source config-local-git --resource-group $ResourceGroupName --name $AppName --query url --output tsv
Write-Host "🔗 URL do Git: $gitUrl" -ForegroundColor Cyan

# Configurar Git e fazer push
Write-Host "📝 Configurando Git e fazendo push..." -ForegroundColor Yellow
git init
git add .
git commit -m "Deploy inicial no Azure"
git remote add azure $gitUrl
git push azure master

# Obter URL da aplicação
$appUrl = az webapp show --resource-group $ResourceGroupName --name $AppName --query defaultHostName --output tsv
$fullUrl = "https://$appUrl"

Write-Host "================================================" -ForegroundColor Green
Write-Host "🎉 Deploy concluído com sucesso!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "🌐 URL da aplicação: $fullUrl" -ForegroundColor Cyan
Write-Host "📚 Documentação Swagger: $fullUrl/docs" -ForegroundColor Cyan
Write-Host "📋 API Matrículas: $fullUrl/api/matriculas" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Green

# Testar a API
Write-Host "🧪 Testando a API..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$fullUrl/api/matriculas" -Method GET -TimeoutSec 30
    Write-Host "✅ API funcionando! Matrículas encontradas: $($response.Count)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  API ainda não está respondendo (pode levar alguns minutos para inicializar)" -ForegroundColor Yellow
}

Write-Host "================================================" -ForegroundColor Green
Write-Host "📋 Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Atualizar a URL da API no bot para: $fullUrl" -ForegroundColor White
Write-Host "2. Testar os endpoints da API" -ForegroundColor White
Write-Host "3. Configurar CORS se necessário" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Green 