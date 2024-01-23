from fastapi import HTTPException, status


UserAlredyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь уже существует",
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не верная почта или пароль",
    headers={"WWW-Authenticate": "Bearer"}
)

TokenExpiredExeption = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен истёк",
    headers={"WWW-Authenticate": "Bearer"},
)

TokenAbsentExeption = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Токен отсутсвует",
    headers={"WWW-Authenticate": "Bearer"},
)

IncorrectTokenFormatExeption = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Неверный формат токена",
    headers={"WWW-Authenticate": "Bearer"}
)

UserIsNotPresentExeption = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователя не существует",
    headers={"WWW-Authenticate": "Bearer"}
)