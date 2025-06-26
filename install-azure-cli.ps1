# Script para instalar Azure CLI
# Autor: Assistente IA

Write-Host "🚀 Instalando Azure CLI..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green

# Verificar se já está instalado
try {
    $azVersion = az version --output json 2>$null | ConvertFrom-Json
    Write-Host "✅ Azure CLI já está instalado - Versão: $($azVersion.'azure-cli')" -ForegroundColor Green
    Write-Host "Tente executar: az login" -ForegroundColor Yellow
    exit 0
} catch {
    Write-Host "Azure CLI não encontrado. Instalando..." -ForegroundColor Yellow
}

# URL do instalador do Azure CLI
$installerUrl = "https://aka.ms/installazurecliwindows"
$installerPath = "$env:TEMP\AzureCLI.msi"

Write-Host "📥 Baixando Azure CLI..." -ForegroundColor Yellow

try {
    # Baixar o instalador
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✅ Download concluído" -ForegroundColor Green
    
    Write-Host "🔧 Instalando Azure CLI..." -ForegroundColor Yellow
    
    # Instalar silenciosamente
    Start-Process msiexec.exe -Wait -ArgumentList "/I $installerPath /quiet /norestart"
    
    Write-Host "✅ Instalação concluída!" -ForegroundColor Green
    
    # Limpar arquivo temporário
    Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
    
    Write-Host "🔄 Reiniciando PowerShell para carregar o Azure CLI..." -ForegroundColor Yellow
    Write-Host "Execute novamente este script após reiniciar o PowerShell" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ Erro durante a instalação: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "📋 Instalação Manual:" -ForegroundColor Yellow
    Write-Host "1. Acesse: https://docs.microsoft.com/cli/azure/install-azure-cli-windows" -ForegroundColor White
    Write-Host "2. Baixe o instalador MSI" -ForegroundColor White
    Write-Host "3. Execute o instalador" -ForegroundColor White
    Write-Host "4. Reinicie o PowerShell" -ForegroundColor White
    Write-Host "5. Execute: az login" -ForegroundColor White
}

Write-Host "================================================" -ForegroundColor Green 