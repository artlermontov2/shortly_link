from pydantic import BaseModel


class UrlItem(BaseModel):
    long_url: str