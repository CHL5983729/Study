from jose import jwt
from datetime import timedelta
import datetime

# 配置(一般存储在evn文件里面的)
# 密钥
SECRET_KEY = 'aaa-bbb-ccc'
# 算法
ALGORITHM = 'HS256'
# 令牌过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 载荷
payload = {
    'sub':'user_1', # 主题(通常是用户ID)
    'iss':'www.xxx.com', # 签发者
    'adu':'www.xxx.com', # 受众
    'iat':datetime.datetime.now(datetime.UTC), # 签发时间
    'exp':datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), # 过期时间

    # 自定义声明
    'user_name':'mike',
    'user_id':1
}

# 生成令牌
token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
print(f'token:{token}')

# 验证并解析JWT
try:
    # 验证令牌并解析载荷
    decode_payload = jwt.decode(
        token, # jwt令牌
        SECRET_KEY, # 密钥
        algorithms=[ALGORITHM], # 算法
        issuer='www.xxx.com', # 验证签发者
        audience='www.xxx.com' # 验证受众
    )
    print(decode_payload)
except Exception as e:
    print(f'解析失败:{e}')