from app import create_app
from app.database import db
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

def init_db():
    try:
        with app.app_context():
            logger.info("Criando tabelas do banco de dados...")
            db.create_all()
            logger.info("Tabelas criadas com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao criar tabelas: {str(e)}")
        raise

if __name__ == '__main__':
    init_db()
    logger.info("Iniciando servidor Flask na porta 8080...")
    logger.info("Backend disponível em: http://localhost:8080")
    logger.info("Documentação Swagger em: http://localhost:8080/docs")
    logger.info("Endpoint de matrícula: POST http://localhost:8080/api/matriculas")
    app.run(debug=True, host='0.0.0.0', port=8080)
