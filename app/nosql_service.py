"""Funções de CRUD para MongoDB."""
from config import mongo_consolidados

def salvar_consolidado(dados):
    """Salva ou atualiza consolidado no MongoDB."""
    mongo_consolidados.update_one(
        {"mes": dados["mes"]},
        {"$set": dados},
        upsert=True
    )

def buscar_consolidado(mes):
    """Busca consolidado pelo mês (formato YYYY-MM)."""
    return mongo_consolidados.find_one({"mes": mes}, {"_id": 0})
