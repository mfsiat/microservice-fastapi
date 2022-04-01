from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import HashModel, get_redis_connection

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['http://localhost:3000'],
  allow_methods=['*'],
  allow_headers=['*']
)

# init redis
redis = get_redis_connection(
  host="redis-13515.c252.ap-southeast-1-1.ec2.cloud.redislabs.com",
  port=13515,
  password="H21OzG3kvmL2kyewXqOBABtsITUcunMl",
  decode_responses=True
)

# create the model for redis to connect
class Product(HashModel):
  name: str
  price: float 
  quantity: int

  class Meta: 
    database = redis

@app.get("/")
async def root():
  return {"message" : "Hello Siat"}


# get req for products
@app.get('/api/v1/products')
def all():
  return Product.all_pks()
