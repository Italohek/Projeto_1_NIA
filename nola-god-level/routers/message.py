# implementacão da mensagem pro db utilizando o gpt 4o

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Customer, Sale

router = APIRouter()

@router.post("/message")
def message(db: Session = Depends(get_db), limit: int = 10):
    # pegamos os ultimos clientes cadastrados
    customers_query = db.query(
        Customer.id,
        Customer.customer_name.label("description"),
        Customer.created_at
    ).order_by(Customer.created_at.desc()).limit(limit)
    
    customers_activity = [
        {
            "type": "customer",
            "id": c.id,
            "desc": f"Novo cliente: {c.description}",
            "time": c.created_at.strftime("%H:%M"),
            "created_at": c.created_at
        }
        for c in customers_query.all()
    ]

    # e as ultimas vendas realizadas
    sales_query = db.query(
        Sale.id,
        Sale.total_amount.label("amount"),
        Sale.created_at
    ).order_by(Sale.created_at.desc()).limit(limit)

    sales_activity = [
        {
            "type": "sale",
            "id": s.id,
            "desc": f"Venda de R$ {s.amount:.2f} realizada",
            "time": s.created_at.strftime("%H:%M"),
            "created_at": s.created_at
        }
        for s in sales_query.all()
    ]

    # ordena os resultados combinados por data/hora de criação
    # utilizando uma função lambda para a chave de ordenação
    combined = customers_activity + sales_activity
    combined_sorted = sorted(combined, key=lambda x: x["created_at"], reverse=True)

    # retorna as ultimas contas/vendas criadas até o limite definido
    return combined_sorted[:limit]
