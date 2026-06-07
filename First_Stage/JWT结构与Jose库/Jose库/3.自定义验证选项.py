from jose import jwt
from datetime import timedelta
import datetime

# 密钥
SECRET_KEY = 'aaa-bbb-ccc'
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

token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
print(f'对称算法加密:{token}')
info = jwt.decode(token,SECRET_KEY,algorithms=['HS256'],
                # 自定义验证选项
                options = {
                    'verify_exp':True, # 验证过期时间
                    'verify_iat':True, # 验证签发时间 # 三个默认都是True
                    'verify_nbf':True, # 验证生效时间
                    'require':['exp','iss','sub'] # 自定义必须包含的声明
                })
print(f'对称算法解密:{info}')