from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class UsersModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    creared_at = Column(Date, nullable=False)
