# abaixo temos o arquivo database.py que configura a conexão com o banco de dados
# e cria a sessão utilizada pelo SQLAlchemy para interagir com o banco.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'postgresql://challenge:challenge_2024@localhost:5432/challenge_db'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()