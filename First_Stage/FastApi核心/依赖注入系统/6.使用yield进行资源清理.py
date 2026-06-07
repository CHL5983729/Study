from fastapi import FastAPI,Depends
import uvicorn


app = FastAPI()


# 数据库连接依赖
async def get_db():
    db = 1
    try:
        yield db # 将连接注入到接口
    finally:
        del db  # 应该是db.close 请求结束后关闭连接

@app.get('/db')
async def get_num(db = Depends(get_db)):
    num = db + 1 # 这里应该是数据库查询操作
    return num


if __name__ == '__main__':
    uvicorn.run(app)