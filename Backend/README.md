# ⚙️ Backend — FastAPI (Catálogo de Restaurantes)

Este é o **backend** da aplicação de catálogo de restaurantes, desenvolvido com [FastAPI](https://fastapi.tiangolo.com/).  
Ele fornece uma API RESTful para o frontend, realizando operações como listagem, consulta e análise de dados de restaurantes e vendas.

---

## 🧰 Tecnologias Principais

| Categoria | Ferramenta |
|------------|-------------|
| Framework  | FastAPI |
| Banco de Dados | PostgreSQL |
| ORM | SQLAlchemy |
| Containerização | Docker & Docker Compose |
| Ambiente Virtual | venv (Python padrão) |

---

## 🧩 Estrutura do Projeto
```text
backend/
├── __pycache__/
├── routers/ # rotas
├── main.py # ponto de entrada FastAPI
├── database.py # conexão com o banco
├── generate_data.py
├── models.py # modelos do SQLAlchemy
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── database-schema.sql
└── README.md
```

---

## 🧱 Instalação Local
### 1️⃣ Crie e ative o ambiente do docker

```bash
1.1 Garanta que você tenha o docker instalado.

1.2 Execute na pasta do backend (aonde estão o docker compose e Dockerfile):
docker compose down -v 2>/dev/null || true
docker compose build --no-cache data-generator
docker compose up -d postgres
docker compose run --rm data-generator
docker compose --profile tools up -d pgadmin

1.3 Após isso teste para ver se o bd está correto
docker compose exec postgres psql -U challenge challenge_db -c 'SELECT COUNT(*) FROM sales;'

Isso deve mostrar ~500k

Caso tudo esteja certo, execute:
1.4 sudo docker compose up -d postgres
1.5 sudo docker compose up -d pgadmin
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
cd backend
python3 -m venv env
source env/bin/activate

2.1 Instale as dependências

pip install -r requirements.txt

2.2 Execute o servidor FastAPI

uvicorn app.main:app --reload

O backend ficará disponível em:
👉 http://127.0.0.1:8000

Documentação interativa:

Swagger UI → http://127.0.0.1:8000/docs
```
