from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routes import farm
from .routes import crops
from .routes import animals
from .routes import milk
from .routes import workers
from .routes import shop
from backend.routes import ai_assistant
from backend.routes import weather
from .routes import transactions


Base.metadata.create_all(bind=engine)
from sqlalchemy import inspect, text

inspector = inspect(engine)

if "sales" in inspector.get_table_names():
    columns = [
        column["name"]
        for column in inspector.get_columns("sales")
    ]

    with engine.begin() as connection:
        if "amount_paid" not in columns:
            connection.execute(
                text("ALTER TABLE sales ADD COLUMN amount_paid FLOAT DEFAULT 0")
            )

        if "remaining_balance" not in columns:
            connection.execute(
                text("ALTER TABLE sales ADD COLUMN remaining_balance FLOAT DEFAULT 0")
            )

app = FastAPI(title="KrishiMitra AI")

app.include_router(farm.router)
app.include_router(crops.router)
app.include_router(animals.router)
app.include_router(milk.router)
app.include_router(workers.router)
app.include_router(shop.router)
app.include_router(ai_assistant.router)
app.include_router(weather.router)
app.include_router(transactions.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to KrishiMitra AI 🌾"
    }