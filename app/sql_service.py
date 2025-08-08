"""Funções de CRUD e consultas no banco SQL."""
from sqlalchemy import func
from config import SessionLocal
from models_sql import Venda, ItemVenda, Produto

def gerar_consolidado_mes(mes, ano):
    """Agrupa vendas no SQL e retorna um resumo mensal."""
    session = SessionLocal()
    resultados = (
        session.query(
            Produto.id,
            Produto.nome,
            func.sum(ItemVenda.quantidade).label("qtd"),
            func.sum(ItemVenda.quantidade * Produto.preco).label("total")
        )
        .join(ItemVenda.produto)
        .join(ItemVenda.venda)
        .filter(func.strftime("%m", Venda.data) == f"{mes:02d}")
        .filter(func.strftime("%Y", Venda.data) == str(ano))
        .group_by(Produto.id, Produto.nome)
        .all()
    )

    faturamento_total = sum(r.total for r in resultados)

    return {
        "mes": f"{ano}-{mes:02d}",
        "top_produtos": [
            {"produto_id": r.id, "nome": r.nome, "quantidade": int(r.qtd), "total_vendas": float(r.total)}
            for r in resultados
        ],
        "faturamento_total": faturamento_total
    }
