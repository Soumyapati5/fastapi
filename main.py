from fastapi import FastAPI
from database import model
from routes import item_routes, clockin_routes

app = FastAPI()

app.include_router(item_routes.router, prefix="/items", tags=["Items"])
app.include_router(clockin_routes.router, prefix="/clockins", tags=["Clock-ins"])

@app.get("/")
async def home():
    return {'message': "Welcome Home!"}