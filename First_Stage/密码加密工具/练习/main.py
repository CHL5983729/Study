"""用户注册并且加密密码"""
from fastapi import FastAPI
from passlib.context import CryptContext
import uvicorn


app = FastAPI()


# 加密配置
pwd_context = CryptContext(
    schemes=['argon2'], # 使用argon2算法
    deprecated=['auto'] # 自动弃用过时的算法
)

@app.post('/user/register')
async def register(username:str,password:str):
    # 进行密码加密
    hash_password = pwd_context.hash(password)
    return {
        'username':username,
        'hash_password':hash_password
    }


if __name__ == '__main__':
    uvicorn.run(app)