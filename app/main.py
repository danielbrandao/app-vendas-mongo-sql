from flask import Flask, request, jsonify
from sql_service import (
    criar_cliente, listar_clientes, obter_cliente, atualizar_cliente, deletar_cliente,
    criar_produto, listar_produtos, obter_produto, atualizar_produto, deletar_produto,
    criar_venda
)
from nosql_service import salvar_consolidado, buscar_consolidado
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return

# ---------------- CRUD CLIENTE ----------------
@app.route("/clientes", methods=["GET"])
def get_clientes():
    return jsonify(listar_clientes())

@app.route("/clientes", methods=["POST"])
def post_cliente():
    data = request.get_json()
    novo = criar_cliente(data["nome"], data["email"])
    return jsonify(novo), 201

@app.route("/clientes/<int:cliente_id>", methods=["GET"])
def get_cliente(cliente_id):
    return jsonify(obter_cliente(cliente_id))

@app.route("/clientes/<int:cliente_id>", methods=["PUT"])
def put_cliente(cliente_id):
    data = request.get_json()
    return jsonify(atualizar_cliente(cliente_id, data["nome"], data["email"]))

@app.route("/clientes/<int:cliente_id>", methods=["DELETE"])
def delete_cliente(cliente_id):
    return jsonify(deletar_cliente(cliente_id))


# ---------------- CRUD PRODUTO ----------------
@app.route("/produtos", methods=["GET"])
def get_produtos():
    return jsonify(listar_produtos())

@app.route("/produtos", methods=["POST"])
def post_produto():
    data = request.get_json()
    novo = criar_produto(data["nome"], data["preco"])
    return jsonify(novo), 201

@app.route("/produtos/<int:produto_id>", methods=["GET"])
def get_produto(produto_id):
    return jsonify(obter_produto(produto_id))

@app.route("/produtos/<int:produto_id>", methods=["PUT"])
def put_produto(produto_id):
    data = request.get_json()
    return jsonify(atualizar_produto(produto_id, data["nome"], data["preco"]))

@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def delete_produto(produto_id):
    return jsonify(deletar_produto(produto_id))


# ---------------- CRIAR VENDA ----------------
@app.route("/vendas", methods=["POST"])
def post_venda():
    data = request.get_json()
    venda = criar_venda(data["cliente_id"], data["itens"])
    return jsonify(venda), 201


# ---------------- CONSOLIDAR NO MONGODB ----------------
@app.route("/consolidar/<int:ano>/<int:mes>", methods=["POST"])
def consolidar(ano, mes):
    resumo = salvar_consolidado(ano, mes)
    return jsonify(resumo)


# ---------------- CONSULTAR CONSOLIDADO ----------------
@app.route("/dashboard/<string:periodo>", methods=["GET"])
def dashboard(periodo):
    return jsonify(buscar_consolidado(periodo))


if __name__ == "__main__":
    app.run(debug=True)
