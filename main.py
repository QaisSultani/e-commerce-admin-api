from fastapi import FastAPI, Query, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from enum import Enum
from typing import Optional, Annotated

import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class InventoryBase(BaseModel):
    product_name: str
    product_description: str
    price: float
    remaining_stock: int
    total_sale_qty: int
    total_sale_amount: float
    user_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post('/inventories', status_code=status.HTTP_201_CREATED)
async def create_inventory(inventory: InventoryBase, db: db_dependency):
    db_inventory = models.Inventory(**inventory.model_dump())
    db.add(db_inventory)
    db.commit()


# # INTRODUCTION
# # routes
# @app.get('/demo', description='this route is gonna show all the things that can be done for api doc', deprecated=True)
# async def demo():
#     return {'message': 'hello form demo'}

# @app.get('/')
# async def sales():
#     return {'message': 'hello world'}

# @app.post('/')
# async def post():
#     return {'message': 'hello from post route'}

# @app.put('/')
# async def put():
#     return {'message': 'hello from put route'}

# # PATH PARAMETERS
# @app.get('/users')
# async def list_users():
#     return {'message': 'list users route'}

# @app.get('/users/me')
# async def get_current_user():
#     return {'message': 'this is current user'}

# # path parameters
# @app.get('/users/{user_id}')
# async def get_user(user_id: str):
#     return {'user_id': user_id}

# class FoodEnum(str, Enum):
#     fruits = 'fruits'
#     vegetables = 'vegetables'
#     dairy = 'dairy'

# @app.get('/foods/{food_name}')
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {'food_name': food_name, 'message': 'you are healthy'}
    
#     if food_name.value == 'fruits':
#         return {
#             'food_name': food_name,
#             'message': 'you are still healthy, but like sweet things',
#         }
    
#     return {'food_name': food_name, 'message': 'i like chocolate milk'}

# # QUERY PARAMETERS
# # query parameters
# fake_items_db = [{'item_name': 'Faa'}, {'item_name': 'Fee'}, {'item_name': 'Fii'}, {'item_name': 'Foo'}, {'item_name': 'Fuu'}]

# # @app.get('/items')
# # async def list_items(skip: int = 0, limit: int = 10):
# #     return {'list_items': fake_items_db[skip: skip+limit]}

# # @app.get('/items/{item_id}')
# # async def get_item(item_id: str, required_query_param: str, q: str | None = None, short: bool = False):
# #     item = {'item_id': item_id, 'required_query_param': required_query_param}
# #     if q:
# #         item.update({'q': q})
# #     if not short:
# #         item.update({'description': 'here is long version'})
# #     return item

# @app.get('/users/{user_id}/items/{item_id}')
# async def get_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
#     item = {'owner_id': user_id, 'item_id': item_id}
#     if q:
#         item.update({'q': q})
#     if not short:
#         item.update({'description': 'here is long version'})
#     return item

# # REQUEST BODY
# # post  routes
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: int
#     tax: float | None = None
#     pass

# @app.post('/items')
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({'price_with_tax': price_with_tax})
#     return item_dict

# @app.put('/items/{item_id}')
# async def item_with_put(item_id: int, item: Item, q: str | None = None):
#     result = {'item_id': item_id, **item.model_dump()}
#     if q:
#         result.update({'q': q})
#     return result

# # QUERY PARAMETERS AND STRING VALIDATION
# @app.get('/items')
# async def read_items(q: str = Query(
#     ...,
#     min_length=3,
#     max_length=50,
#     title='Sample Query String',
#     description='this is a sample query string',
#     alias='item-query'
#     )):
#     results = {'items': [{'item_id': 'foo'}, {'item_id': 'bar'}]}
#     if q:
#         results.update({'q': q})
#     return results

# @app.get('/items/hidden')
# async def hidden_query(hidden_query: str | None = Query(None, include_in_schema=False)):
#     if hidden_query:
#         return {'hidden_query': hidden_query}
#     return {'hidden_query': 'Not Found'}

# # PATH PARAMETERS AND NUMERIC VALIDATIONS
