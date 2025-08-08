"""API Flask para gerar e consultar consolidados."""

from flask import Flask, jsonify
from sql_service import gerar_consolidado_mes
from nosql_service import salvar_consolidado, buscar_consolidado

app = Flask(__name__)

@app.route("/consolidar/<int:ano>/<int:mes>", methods=["POST"])
def consolidar(ano, mes):
    consolidado = gerar_consolidado_mes(mes, ano)
    salvar_consolidado(consolidado)
    return jsonify({"status": "Consolidado salvo no MongoDB", "dados": consolidado})

@app.route("/dashboard/<ano_mes>")
def dashboard(ano_mes):
    dados = buscar_consolidado(ano_mes)
    if dados:
        return jsonify(dados)
    return jsonify({"erro": "Consolidado não encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
