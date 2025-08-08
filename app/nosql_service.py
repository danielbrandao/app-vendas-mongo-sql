from config import mongo_consolidados

def salvar_consolidado(dados):
    """
    Salva ou atualiza um consolidado no MongoDB.
    O parâmetro `dados` é um dict com, por exemplo:
    {
        "mes": "2025-08",
        "top_produtos": [
            {"produto_id": 1, "nome": "Notebook", "quantidade": 10, "total_vendas": 35000.0},
            ...
        ],
        "faturamento_total": 123456.78
    }
    """
    mongo_consolidados.update_one(
        {"mes": dados["mes"]},
        {"$set": dados},
        upsert=True
    )

def buscar_consolidado(mes):
    """
    Busca o consolidado do mês no formato 'YYYY-MM'.
    Retorna um dict com os dados ou None se não existir.
    """
    doc = mongo_consolidados.find_one({"mes": mes}, {"_id": 0})
    return doc
