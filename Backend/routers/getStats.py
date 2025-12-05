# Abaixo temos o router do endpoint que será utilizado para calcular os status da página inicial
# do dashboard. Nele retornamos o total obtido até agora desde o início do bd, o ganho de
# vendas no total e o número de clientes cadastrados até o momento.

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Sale, Customer

router = APIRouter()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), month: int = None):
    # verificamos se recebemos algum input do front para filtrar por mês
    # caso não, retornamos os totais gerais
    if not month:
        total_revenue = db.query(func.sum(Sale.total_amount)).scalar() or 0
        total_sales = db.query(func.count(Sale.id)).scalar() 
        total_customers = db.query(func.count(Customer.id)).scalar() 
        customers_with_sales = db.query(func.count(func.distinct(Sale.customer_id))).scalar() if total_customers else 0
        conversion_rate = (customers_with_sales / total_customers * 100) if total_customers else 0
    else:
        # caso tenhamos um mês, filtramos os dados para retornar apenas os
        # totais daquele mês específico
        total_revenue = (
            db.query(func.sum(Sale.total_amount))
            .filter(func.extract('month', Sale.created_at) == month)
            .scalar() or 0
        )

        total_sales = (
            db.query(func.count(Sale.id))
            .filter(func.extract('month', Sale.created_at) == month)
            .scalar()
        )

        total_customers = db.query(func.count(Customer.id)).scalar()

    return {
        "total_revenue": float(total_revenue),
        "total_sales": total_sales,
        "total_customers": total_customers,
    }
