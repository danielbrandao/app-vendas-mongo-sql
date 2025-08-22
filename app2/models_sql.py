from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)

    #vendas = db.relationship("Venda", backref="cliente")


class Produto(db.Model):
    __tablename__ = "produtos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)

    #vendas = db.relationship("Venda", backref="produto")

class Venda(db.Model):
    __tablename__ = "vendas"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produtos.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.DateTime, default=func.now())

    cliente = db.relationship("Cliente", back_populates="vendas")
    produto = db.relationship("Produto", back_populates="vendas")