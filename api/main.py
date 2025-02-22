from fastapi import FastAPI
from database import engine 
from routers import serpro
import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(serpro.router)




