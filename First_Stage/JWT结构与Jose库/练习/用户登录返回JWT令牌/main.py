from fastapi import FastAPI,Depends
from jose import jwt
from datetime import timedelta
import datetime,uvicorn

app = FastAPI()


SECRET_KEY = 'plk#-mnf3-pqi$'


async def create_token(username:str):
    payload = {
        'username':username,
        'iat':datetime.datetime.now(datetime.UTC),
        'exp':datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
    }
    token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    return token

async def decode_token(token:str):
    try:
        decode_payload = jwt.decode(token,SECRET_KEY,algorithms=['HS256'])
        return {
            'message':decode_payload
        }
    except Exception as e:
        return {
            'error':f'解析失败:{e}'
        }



@app.post('/user/login')
async def login(username:str,password:str = '123'):
    token = await create_token(username)
    return {
        'username':username,
        'token':token
    }

# 获取当前用户
@app.get('/user')
async def get_user(token:dict = Depends(login)):
    result = await decode_token(token['token'])
    return {
        'message':result
    }



if __name__ == '__main__':
    uvicorn.run(app)