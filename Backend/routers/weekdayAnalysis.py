from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models

router = APIRouter()

@router.get("/weekdayAnalysis")
def get_weekday_analysis(db: Session = Depends(get_db)):
    # agrupa as vendas por dia da semana (domingo = 0 e sábado = 6) e horas do dia
    results = (
        db.query(
            func.extract('dow', models.Sale.created_at).label('weekday'), # dia da semana
            func.extract('hour', models.Sale.created_at).label('hour'),   # hora
            func.count(models.Sale.id).label('sales')                     # nº de vendas
        )
        .group_by('weekday', 'hour')
        .order_by('weekday', 'hour')
        .all()
    )

    # reorganiza em um dicionário no formato que o front espera
    data = {i: [] for i in range(7)}  # domingo (0) até sábado (6)

    for row in results:
        weekday = int(row.weekday)
        hour = f"{int(row.hour):02d}h"
        data[weekday].append({
            "hour": hour,
            "sales": int(row.sales)
        })

    return data
