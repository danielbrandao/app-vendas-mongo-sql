from config import SessionLocal
from models_sql import Cliente, Produto, Venda, ItemVenda
from datetime import datetime

# CLIENTE
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

def obter_cliente(cliente_id):
    session = SessionLocal()
    cliente = session.query(Cliente).get(cliente_id)
    session.close()
    return cliente.to_dict() if cliente else None

def atualizar_cliente(cliente_id, nome, email):
    session = SessionLocal()
    cliente = session.query(Cliente).get(cliente_id)
    if not cliente:
        session.close()
        return None
    cliente.nome = nome
    cliente.email = email
    session.commit()
    session.refresh(cliente)
    session.close()
    return cliente.to_dict()

def deletar_cliente(cliente_id):
    session = SessionLocal()
    cliente = session.query(Cliente).get(cliente_id)
    if not cliente:
        session.close()
        return None
    session.delete(cliente)
    session.commit()
    session.close()
    return {"message": f"Cliente {cliente_id} deletado"}

# PRODUTO
def criar_produto(nome, preco):
    session = SessionLocal()
    produto = Produto(nome=nome, preco=preco)
    session.add(produto)
    session.commit()
    session.refresh(produto)
    session.close()
    return produto.to_dict()

def listar_produtos():
    session = SessionLocal()
    produtos = session.query(Produto).all()
    resultado = [p.to_dict() for p in produtos]
    session.close()
    return resultado

def obter_produto(produto_id):
    session = SessionLocal()
    produto = session.query(Produto).get(produto_id)
    session.close()
    return produto.to_dict() if produto else None

def atualizar_produto(produto_id, nome, preco):
    session = SessionLocal()
    produto = session.query(Produto).get(produto_id)
    if not produto:
        session.close()
        return None
    produto.nome = nome
    produto.preco = preco
    session.commit()
    session.refresh(produto)
    session.close()
    return produto.to_dict()

def deletar_produto(produto_id):
    session = SessionLocal()
    produto = session.query(Produto).get(produto_id)
    if not produto:
        session.close()
        return None
    session.delete(produto)
    session.commit()
    session.close()
    return {"message": f"Produto {produto_id} deletado"}

# VENDA
def criar_venda(cliente_id, itens):
    """
    itens: lista de dicts {produto_id, quantidade}
    """
    session = SessionLocal()
    venda = Venda(cliente_id=cliente_id, data=datetime.utcnow())
    session.add(venda)
    session.commit()
    session.refresh(venda)

    for item in itens:
        iv = ItemVenda(
            venda_id=venda.id,
            produto_id=item["produto_id"],
            quantidade=item["quantidade"]
        )
        session.add(iv)

    session.commit()
    # Atualiza para incluir itens no objeto venda
    session.refresh(venda)

    # Carregar itens para retorno
    venda.itens  # garante carregamento lazy

    resultado = venda.to_dict()
    session.close()
    return resultado
