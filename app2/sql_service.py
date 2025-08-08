from models_sql import db, Cliente
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
