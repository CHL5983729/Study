from fastapi import FastAPI,Depends
import uvicorn

# FastAPI 支持两种主要的依赖作用域，决定了依赖实例的生命周期。

app = FastAPI()

# 请求作用域(默认)

# 每次请求都会创建一个新依赖实例,请求结束后销毁
class GetDB:
    # 创建实列时执行的函数
    def __init__(self):
        print('创建数据库连接')

    # 销毁实例时执行的函数
    def __del__(self):
        print('关闭数据库连接')

@app.get('/user')
async def get_user(db = Depends(GetDB)):
    return {
        'message':'使用数据库连接'
    }



# 应用作用域(单例)

# 使用Depends(..., use_cache=True)配合全局注册，或者直接使用单例模式，让依赖在整个应用生命周期中只创建一次。
# 应用单例依赖
class AppConfig:
    def __init__(self):
        self.MySQL_url = '123'
        self.redis_url = '321'

# 创建单例实例
app_config = AppConfig()

# 依赖函数返回单例
def get_app_config():
    return app_config

@app.get('/db')
async def get_db_url(config = Depends(get_app_config,use_cache=True)):
    return {
        'MySQL_URL':config.MySQL_url,
        'Redis_URL':config.redis_url
    }



if __name__ == '__main__':
    uvicorn.run(app)