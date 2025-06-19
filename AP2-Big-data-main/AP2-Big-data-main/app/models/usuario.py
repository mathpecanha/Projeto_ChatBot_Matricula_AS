from app.database import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    dt_nascimento = db.Column(db.String(10))
    cpf = db.Column(db.String(11), unique=True)
    telefone = db.Column(db.String(20))

    enderecos = db.relationship("Endereco", back_populates="usuario", lazy=True)
    cartoes = db.relationship("Cartao", back_populates="usuario", lazy=True)
    pedidos = db.relationship("Pedido", back_populates="usuario", lazy=True)