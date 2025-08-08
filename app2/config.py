# Configurações de banco

# SQLite para testes locais
#SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Versão MySQL:
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost:3306/banco_teste"

# Config MongoDB
MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "testing"
MONGO_COLLECTION_DASHBOARD = "client"
