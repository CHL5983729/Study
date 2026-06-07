"""用户登录自动刷新令牌,未登录不能访问接口"""
from fastapi import FastAPI,HTTPException,status,Depends,Request
from jose import jwt
from passlib.context import CryptContext
from datetime import timedelta
import uvicorn,datetime
from starlette.responses import FileResponse

app = FastAPI()

# 密码处理函数

# 配置
password_context = CryptContext(schemes=['argon2'],deprecated=['auto'])
# 密码对比
async def verify_password(password:str,hash_pwd:str):
    verify_result = password_context.verify(password,hash_pwd)
    return verify_result


# JWT处理函数

# 配置
KEY = '16f666dd-421f-411f-a89e-da3e3b062fca'
ALGORITHM = 'HS256'

# 生成token
async def create_token(username:str):
    # 生成access_token
    payload = {
        'username':username,
        'type':'access',
        'iat':datetime.datetime.now(datetime.UTC),
        'exp':datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
    }
    access_token = jwt.encode(
        payload,
        KEY,
        algorithm=ALGORITHM
    )
    # 生成refresh_token
    payload = {
        'username':username,
        'type':'refresh',
        'iat':datetime.datetime.now(datetime.UTC),
        'exp':datetime.datetime.now(datetime.UTC) + timedelta(days=7)
    }
    refresh_token = jwt.encode(payload,KEY,algorithm=ALGORITHM)
    return access_token,refresh_token

# 刷新token
async def flush_token(token:str):
    # 先解码token
    try:
        old_payload = jwt.decode(token,KEY,algorithms=[ALGORITHM])
        if old_payload['type'] != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='无效的刷新令牌')
        # 生成新访问令牌
        new_payload = {
            'username':old_payload['username'],
            'type':'access',
            'iat':datetime.datetime.now(datetime.UTC),
            'exp':datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
        }
        new_access_token = jwt.encode(new_payload,KEY,algorithm=ALGORITHM)
        return new_access_token
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='令牌无效')

# 解码token
async def get_current_user(request:Request):
    # 从请求头拿token
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='未登录或token无效')
    token = auth_header[7:]
    try:
        # 解码token
        payload = jwt.decode(token,KEY,algorithms=[ALGORITHM])
        username = payload.get('username')
        token_type = payload.get('type')
        if username is None or token_type != 'access':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='无效的token')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='token无效')
    return username

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('test.html')

# 登录接口
@app.post('/login')
async def login(username:str,password:str):
    if username == '123':
        hash_pwd = '$argon2id$v=19$m=65536,t=3,p=4$B+A8x9h7D4HQ+n9PKYWw9g$r2badhdEWqd2SPaqfR2/A/Lvq2ysZuoGFdd7kjXfIcw' # 模拟从数据库中拿hash密码
        verify_result = await verify_password(password,hash_pwd)
        if verify_result:
            # 生成token
            access_token,refresh_token = await create_token(username)
            return {
                'username':username,
                'access_token':access_token,
                'refresh_token':refresh_token
            }
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='账号或密码错误')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='用户不存在')

# 刷新令牌接口
@app.post('/refresh')
async def refresh_tokens(refresh_token:str):
    new_access_token = await flush_token(refresh_token)
    return {
        'access_token':new_access_token
    }

# 只有登录才能访问的接口
@app.get('/message')
async def get_message(username:str = Depends(get_current_user)):
    return {
        'username':username,
        'message':'这条信息只有登录才能看到'
    }


if __name__ == '__main__':
    uvicorn.run(app)