from flask import Flask, request, jsonify
from sqlalchemy.orm import joinedload

from app2 import sql_service
from models_sql import db, Cliente, Venda
from sql_service import criar_cliente, listar_clientes, obter_cliente, atualizar_cliente, deletar_cliente, criar_produto, listar_produtos, atualizar_produto, deletar_produto,criar_venda, listar_vendas
from nosql_service import registrar_dashboard_total, obter_dashboard_total
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)

# Configurações SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)

# Criar tabelas no primeiro run
with app.app_context():
    db.create_all()

@app.route("/clientes", methods=["POST"])
def criar_cliente_route():
    data = request.json
    if not all(k in data for k in ("nome", "email", "cpf", "data_nascimento")):
        return jsonify({"erro": "Campos obrigatórios: nome, email, cpf, data_nascimento"}), 400

    cliente = criar_cliente(
        nome=data["nome"],
        email=data["email"],
        cpf=data["cpf"],
        data_nascimento=data["data_nascimento"]
    )

    total_clientes = len(listar_clientes())
    registrar_dashboard_total(total_clientes)

    return jsonify({"id": cliente.id, "mensagem": "Cliente criado com sucesso"}), 201

@app.route("/clientes", methods=["GET"])
def listar_clientes_route():
    clientes = listar_clientes()
    return jsonify([
        {
            "id": c.id,
            "nome": c.nome,
            "email": c.email,
            "cpf": c.cpf,
            "data_nascimento": c.data_nascimento.strftime("%Y-%m-%d")
        } for c in clientes
    ])

@app.route("/clientes/<int:cliente_id>", methods=["GET"])
def obter_cliente_route(cliente_id):
    cliente = obter_cliente(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404
    return jsonify({
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "cpf": cliente.cpf,
        "data_nascimento": cliente.data_nascimento.strftime("%Y-%m-%d")
    })

@app.route("/clientes/<int:cliente_id>", methods=["PUT"])
def atualizar_cliente_route(cliente_id):
    data = request.json
    cliente = atualizar_cliente(
        cliente_id,
        nome=data.get("nome"),
        email=data.get("email"),
        cpf=data.get("cpf"),
        data_nascimento=data.get("data_nascimento")
    )
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    total_clientes = len(listar_clientes())
    registrar_dashboard_total(total_clientes)

    return jsonify({"mensagem": "Cliente atualizado com sucesso"})

@app.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def deletar_cliente_route(cliente_id):
    cliente = deletar_cliente(cliente_id)
    if not cliente:
        return jsonify({"erro": "Cliente não encontrado"}), 404

    total_clientes = len(listar_clientes())
    registrar_dashboard_total(total_clientes)

    return jsonify({"mensagem": "Cliente deletado com sucesso"})

# Produtos

@app.route("/produtos", methods=["GET"])
def get_produtos():
    produtos = sql_service.listar_produtos()
    return jsonify([{"id": p.id, "nome": p.nome, "preco": p.preco, "estoque": p.estoque} for p in produtos])

@app.route("/produtos", methods=["POST"])
def post_produto():
    data = request.json
    produto = sql_service.criar_produto(data["nome"], data["preco"], data["estoque"])
    return jsonify({"id": produto.id}), 201


#  VENDAS -----------------

@app.route("/vendas", methods=["GET"])
def listar_vendas_route():
    vendas = Venda.query.options(
        joinedload(Venda.cliente),
        joinedload(Venda.produto)
    ).all()

    result = []
    for v in vendas:
        result.append({
            "id": v.id,
            "quantidade": v.quantidade,
            "data_venda": v.data_venda.isoformat(),
            "cliente": v.cliente.nome if v.cliente else None,
            "produto": v.produto.nome if v.produto else None,
        })

    return jsonify(result)

@app.route("/vendas", methods=["POST"])
def post_venda():
    data = request.json
    venda = sql_service.criar_venda(data["cliente_id"], data["produto_id"], data["quantidade"])
    if not venda:
        return jsonify({"erro": "Produto inexistente ou estoque insuficiente"}), 400
    return jsonify({"id": venda.id}), 201

# MongoDB - Relatórios

@app.route("/dashboard/total_clientes", methods=["GET"])
def dashboard_total_clientes():
    total = obter_total_clientes()
    return jsonify({"total_clientes": total})

@app.route("/dashboard/total_vendas", methods=["GET"])
def dashboard_total_vendas():
    total = obter_total_vendas()
    return jsonify({"total_vendas": total})

@app.route("/dashboard/faturamento", methods=["GET"])
def dashboard_faturamento():
    total = obter_faturamento_total()
    return jsonify({"faturamento_total": total})

@app.route("/dashboard/total_clientes", methods=["GET"])
def dashboard_total():
    total = obter_dashboard_total()
    return jsonify({"total_clientes": total})

if __name__ == "__main__":
    app.run(debug=True)
