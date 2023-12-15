from piza_api.database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "user"
    id= Column(Integer,primary_key=True)
    username=Column(String(24),unique=True)
    email=Column(String(84),unique=True)
    password=Column(Text,nullable=True)
    is_staff=Column(Boolean,default=False)
    is_active=Column(Boolean,default=False)
    orders = relationship('Order', back_populates='user')
    


    def __repr__(self):
        return f"user {self.username}"

class Order(Base):
    ORDER_STATUSES=(
        ('PENDING','pending'),
        ('IN-TRANSIST','in_transist'),
        ('DELIVERED','delivered')
    )
    PIZZA_SIZES=(
        ("SMALL",'small'),
        ("MEDIUM",'medium'),
        ("LARGE",'large'),
        ("EXTRA-LARGE",'extra-large')
    )


    __tablename__ = "orders"
    id= Column(Integer,primary_key=True)
    quantity=Column(Integer,nullable=True)
    order_status=Column(ChoiceType(choices=ORDER_STATUSES),default="PENDING")
    piza_size=Column(ChoiceType(choices=PIZZA_SIZES),default='SMALL')
    user_id=Column(Integer,ForeignKey('user.id'))
    user = relationship('User', back_populates='orders')
    


    def __repr__(self):
        return f"order {self.id}"



