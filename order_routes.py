from fastapi import APIRouter,Depends,status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from piza_api.models import User,Order
from piza_api.schemas import OrderModel,OrderStatusModel
from piza_api.database import Session,engine
from fastapi.encoders import jsonable_encoder


order_router=APIRouter(
    prefix='/order',
    tags=['orders']
)
session=Session(bind=engine)
@order_router.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="invalid token")
    return {"hello":"order"}

@order_router.post('/order',status_code=status.HTTP_201_CREATED)
async def place_order(order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )
    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        piza_size=order.piza_size,
        quantity=order.quantity
    )
    new_order.user=user
    session.add(new_order)
    session.commit()

    response={
        "pizza_size":new_order.piza_size,
        "quantity":new_order.quantity,
        "id":new_order.id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)

@order_router.get('/orders')
def list_all_orders(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )
    current_user=Authorize.get_jwt_subject()

    user=session.query(User).filter(User.username==current_user).first()

    if user.is_staff:
        orders=session.query(Order).all()

        return jsonable_encoder(orders)
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ypu are not a super user"
        )

@order_router.get('/order/{id}')
async def get_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="provide valid token")
    user = Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you are not a admin")

@order_router.get('/user/orders')
async def get_user_order(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="provide valid token")
    user = Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()
    print(current_user.id)
    return jsonable_encoder(current_user.orders)

@order_router.get('/user/order/{id}')
async def get_specific_order(id:int,Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="provide valid token")
    user = Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    orders=current_user.orders
    for order in orders:
        if order.id==id:
            return jsonable_encoder(order)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="no order with that id")

@order_router.put('/order/update/{id}')
async def update_order(id:int,order:OrderModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="provide valid token")
    order_to_update = session.query(Order).filter(Order.id==id).first()
    order_to_update.quantity=order.quantity
    order_to_update.piza_size=order.piza_size
    print(order_to_update,'-->')
    session.commit()
    return jsonable_encoder({"quantiy":order_to_update.quantity,"size":order_to_update.piza_size})

@order_router.patch('/order/status/update/{id}')
async def update_order_status(id:int,order:OrderStatusModel,Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token"
        )
    username=Authorize.get_jwt_subject()

    current_user=session.query(User).filter(User.username==username).first()

    if current_user.is_staff:
        order_to_update=session.query(Order).filter(Order.id==id).first()

        order_to_update.order_status=order.order_status

        session.commit()

        return jsonable_encoder({"order":order_to_update.order_status})
        

