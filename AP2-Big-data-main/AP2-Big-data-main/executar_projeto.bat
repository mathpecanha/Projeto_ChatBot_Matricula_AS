@echo off
echo ========================================
echo    CHATBOT DE MATRICULA - IBMEC
echo ========================================
echo.

echo Iniciando o Backend Spring Boot...
echo.
cd backend-springboot
start "Backend Spring Boot" cmd /k "mvnw.cmd spring-boot:run"

echo Aguardando 10 segundos para o backend inicializar...
timeout /t 10 /nobreak

echo.
echo Iniciando o Bot...
echo.
cd ../bot
start "Bot Framework" cmd /k "python app.py"

echo.
echo ========================================
echo PROJETO INICIADO COM SUCESSO!
echo ========================================
echo.
echo Backend: http://localhost:8080
echo Bot: http://localhost:3978
echo.
echo Use o Bot Framework Emulator para testar:
echo Endpoint: http://localhost:3978/api/messages
echo.
echo Pressione qualquer tecla para sair...
pause 