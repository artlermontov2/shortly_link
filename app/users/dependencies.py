import os
from datetime import datetime
from fastapi import Depends, Request, Response
from dotenv import load_dotenv
from jose import jwt, JWTError


load_dotenv()


def get_token(responce: Response):
    pass