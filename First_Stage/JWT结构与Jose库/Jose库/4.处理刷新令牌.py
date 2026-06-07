from jose import jwt
from datetime import timedelta
import datetime

# 密钥
SECRET_KEY = 'aaa-bbb-ccc'
# 算法
ALGORITHM = 'HS256'
# 令牌过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 生成令牌函数
def create_token(user_name:str):
    # 访问令牌,短期有效
    access_payload = {
        'sub':user_name,
        'type':'access',
        'exp':datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
    }
    access_token = jwt.encode(access_payload,SECRET_KEY,algorithm=ALGORITHM)

    # 刷新令牌,长期有效
    refresh_payload = {
        'sub':user_name,
        'type':'refresh',
        'exp':datetime.datetime.now(datetime.UTC) + timedelta(days=7)
    }
    refresh_token = jwt.encode(refresh_payload,SECRET_KEY,algorithm=ALGORITHM)

    return {
        'access_token':access_token,
        'refresh_token':refresh_token
    }

# 使用刷新令牌获取新的访问令牌
def refresh_access_token(refreshed_token:str):
    try:
        payload = jwt.decode(refreshed_token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get('type') != 'refresh':
            print(f'无效的刷新令牌')
        else:
            # 生成新的访问令牌
            new_access_payload = {
                'sub':payload['sub'],
                'type':'access',
                'exp':datetime.datetime.now(datetime.UTC) + timedelta(minutes=15)
            }
            new_access_token = jwt.encode(new_access_payload,SECRET_KEY,algorithm=ALGORITHM)
            return {
                'access_token':new_access_token
            }
    except Exception as e:
        print(f'刷新令牌失败:{e}')



token = create_token('chl')
print(f'生成的refresh_token和access_token:{token}')

refresh_token = token['refresh_token']

access_token = refresh_access_token(refresh_token)
print(f'refresh_token生成的access_token:{access_token}')