from datetime import datetime, timedelta
from fastapi import APIRouter, Response, HTTPException, status



router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)