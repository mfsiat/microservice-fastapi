import time

import requests
from colorama import Back
from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel, get_redis_connection
from starlette.requests import Request

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_methods=['*'],
  allow_headers=['*']
)

redis = get_redis_connection(
  host="redis-13515.c252.ap-southeast-1-1.ec2.cloud.redislabs.com",
  port=13515,
  password="H21OzG3kvmL2kyewXqOBABtsITUcunMl",
  decode_responses=True
)

class Order(HashModel):
  product_id: str
  price: float
  fee: float
  total: float
  quantity: int
  status: str # pending, completed, refunded

  class Meta: 
    database = redis

@app.post('/api/v1/orders')
async def create(request: Request, backgroud_tasks: BackgroundTasks): # id, quantity
  body = await request.json()

  url = 'http://localhost:8001/api/v1/products/%s'
  req = requests.get(url % body['id'], verify=False)

  product = req.json()

  order = Order(
    product_id = body['id'],
    price = product['price'],
    fee = 0.2 * product['price'],
    total = 1.2 * product['price'],
    quantity = body['quantity'],
    status = 'pending'
  )
  order.save()

  backgroud_tasks.add_task(order_completed, order)

  order_completed(order)

  return order


def order_completed(order: Order):
  order.status = 'completed'
  order.save()
