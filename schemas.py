from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode=True
        schema_etra={
            'example':{
                "username":"john wick",
                "email":"johnwick@gmail.com",
                "password":"password123",
                "is_staff":False,
                "is_active":True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key:str ='bdd36a089c94a4c1bf682cbd35b40590512c3e8d0a07d769be9dba0010d19cdd'

class LoginModel(BaseModel):
    username:str
    password:str


class OrderModel(BaseModel):
    id : Optional[int]
    quantity :int
    order_status :Optional[str]="PENDING"
    piza_size :Optional[str]="SMALL"
    user_id :Optional[int]
    
    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "piza_size":"LARGE"
            }
        }

class OrderStatusModel(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }