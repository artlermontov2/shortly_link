from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database import Base


class UsersModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)

    urls = relationship("ShortenModel", back_populates="user")

    def __str__(self) -> str:
        return self.email
