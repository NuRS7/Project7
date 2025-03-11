from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..routes.auth import get_current_user
from ..database import get_db
from ..CartModel import Flower, CartItem, Purchase

router=APIRouter()


# Добавить цветок в корзину
@router.post("/cart/items")
async def add_to_cart(
        flower_id: int = Form(...),
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    flower=db.query(Flower).filter(Flower.id == flower_id).first()
    if not flower:
        raise HTTPException(status_code=404, detail="Flower not found")

    # Проверяем, есть ли уже этот товар в корзине
    existing_cart_item=db.query(CartItem).filter(
        CartItem.user_email == user["email"],
        CartItem.flower_id == flower_id
    ).first()

    if existing_cart_item:
        raise HTTPException(status_code=400, detail="Flower is already in the cart")

    cart_item=CartItem(user_email=user["email"], flower_id=flower_id)
    db.add(cart_item)
    db.commit()
    return {"message": "Flower added to cart successfully"}


# Получить товары в корзине
@router.get("/cart/items")
async def get_cart_items(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items=db.query(CartItem).filter(CartItem.user_email == user["email"]).all()

    if not cart_items:
        return {"cart": [], "total_price": 0}

    flower_ids=[item.flower_id for item in cart_items]
    flowers=db.query(Flower).filter(Flower.id.in_(flower_ids)).all()
    total_price=sum(flower.price for flower in flowers)

    return {"cart": flowers, "total_price": total_price}


# Оформить покупку
@router.post("/purchased")
async def purchase_items(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items=db.query(CartItem).filter(CartItem.user_email == user["email"]).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    try:
        for item in cart_items:
            purchase=Purchase(user_email=user["email"], flower_id=item.flower_id)
            db.add(purchase)
            db.delete(item)  # Удаляем товар из корзины

        db.commit()
        return {"message": "Flowers purchased successfully"}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")


# Получить купленные товары
@router.get("/purchased")
async def get_purchased_items(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    purchased_items=db.query(Purchase).filter(Purchase.user_email == user["email"]).all()

    if not purchased_items:
        return {"purchased": []}

    flower_ids=[item.flower_id for item in purchased_items]
    flowers=db.query(Flower).filter(Flower.id.in_(flower_ids)).all()

    return {"purchased": flowers}
