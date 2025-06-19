# Chatbot de Matrícula - IBMEC

## Descrição do Projeto

Este projeto implementa um chatbot local utilizando o Bot Framework SDK para atender usuários com perguntas frequentes e realizar matrícula via integração com backend em Spring Boot.

## Funcionalidades

1. **Atendimento a perguntas frequentes:**
   - Calendário acadêmico
   - Como emitir boleto
   - Horários de aula
   - Contato da secretaria
   - Informações sobre cursos

2. **Processo de matrícula:**
   - Coleta de nome, e-mail e curso
   - Validação dos dados
   - Envio dos dados ao backend
   - Confirmação da matrícula

3. **Backend REST API:**
   - Endpoint POST `/api/matriculas`
   - Armazenamento em banco de dados H2
   - Validação de dados duplicados

## Arquitetura

- **Bot (Python):** Usa Bot Framework SDK
- **Backend (Spring Boot):** API REST com JPA/Hibernate
- **Banco de Dados:** H2 (em memória para desenvolvimento)

## Como Executar

### 1. Executar o Backend (Spring Boot)

```bash
cd backend-springboot

# Se você tem Maven instalado:
mvn spring-boot:run

# Ou se você tem Java 17+ instalado:
./mvnw spring-boot:run  # Linux/Mac
mvnw.cmd spring-boot:run  # Windows
```

O backend estará disponível em: `http://localhost:8080`

**Endpoints disponíveis:**
- `GET /api/matriculas/health` - Verificar se a API está funcionando
- `POST /api/matriculas` - Criar nova matrícula
- `GET /api/matriculas` - Listar todas as matrículas
- `GET /api/matriculas/{id}` - Buscar matrícula por ID
- `GET /h2-console` - Console do banco H2

### 2. Executar o Bot (Python)

```bash
cd bot

# Instalar dependências (se ainda não instalou):
pip install -r ../requirements.txt

# Executar o bot:
python app.py
```

O bot estará disponível em: `http://localhost:3978`

### 3. Testar o Bot

Use o **Bot Framework Emulator** para testar:

1. Baixe o Bot Framework Emulator: https://github.com/Microsoft/BotFramework-Emulator
2. Abra o emulator
3. Conecte-se ao endpoint: `http://localhost:3978/api/messages`
4. Deixe App ID e App Password em branco para desenvolvimento local

## Exemplos de Uso

### Perguntas Frequentes

- "Qual o calendário acadêmico?"
- "Como emitir boleto?"
- "Quais os horários de aula?"
- "Secretaria"
- "Cursos"

### Processo de Matrícula

1. Digite: "quero me matricular"
2. Informe seu nome completo
3. Informe seu email
4. Escolha um curso:
   - Engenharia
   - Administração
   - Direito
   - Medicina
   - Tecnologia da Informação
5. Confirme os dados

### Exemplo de JSON para teste da API

```json
POST http://localhost:8080/api/matriculas
Content-Type: application/json

{
    "nome": "João Silva",
    "email": "joao@email.com",
    "curso": "Engenharia"
}
```

## Estrutura do Projeto

```
AP2-Big-data-main/
├── bot/                          # Bot em Python
│   ├── dialogs/
│   │   ├── main_dialog.py       # Diálogo principal
│   │   └── matricula_dialog.py  # Diálogo de matrícula
│   ├── data/
│   │   └── faq.json            # Perguntas frequentes
│   └── app.py                  # Aplicação principal do bot
├── backend-springboot/          # Backend em Spring Boot
│   ├── src/main/java/com/ibmec/chatbot/
│   │   ├── controller/         # Controllers REST
│   │   ├── service/           # Lógica de negócio
│   │   ├── entity/            # Entidades JPA
│   │   ├── dto/               # DTOs
│   │   └── repository/        # Repositórios JPA
│   └── pom.xml                # Dependências Maven
└── app/                        # Backend Flask (original)
```

## Tecnologias Utilizadas

### Bot
- Python 3.x
- Bot Framework SDK
- aiohttp
- requests

### Backend
- Java 17
- Spring Boot 3.2.0
- Spring Data JPA
- H2 Database
- Maven

## Logs e Monitoramento

- **Backend:** Logs detalhados no console e arquivo
- **Bot:** Logs de erro e informações importantes
- **H2 Console:** Acesse `http://localhost:8080/h2-console` para visualizar dados

## Deployment no Azure

Para publicar no Azure:

1. **Backend:** Use Azure App Service com Java 17
2. **Bot:** Configure Azure Bot Service
3. **Banco:** Use Azure SQL Database em produção

## Troubleshooting

### Problemas Comuns

1. **Porta 8080 ocupada:**
   - Altere a porta no `application.properties`
   - Atualize a URL no bot

2. **Bot não conecta ao backend:**
   - Verifique se o backend está rodando
   - Confirme a URL no `matricula_dialog.py`

3. **Erro de CORS:**
   - O backend já está configurado com `@CrossOrigin(origins = "*")`

### Verificação de Status

```bash
# Verificar se o backend está funcionando:
curl http://localhost:8080/api/matriculas/health

# Verificar se o bot está funcionando:
curl http://localhost:3978
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request 