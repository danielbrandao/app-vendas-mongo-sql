from flask import Flask, request, jsonify
from models_sql import db, Cliente
from sql_service import criar_cliente, listar_clientes, obter_cliente, atualizar_cliente, deletar_cliente
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

@app.route("/dashboard/total_clientes", methods=["GET"])
def dashboard_total():
    total = obter_dashboard_total()
    return jsonify({"total_clientes": total})

if __name__ == "__main__":
    app.run(debug=True)
