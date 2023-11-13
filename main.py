from fastapi import FastAPI, Query, HTTPException, Depends, status
from typing import Optional
from enum import Enum

from modelsbase import ProductBase, UpdateStockBase
from models import Product
from dependency import db_dependency
from database import engine
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# create product with inventory
@app.post('/products', status_code=status.HTTP_201_CREATED, description='creates product and add it\'s inventory details')
async def create_product(product_initial: ProductBase, db: db_dependency):
    product_final = product_initial.model_dump()
    product_final.update({'total_sale_qty':0, 'total_sale_amount':0, 'low_stock':product_initial.remaining_stock < 10})
    new_product = Product(**product_final)
    db.add(new_product)
    db.commit()
    return new_product.as_dict()

# retreave product details
@app.get('/products/{id}', status_code=status.HTTP_200_OK, description='gets product details')
async def get_product(id: int, db: db_dependency):
    product = db.query(Product).filter_by(id=id).first()
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='product details not found!')

# updates stock
@app.patch('/products/{id}', status_code=status.HTTP_200_OK, description='modifies product stock')
async def update_stock(id: int,  db: db_dependency, updated_product: UpdateStockBase):
    product_final = updated_product.model_dump()
    product_final.update({'low_stock': updated_product.remaining_stock < 10})
    new_product = Product(**product_final)
    product = db.query(Product).filter_by(id=id).first()
    if product:
        product.remaining_stock = new_product.remaining_stock
        product.low_stock = new_product.low_stock
        db.commit()
        db.refresh(product)
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='couldn\'t update! product details not found!')






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
