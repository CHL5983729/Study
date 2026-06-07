"""主文件"""
from fastapi import FastAPI,Depends,Request
from routers import user
import uvicorn
import time
import logging



#  定义全局日志函数
async def global_log(request:Request):
    start_time = time.time()
    yield 
    end_time = time.time()
    # 设置日志级别信息
    logging.getLogger().setLevel(level=logging.INFO)
    logging.info(f'{request.client.host}:访问了{request.method}:{request.url}'
        f'耗时:{end_time - start_time}s')

app = FastAPI(dependencies=[Depends(global_log)])

# 添加路由
app.include_router(user)

if __name__ == '__main__':
    uvicorn.run(app)