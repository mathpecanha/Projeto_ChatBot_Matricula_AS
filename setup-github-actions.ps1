# Script para configurar GitHub Actions
# Autor: Assistente IA

param(
    [string]$AppName = "ibmec-backend-api",
    [string]$ResourceGroup = "ibmec-backend-rg",
    [string]$Location = "East US"
)

Write-Host "🚀 Configurando GitHub Actions para Deploy no Azure..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Verificar se Azure CLI está instalado
try {
    $azVersion = az version --output json 2>$null | ConvertFrom-Json
    Write-Host "✅ Azure CLI encontrado - Versão: $($azVersion.'azure-cli')" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI não encontrado. Execute primeiro: .\install-azure-cli.ps1" -ForegroundColor Red
    exit 1
}

# Verificar login no Azure
try {
    $account = az account show --output json 2>$null | ConvertFrom-Json
    Write-Host "✅ Logado no Azure como: $($account.user.name)" -ForegroundColor Green
} catch {
    Write-Host "🔐 Fazendo login no Azure..." -ForegroundColor Yellow
    az login
}

Write-Host "📦 Criando recursos no Azure..." -ForegroundColor Yellow

# Criar Resource Group
Write-Host "   Criando Resource Group: $ResourceGroup" -ForegroundColor Cyan
az group create --name $ResourceGroup --location $Location --output none

# Criar App Service Plan
Write-Host "   Criando App Service Plan..." -ForegroundColor Cyan
az appservice plan create --name "$AppName-plan" --resource-group $ResourceGroup --sku B1 --is-linux --output none

# Criar Web App
Write-Host "   Criando Web App: $AppName" -ForegroundColor Cyan
az webapp create --resource-group $ResourceGroup --plan "$AppName-plan" --name $AppName --runtime "PYTHON|3.9" --output none

# Configurar variáveis de ambiente
Write-Host "   Configurando variáveis de ambiente..." -ForegroundColor Cyan
az webapp config appsettings set --resource-group $ResourceGroup --name $AppName --settings FLASK_ENV=production FLASK_APP=run.py --output none

# Configurar startup command
Write-Host "   Configurando comando de inicialização..." -ForegroundColor Cyan
az webapp config set --resource-group $ResourceGroup --name $AppName --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 run:app" --output none

Write-Host "✅ Recursos criados com sucesso!" -ForegroundColor Green

# Gerar Publish Profile
Write-Host "📄 Gerando Publish Profile..." -ForegroundColor Yellow
$publishProfile = az webapp deployment list-publishing-profiles --resource-group $ResourceGroup --name $AppName --xml --output tsv

Write-Host "================================================" -ForegroundColor Green
Write-Host "🎯 PRÓXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Green

Write-Host "1. 📋 Copie o Publish Profile abaixo:" -ForegroundColor Cyan
Write-Host "   (Cole no GitHub Secrets como AZURE_WEBAPP_PUBLISH_PROFILE)" -ForegroundColor White
Write-Host ""

# Salvar publish profile em arquivo
$publishProfile | Out-File -FilePath "publish-profile.xml" -Encoding UTF8
Write-Host "   ✅ Publish Profile salvo em: publish-profile.xml" -ForegroundColor Green

Write-Host ""
Write-Host "2. 🔧 Configure o GitHub:" -ForegroundColor Cyan
Write-Host "   - Vá para seu repositório no GitHub" -ForegroundColor White
Write-Host "   - Settings > Secrets and variables > Actions" -ForegroundColor White
Write-Host "   - Adicione secret: AZURE_WEBAPP_PUBLISH_PROFILE" -ForegroundColor White
Write-Host "   - Cole o conteúdo do arquivo publish-profile.xml" -ForegroundColor White

Write-Host ""
Write-Host "3. 📝 Personalize o workflow:" -ForegroundColor Cyan
Write-Host "   - Edite .github/workflows/deploy-azure.yml" -ForegroundColor White
Write-Host "   - Altere AZURE_WEBAPP_NAME para: $AppName" -ForegroundColor White

Write-Host ""
Write-Host "4. 🚀 Faça o deploy:" -ForegroundColor Cyan
Write-Host "   git add ." -ForegroundColor White
Write-Host "   git commit -m 'Add GitHub Actions workflow'" -ForegroundColor White
Write-Host "   git push origin main" -ForegroundColor White

Write-Host ""
Write-Host "5. 🌐 URLs da aplicação:" -ForegroundColor Cyan
Write-Host "   - API: https://$AppName.azurewebsites.net/api/matriculas" -ForegroundColor White
Write-Host "   - Swagger: https://$AppName.azurewebsites.net/docs" -ForegroundColor White

Write-Host ""
Write-Host "6. 📊 Monitoramento:" -ForegroundColor Cyan
Write-Host "   - GitHub Actions: https://github.com/seu-usuario/seu-repo/actions" -ForegroundColor White
Write-Host "   - Azure Portal: https://portal.azure.com" -ForegroundColor White

Write-Host "================================================" -ForegroundColor Green
Write-Host "🎉 Configuração concluída!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green 