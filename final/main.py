from datetime import datetime
from typing import List
from fastapi import FastAPI
from random import randint
from final import database as db
from final import models

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


@app.get("/fake_users/{count}")
async def create_users(count: int):
    for i in range(count):
        query = db.users.insert().values(name=f'user{i}', surname=f'surname{i}', email=f'mail{i}@mail.ru',
                                         password=f'12345{i}')
        await db.database.execute(query)
    return {'message': f'{count} fake users create'}


@app.get("/fake_products/{count}")
async def create_products(count: int):
    for i in range(count):
        query = db.products.insert().values(name=f'product{i}', descriptions=f'descriptions{i}',
                                            cost=randint(10, 999))
        await db.database.execute(query)
    return {'message': f'{count} fake products create'}


@app.get("/fake_orders/{count}")
async def create_orders(count: int):
    for i in range(count):
        query = db.orders.insert().values(user_id=randint(1, 25), product_id=randint(1, 25), date=datetime.now(),
                                          status="created")
        await db.database.execute(query)
    return {'message': f'{count} fake orders create'}


@app.post("/users/", response_model=models.User)
async def create_user(user: models.UserIn):
    query = db.users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    last_record_id = await db.database.execute(query)
    return {**user.dict(), "id": last_record_id}


# read

@app.get("/users/", response_model=List[models.User])
async def read_users():
    query = db.users.select()
    return await db.database.fetch_all(query)


@app.get("/products/", response_model=List[models.Products])
async def read_products():
    query = db.products.select()
    return await db.database.fetch_all(query)


@app.get("/orders/", response_model=List[models.Orders])
async def read_orders():
    query = db.orders.select()
    return await db.database.fetch_all(query)


# read 1

@app.get("/users/{user_id}", response_model=models.User)
async def read_user(user_id: int):
    query = db.users.select().where(db.users.c.id == user_id)
    return await db.database.fetch_one(query)


@app.get("/products/{product_id}", response_model=models.Products)
async def read_products(product_id: int):
    query = db.products.select().where(db.products.c.id == product_id)
    return await db.database.fetch_one(query)


@app.get("/orders/{order_id}", response_model=models.Orders)
async def read_orders(order_id: int):
    query = db.orders.select().where(db.orders.c.id == order_id)
    return await db.database.fetch_one(query)


# update

@app.put("/users/{user_id}", response_model=models.User)
async def update_user(user_id: int, new_user: models.UserIn):
    query = db.users.update().where(db.users.c.id == user_id).values(**new_user.dict())
    await db.database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.put("/products/{product_id}", response_model=models.Products)
async def update_products(product_id: int, new_product: models.ProductsIn):
    query = db.products.update().where(db.products.c.id == product_id).values(**new_product.dict())
    await db.database.execute(query)
    return {**new_product.dict(), "id": product_id}


@app.put("/orders/{order_id}", response_model=models.Orders)
async def update_orders(order_id: int, new_order: models.OrdersIn):
    query = db.orders.update().where(db.orders.c.id == order_id).values(**new_order.dict())
    await db.database.execute(query)
    return {**new_order.dict(), "id": order_id}

# delete


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = db.users.delete().where(db.users.c.id == user_id)
    await db.database.execute(query)
    return {'message': 'User deleted'}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = db.products.delete().where(db.products.c.id == product_id)
    await db.database.execute(query)
    return {'message': 'Product deleted'}


@app.delete("/orders/{order_id}")
async def delete_orders(order_id: int):
    query = db.orders.delete().where(db.orders.c.id == order_id)
    await db.database.execute(query)
    return {'message': 'Order deleted'}