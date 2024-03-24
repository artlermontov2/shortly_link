from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.users.models import UsersModel  # Не удалять


class ShortenModel(Base):
    __tablename__ = "shorten_table"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey("user_table.id"))
    token = Column(String, nullable=False)
    long_url = Column(String, nullable=False)
    created_at = Column(Date, nullable=False)
    expiry_at = Column(Date, nullable=False)

    user = relationship("UsersModel", back_populates="urls")

    def __str__(self) -> str:
        return f"#{self.id}"
    
    