from fastapi import FastAPI
from app.reduction.router import router as reduction_router


app = FastAPI()

app.include_router(reduction_router)