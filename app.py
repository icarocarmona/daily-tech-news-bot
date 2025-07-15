from fastapi import FastAPI
from api.routers import router

app = FastAPI(title="Agente de Notícias")

app.include_router(router=router, prefix="/api")
