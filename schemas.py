from pydantic import BaseModel
from typing import Optional 




class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]


    class Config:
        orm_mode = True
        schema_extra={
            'example':{
                'username':'Christa',
                'email':'christadushime@gmail.com',
                'password':'Hello',
                'is_staff':False,
                'is_active': True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key:str='c9b281441ce1ffb2f8761adbf34e50a66df49ec7769b95e0ff81985820953873'

class LoginModel(BaseModel):
    username:str
    password:str



class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    user_id:Optional[int]
    
    class config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }

class OrderStatusModel(BaseModel):
    order_status:Optional[str]="PENDING"

    class config:
        orm_mode=True
        schema_extra={
            "example": {
                "order_status":"PENDING"
            }
        }

class OrderPlacementModel(BaseModel):
    quantity:int
    pizza_size: str

    class config:
        orm_mode=True
        schema_extra={
            "example": {
                "quantity": 3,
                "pizza_size": "LARGE"
            }
        }