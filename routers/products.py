from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from models.product import Product
from models.user import User
from core.dependencies import require_admin, get_current_user
from fastapi import UploadFile, File, Form
from PIL import Image
import secrets
import os

router = APIRouter()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new product with image (Admin only)"""

    # Check duplicate product
    existing_product = db.query(Product).filter(Product.name == name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )

    image_name = None

    if image:
        IMAGE_PATH = "./app/static/products/"
        os.makedirs(IMAGE_PATH, exist_ok=True)

        extension = image.filename.split(".")[-1].lower()
        if extension not in ["png", "jpg", "jpeg"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image format not supported"
            )

        image_name = secrets.token_hex(10) + "." + extension
        image_path = os.path.join(IMAGE_PATH, image_name)

        contents = image.file.read()
        with open(image_path, "wb") as f:
            f.write(contents)

        # Resize to 300x300 pixels
        img = Image.open(image_path)
        img = img.resize((300, 300)) 
        img.save(image_path)

    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image=image_name
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
    ):
    """Get all products (Public endpoint)"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a single product by ID (Public)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found"
        )
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
    ):
    """Update a product (Admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update only provided fields
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
    ):
    """Delete a product (Admin only)"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()


        raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="Product Deleted Successfully"
    )
        
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    

    
    return product


@router.patch("/{product_id}/stock", response_model=ProductResponse)
def update_product_stock(
    product_id: int,
    stock: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
    ):
    """Update product stock (Admin only)"""
    
    if stock < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input Stock must be a positive integer"
        )
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not  found"
        )
    
    product.stock = stock
    db.commit()
    db.refresh(product)
    
    return product