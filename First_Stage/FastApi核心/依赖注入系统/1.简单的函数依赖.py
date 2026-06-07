from fastapi import FastAPI,Depends
import uvicorn


app = FastAPI()


# 定义一个依赖函数
def get_info(user_id:int,user_name:str):
    return {
        'user_id':user_id,
        'user_name':user_name
    }

# 在路由中使用依赖注入
@app.get('/user')
async def get_user_info(info:dict = Depends(get_info)):
    return info


if __name__ == '__main__':
    uvicorn.run(app)