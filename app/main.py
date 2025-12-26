from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import auth_routes, data_routes
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Data Cleaning Assistant")
app.mount("/cleaned", StaticFiles(directory="cleaned"), name="cleaned")

app.include_router(auth_routes.router)
app.include_router(data_routes.router)
