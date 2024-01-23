from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)


class Bill(Base):
    __tablename__ = "Bill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    money = Column(Float, nullable=False)
    user = relationship("User", back_populates="bills")


User.bills = relationship(
    "Bill",
    order_by=Bill.id,
    back_populates="user",
)
User.predictions = relationship(
    "PredictRow",
    order_by=User.id,
    back_populates="user",
)
