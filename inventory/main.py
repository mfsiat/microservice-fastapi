from fastapi import FastAPI
from redis_om import get_redis_connection

app = FastAPI()

# init redis
redis = get_redis_connection(
  host="redis-13515.c252.ap-southeast-1-1.ec2.cloud.redislabs.com",
  port=13515,
  password="H21OzG3kvmL2kyewXqOBABtsITUcunMl",
  decode_responses=True
)

@app.get("/")
async def root():
  return {"message" : "Hello Siat"}

# if __name__ == "__main__":
#     # db.create_all()
#     app.run(debug=True, host="0.0.0.0")
