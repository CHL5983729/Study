from fastapi import FastAPI,Depends
import uvicorn

# 类依赖比函数依赖更强大,适合封装有状态的逻辑和复杂依赖

app = FastAPI()


# 定义一个类依赖
class GetInfo:
    def __init__(self,user_id:int,user_name:str):
        self.user_id = user_id
        self.user_name = user_name


# 使用类依赖
@app.get('/user')
                                # 这里的GetInfo可以省略掉FastApi会自动实列化
async def get_user_info_1(info:GetInfo = Depends(GetInfo)):
    # 这里的info是GetInfo类的实例
    return {
        'user_id':info.user_id,
        'user_name':info.user_name
    }


if __name__ == '__main__':
    uvicorn.run(app)