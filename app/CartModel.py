from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database  import Base

# Модель Цветов
class Flower(Base):
    __tablename__ = "flowers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    image_url = Column(String)

# Модель Корзины
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    flower_id = Column(Integer, ForeignKey("flowers.id"))

# Модель Покупок
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    flower_id = Column(Integer, ForeignKey("flowers.id"))
