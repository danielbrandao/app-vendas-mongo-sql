from config import SessionLocal
from models_sql import Cliente

def criar_cliente(nome, email):
    session = SessionLocal()
    cliente = Cliente(nome=nome, email=email)
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    session.close()
    return cliente.to_dict()

def listar_clientes():
    session = SessionLocal()
    clientes = session.query(Cliente).all()
    resultado = [c.to_dict() for c in clientes]
    session.close()
    return resultado

def contar_clientes():
    session = SessionLocal()
    total = session.query(Cliente).count()
    session.close()
    return total
