from app.config import SessionLocal
from models_sql import db, Cliente, Produto, Venda
from datetime import datetime

def criar_cliente(nome, email, cpf, data_nascimento):
    cliente = Cliente(
        nome=nome,
        email=email,
        cpf=cpf,
        data_nascimento=datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    )
    db.session.add(cliente)
    db.session.commit()
    return cliente

def listar_clientes():
    return Cliente.query.all()

def obter_cliente(cliente_id):
    return Cliente.query.get(cliente_id)

def atualizar_cliente(cliente_id, nome=None, email=None, cpf=None, data_nascimento=None):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return None
    if nome:
        cliente.nome = nome
    if email:
        cliente.email = email
    if cpf:
        cliente.cpf = cpf
    if data_nascimento:
        cliente.data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
    db.session.commit()
    return cliente

def deletar_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return None
    db.session.delete(cliente)
    db.session.commit()
    return cliente

# ----------------- PRODUTOS -----------------
def criar_produto(nome, preco, estoque):
    produto = Produto(nome=nome, preco=preco, estoque=estoque)
    db.session.add(produto)
    db.session.commit()
    return produto

def listar_produtos():
    return Produto.query.all()

def atualizar_produto(id, nome=None, preco=None, estoque=None):
    produto = Produto.query.get(id)
    if produto:
        if nome:
            produto.nome = nome
        if preco:
            produto.preco = preco
        if estoque is not None:
            produto.estoque = estoque
        db.session.commit()
    return produto

def deletar_produto(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
    return produto

# ----------------- VENDAS -----------------
def criar_venda(cliente_id, produto_id, quantidade):
    produto = Produto.query.get(produto_id)
    if not produto or produto.estoque < quantidade:
        return None  # estoque insuficiente ou produto inexistente

    venda = Venda(cliente_id=cliente_id, produto_id=produto_id, quantidade=quantidade)
    produto.estoque -= quantidade  # baixa no estoque
    db.session.add(venda)
    db.session.commit()
    return venda

def listar_vendas():
    return Venda.query.all()