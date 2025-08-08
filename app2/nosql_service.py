from config import mongo_consolidados

def salvar_total_clientes(total):
    mongo_consolidados.update_one(
        {"_id": "total_clientes"},
        {"$set": {"total": total}},
        upsert=True
    )

def buscar_total_clientes():
    doc = mongo_consolidados.find_one({"_id": "total_clientes"}, {"_id": 0})
    return doc
t