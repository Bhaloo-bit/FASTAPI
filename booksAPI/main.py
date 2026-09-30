from fastapi import FastAPI
from database import create_tables
from routes import books , user

app = FastAPI(
    title="Kitab Exchange API",
    description='A simple API for exchanging used books',    version="1.0"
)

@app.on_event("startup")
def on_startup():
    create_tables()
    
app.include_router(books.router)
app.include_router(user.router)

@app.get("/")
def home():
    return {"message": "Welcome to the kitab Exchange used books"}