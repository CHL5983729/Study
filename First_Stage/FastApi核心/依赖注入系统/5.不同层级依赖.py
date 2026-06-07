from fastapi import FastAPI,Depends,Request,APIRouter
import time
import uvicorn


# FastAPI 允许在三个不同层级声明依赖，影响范围逐级缩小。

# 定义全局依赖
async def log(request:Request):
    start_time = time.time()
    time.sleep(1)
    end_time = time.time()
    print(f'{request.method},{request.url}耗时:{end_time - start_time}s')

# 路由组下的依赖
async def get_info():
    print('admin路由组下的依赖被调用')

# 单个接口依赖
async def get_password():
    print('secret接口的依赖调用')


# 添加全局依赖
app = FastAPI(dependencies=[Depends(log)])

# 所有接口都会自动应用log依赖
@app.get('/user')
async def get_user():
    return {'user'}


# 某个路由组下所有接口
router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(get_info)]
)
@router.get('/admin_1')
async def get_admin():
    return {
        'admin':'admin_1'
    }
@router.get('/admin_2')
async def get_admin_2():
    return {
        'admin':'admin_2'
    }

# 将路由组添加到app中
app.include_router(router)


# 单个接口的依赖
@app.get('/secret',dependencies=[Depends(get_password)])
async def get_secret():
    return {
        'password':'这是机密'
    }



if __name__ == '__main__':
    uvicorn.run(app)