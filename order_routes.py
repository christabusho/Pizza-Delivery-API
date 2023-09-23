from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select
from models import OrderStatus, OrderSize, User, Order, Toppings
from schemas import OrderModel, OrderStatusModel, OrderPlacementModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

order_router=APIRouter(
    prefix='/orders',
    tags=['orders']
)

session=Session(bind=engine)


@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    """
        ## A sample hello world route 
        This returns Hello world
    """
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    return {"message":"Hello World"}

@order_router.post('/order',status_code=status.HTTP_201_CREATED)
async def place_an_order(quantity:int,t:Toppings,size:OrderSize, Authorize:AuthJWT=Depends()):

    """
        ## Place an Order
        This requires the following:
        - the quantity: integer
        - the pizza size: str
        - the toppings: str
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    current_user=Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        pizza_size=size,
        quantity=quantity,
        toppings=t
    )

    new_order.user=user

    session.add(new_order)

    session.commit()

    response={
        "pizza_size":new_order.pizza_size,
        "toppings":new_order.toppings,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)
    


@order_router.get('/orders')
async def list_all_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()
    # orders=db.query(Order).all()
    # print("**************", orders )
    # return orders



    if user.is_staff:
        orders=session.query(Order).all()

        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not a super user"
    )


@order_router.get('/orders/{id}')
async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    user=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to carry out the request"
    )

@order_router.get('/user/orders')
async def get_current_user_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    user = Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==user).first()

    return jsonable_encoder(current_user.orders)


@order_router.get('/user/order/{id}/')
async def get_specific_order_of_user(id:int, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    subject = Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==subject).first()

    orders=current_user.orders

    for o in orders:
        if o.id == id:
            return jsonable_encoder(o)
        
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No order with such Id"
    )

@order_router.put('/order/update/{id}/')
async def update_order(id:int,quantity:int,t:Toppings,order:OrderSize,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    order_to_update=session.query(Order).filter(Order.id==id).first()

    order_to_update.quantity=quantity
    order_to_update.pizza_size=order
    order_to_update.toppings=t

    session.commit()

    response={
            "quantity":order_to_update.quantity,
            "pizza_size":order_to_update.pizza_size,
            "toppings":order_to_update.toppings,
            "order_status":order_to_update.order_status
            
        }

    return jsonable_encoder(response)


@order_router.patch('/order/update/{id}/')
async def update_order_status(id:int,
                              order_status:OrderStatus,
                              Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    username=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()

        order_to_update.order_status=order_status

        session.commit()

        response={
            "quantity":order_to_update.quantity,
            "pizza_size":order_to_update.pizza_size,
            "toppings":order_to_update.toppings,
            "order_status":order_to_update.order_status
        }

        return jsonable_encoder(response)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not allowed to carry out the request"
    )


@order_router.delete('/order/delete/{id}/',
                     status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    
    order_to_delete=session.query(Order).filter(Order.id==id).first()

    session.delete(order_to_delete)

    session.commit()

    return order_to_delete