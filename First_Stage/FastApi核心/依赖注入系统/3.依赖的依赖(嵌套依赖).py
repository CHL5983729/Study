from fastapi import FastAPI,Depends,HTTPException,status
import uvicorn

# 依赖可以依赖其他依赖
'''
执行流程：
    请求/user/?api_key=secret-key
    FastAPI 先执行get_api_key依赖
    将get_api_key的返回值传递给get_user
    将get_user的返回值传递给接口函数
'''

app = FastAPI()

# 第一层依赖
def get_api_key(api_key:str):
    if api_key != 'abc':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='无效的key')
    else:
        return api_key

# 第二层依赖
def get_user(api_key:str = Depends(get_api_key)):
    return {
        'id':1,
        'api_key':api_key
    }

# 使用第二层依赖
@app.get('/user')
async def get_info(user:dict = Depends(get_user)):
    return user



if __name__ == '__main__':
    uvicorn.run(app)