@echo off
echo Testando API de Matriculas...
echo.

echo Testando GET /api/matriculas...
curl -X GET http://localhost:8080/api/matriculas
echo.
echo.

echo Testando POST /api/matriculas...
curl -X POST http://localhost:8080/api/matriculas ^
  -H "Content-Type: application/json" ^
  -d "{\"nome\":\"Teste Bot\",\"email\":\"teste.bot@exemplo.com\",\"curso\":\"Engenharia\"}"
echo.
echo.

pause 