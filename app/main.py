from fastapi import FastAPI
from app.reduction.router import router as reduction_router
from app.users.router import router as users


app = FastAPI()

app.include_router(reduction_router)
app.include_router(users)