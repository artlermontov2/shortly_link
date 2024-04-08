import time
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
import sentry_sdk
from fastapi_versioning import VersionedFastAPI

from app.admin.auth import authentication_backend
from app.admin.view import ShortenAdmin, UserAdmin
from app.database import engine
from app.pages.router import router as pages_router
from app.reduction.router import router as reduction_router
from app.users.router import router as users_router
from app.logger import logger

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv('DSN'),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

app = FastAPI(
    title="Сокращение ссылок",
    version="0.1.0",
    root_path="/api",
)

app.include_router(users_router)
app.include_router(reduction_router)
app.include_router(pages_router)

# Подключение CORS, чтобы запросы к API могли приходить из браузера 
origins = [
    "http://localhost:3000", "http://127.0.0.1:8000", "http://localhost:6379"
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

# Подключение версионирования
# Добавление версии к endpoint при помщи декоратора @version(int)
app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/api/v{major}',
)

if os.getenv('MODE') == "TEST":
    # При тестировании через pytest, необходимо подключать Redis, чтобы кэширование работало.
    # Иначе декоратор @cache из библиотеки fastapi-cache ломает выполнение кэшируемых эндпоинтов.
    # Из этого следует вывод, что сторонние решения порой ломают наш код, и это бывает проблематично поправить.
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

# Redis
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

# SQLAlchemy Admin
admin = Admin(
    app, engine, authentication_backend=authentication_backend, base_url="/pages/admin", debug=True
)
admin.add_view(UserAdmin)
admin.add_view(ShortenAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    response.headers["X-Process-Time"] = str(process_time)
    return response



