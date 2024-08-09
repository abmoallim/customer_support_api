from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    user_type_id = Column(Integer, ForeignKey("usertype.id"))

    user_type = relationship("UserType", back_populates="users")
    companies = relationship("Company", back_populates="owner")
