from app.database import db
from datetime import datetime

class Matricula(db.Model):
    __tablename__ = 'matriculas'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(100), nullable=False)
    data_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, nome, email, curso):
        self.nome = nome
        self.email = email
        self.curso = curso
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'curso': self.curso,
            'data_matricula': self.data_matricula.isoformat() if self.data_matricula else None
        } 