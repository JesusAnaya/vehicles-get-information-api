from fastapi import FastAPI
from api.routers import router
from db.base import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router, prefix="/api/v1")
