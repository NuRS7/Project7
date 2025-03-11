from fastapi import APIRouter, Form, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import shutil
import os
from ..database import get_db
from ..CartModel import Flower
from ..database import Base, engine

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Папка для загрузки фото
UPLOAD_DIR = "static/flowers/"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создаем папку, если ее нет

# Страница с цветами и формой добавления
@router.get("/flowers")
async def flowers_page(request: Request, db: Session = Depends(get_db)):
    flowers = db.query(Flower).all()
    return templates.TemplateResponse("flowers.html", {"request": request, "flowers": flowers})

# Добавление цветка в базу с загрузкой фото
@router.post("/flowers")
async def add_flower(
    name: str = Form(...),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Создаем путь для файла
    file_path = f"{UPLOAD_DIR}{image.filename}"

    # Сохраняем файл в папку
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Сохраняем в БД
    flower = Flower(name=name, price=price, image_url=file_path)
    db.add(flower)
    db.commit()
    return {"message": "Flower added successfully", "image_url": file_path}

# Создание таблицы (если не существует)
Base.metadata.create_all(bind=engine)
