import redis,time
from fastapi import FastAPI,Depends,Request
import logging
import uvicorn

# Redis连接池
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    decode_responses=True
)
# Redis依赖
async def client_redis():
    r = redis.Redis(connection_pool=redis_pool)
    try:
        yield r
    except Exception as e:
        logging.error(f'Redis连接错误:{e}')

# log依赖
async def log(request:Request):
    start_time = time.time()
    yield
    end_time = time.time()
    logging.getLogger().setLevel(level=logging.INFO)
    logging.info(f'{request.method}:{request.url}:耗时:{end_time - start_time}s')

app = FastAPI(dependencies=[Depends(log)])

@app.get('/user')
async def get_user(user_id:int,r = Depends(client_redis)):
    user_name = r.get(f'{user_id}')
    return user_name

if __name__ == '__main__':
    uvicorn.run(app)