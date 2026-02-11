from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from schemas.order import OrderResponse, OrderStatusUpdate
from models.order import Order, OrderItem, OrderStatus
from models.cart import Cart, CartItem
from models.product import Product
from models.user import User, UserRole
from core.dependencies import get_current_user, require_admin

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Place an order from cart items"""
    # Get user's cart
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart or not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Begin transaction
    try:
        total_amount = 0.0
        order_items_data = []
        
        # Validate all items and calculate total
        for cart_item in cart.items:
            product = db.query(Product).filter(Product.id == cart_item.product_id).first()
            
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product {cart_item.product_id} not found"
                )
            
            # Check stock availability
            if product.stock < cart_item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for {product.name}. Only {product.stock} items available"
                )
            
            # Prevent negative inventory
            if product.stock - cart_item.quantity < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot order {cart_item.quantity} of {product.name}"
                )
            
            item_total = product.price * cart_item.quantity
            total_amount += item_total
            
            order_items_data.append({
                "product_id": product.id,
                "quantity": cart_item.quantity,
                "price": product.price  # Store current price
            })
        
        # Create order
        new_order = Order(
            user_id=current_user.id,
            total_amount=round(total_amount, 2),
            status=OrderStatus.PENDING
        )
        db.add(new_order)
        db.flush()  # Get order ID without committing
        
        # Create order items and deduct stock
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price=item_data["price"]
            )
            db.add(order_item)
            
            # Deduct stock
            product = db.query(Product).filter(Product.id == item_data["product_id"]).first()
            product.stock -= item_data["quantity"]
        
        # Clear cart after successful order
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        
        # Commit transaction
        db.commit()
        db.refresh(new_order)
        
        return new_order
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to place order: {str(e)}"
        )


@router.get("/", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's orders (customers see their own, admins see all)"""
    
    if current_user.role == UserRole.ADMIN:
        # Admin can see all orders
        orders = db.query(Order).order_by(Order.created_at.desc()).all()
    else:
        # Customer can only see their orders
        orders = db.query(Order).filter(
            Order.user_id == current_user.id
        ).order_by(Order.created_at.desc()).all()
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific order"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user has permission to view this order
    if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
    
    ):
    """Update order status (Admin only)"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    """Cancel an order (restore stock and track cancellations for fraud prevention)"""
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check permission
    if current_user.role != UserRole.ADMIN and order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this order"
        )
    
    # Only pending orders can be cancelled
    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be cancelled"
        )
    
    try:
        # Restore stock
        for order_item in order.items:
            product = db.query(Product).filter(Product.id == order_item.product_id).first()
            if product:
                product.stock += order_item.quantity
        
        # Update order status
        order.status = OrderStatus.CANCELLED
        
        # Track cancellations for fraud prevention
        user = db.query(User).filter(User.id == order.user_id).first()
        user.order_cancellation_count += 1
        
        # Fraud prevention: block users with excessive cancellations
        if user.order_cancellation_count > 3:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account suspended due to excessive order cancellations"
            )
        
        db.commit()
        
        return None
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel order: {str(e)}"
        )