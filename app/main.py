from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.reduction.router import router as reduction_router
from app.users.router import router as users_router
from app.pages.router import router as pages_router


app = FastAPI()

app.include_router(reduction_router)
app.include_router(users_router)
app.include_router(pages_router)

# Подключение CORS, чтобы запросы к API могли приходить из браузера 
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js 
    "http://localhost:3000", "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", 
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)