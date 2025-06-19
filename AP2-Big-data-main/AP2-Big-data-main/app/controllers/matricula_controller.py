from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.database import db
from app.models.matricula import Matricula
import logging
import json

# Configuração do logging
logger = logging.getLogger(__name__)

# Namespace para documentação Swagger
ns = Namespace('matriculas', description='Operações relacionadas a matrículas')

# Modelo para documentação Swagger
matricula_model = ns.model('Matricula', {
    'nome': fields.String(required=True, description='Nome completo do estudante'),
    'email': fields.String(required=True, description='Email do estudante'),
    'curso': fields.String(required=True, description='Nome do curso')
})

matricula_response_model = ns.model('MatriculaResponse', {
    'id': fields.Integer(description='ID da matrícula'),
    'nome': fields.String(description='Nome completo do estudante'),
    'email': fields.String(description='Email do estudante'),
    'curso': fields.String(description='Nome do curso'),
    'data_matricula': fields.String(description='Data da matrícula'),
    'message': fields.String(description='Mensagem de confirmação')
})

@ns.route('')
class MatriculaResource(Resource):
    @ns.expect(matricula_model)
    @ns.marshal_with(matricula_response_model, code=201)
    @ns.doc('criar_matricula')
    def post(self):
        """Criar uma nova matrícula"""
        try:
            # Tentar obter dados JSON com diferentes abordagens
            data = None
            
            try:
                data = request.get_json(force=True)
            except Exception as json_error:
                logger.error(f"Erro ao fazer parse do JSON: {str(json_error)}")
                try:
                    # Tentar decodificar manualmente
                    raw_data = request.get_data(as_text=True)
                    data = json.loads(raw_data)
                except Exception as manual_error:
                    logger.error(f"Erro no parse manual: {str(manual_error)}")
                    return {'error': 'Dados JSON inválidos'}, 400
            
            # Validação básica
            if not data:
                return {'error': 'Dados não fornecidos'}, 400
                
            nome = data.get('nome', '').strip()
            email = data.get('email', '').strip()
            curso = data.get('curso', '').strip()
            
            if not all([nome, email, curso]):
                return {'error': 'Nome, email e curso são obrigatórios'}, 400
            
            # Verificar se já existe matrícula com mesmo email
            matricula_existente = Matricula.query.filter_by(email=email).first()
            if matricula_existente:
                return {'error': 'Já existe uma matrícula cadastrada com este email'}, 409
            
            # Criar nova matrícula
            nova_matricula = Matricula(nome=nome, email=email, curso=curso)
            db.session.add(nova_matricula)
            db.session.commit()
            
            logger.info(f"Nova matrícula criada: {nome} - {email} - {curso}")
            
            response_data = nova_matricula.to_dict()
            response_data['message'] = 'Matrícula realizada com sucesso!'
            
            return response_data, 201
            
        except Exception as e:
            logger.error(f"Erro ao criar matrícula: {str(e)}")
            db.session.rollback()
            return {'error': 'Erro interno do servidor'}, 500
    
    @ns.marshal_list_with(matricula_response_model)
    @ns.doc('listar_matriculas')
    def get(self):
        """Listar todas as matrículas"""
        try:
            matriculas = Matricula.query.all()
            return [matricula.to_dict() for matricula in matriculas], 200
        except Exception as e:
            logger.error(f"Erro ao listar matrículas: {str(e)}")
            return {'error': 'Erro interno do servidor'}, 500

@ns.route('/<int:matricula_id>')
class MatriculaByIdResource(Resource):
    @ns.marshal_with(matricula_response_model)
    @ns.doc('obter_matricula')
    def get(self, matricula_id):
        """Obter matrícula por ID"""
        try:
            matricula = Matricula.query.get(matricula_id)
            if not matricula:
                return {'error': 'Matrícula não encontrada'}, 404
            return matricula.to_dict(), 200
        except Exception as e:
            logger.error(f"Erro ao obter matrícula: {str(e)}")
            return {'error': 'Erro interno do servidor'}, 500 