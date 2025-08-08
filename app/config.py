"""Configurações de banco de dados SQL e MongoDB."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

# Configuração SQL (exemplo com SQLite para testes)
DATABASE_URL = "sqlite:///meubanco.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

# Configuração MongoDB
MONGO_URL = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["analytics_db"]
mongo_consolidados = mongo_db["consolidados"]
