from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import overviewSection, getStats, weekdayAnalysis, message
import models


def create_app():
    app = FastAPI(title="Nola Challenge API")

    # configuração do CORS para permitir requisições do front-end
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

    # inclui os routers dos endpoints na aplicação FastAPI
    app.include_router(overviewSection.router, prefix="/overviewSection", tags=["overviewSection"])
    app.include_router(getStats.router, prefix="/getStats", tags=["getStats"])
    app.include_router(weekdayAnalysis.router, prefix="/weekdayAnalysis", tags=["weekdayAnalysis"])
    app.include_router(message.router, prefix="/message", tags=["message"])

    # cria as tabelas no banco de dados, se ainda não existirem
    models.Base.metadata.create_all(bind=engine)
    return app

app = create_app()
