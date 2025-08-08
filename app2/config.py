from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

DATABASE_URL = "sqlite:///app2/banco_sql.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

MONGO_URL = "mongodb://localhost:27017"
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["app2_analytics"]
mongo_consolidados = mongo_db["dashboard"]
