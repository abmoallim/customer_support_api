from sqlalchemy import Column, Integer, String
from app.db.session import Base

class UserType(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
