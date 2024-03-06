from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.users.models import UsersModel
from app.database import Base


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