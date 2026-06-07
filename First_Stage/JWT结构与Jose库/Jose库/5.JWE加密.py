from jose import jwe
from datetime import timedelta
import datetime
import json


'''如果需要在 JWT 中存储敏感信息，应该使用 JWE 进行加密：'''


# 配置(一般存储在evn文件里面的)
# 密钥
SECRET_KEY = '12345678901234567890123456789012'
# 算法
ALGORITHM = 'HS256'
# 令牌过期时间
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 载荷
payload = {
    'sub':'user_1', # 主题(通常是用户ID)
    'iss':'www.xxx.com', # 签发者
    'adu':'www.xxx.com', # 受众
    'iat': int(datetime.datetime.now(datetime.UTC).timestamp()),
    'exp': int((datetime.datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),

    # 自定义声明
    'user_name':'mike',
    'password':123456
}

# 1. 必须先把字典转成 JSON 字符串
payload_str = json.dumps(payload)

# 2. 生成加密的jwt
encrypted_token = jwe.encrypt(
    payload_str,
    SECRET_KEY,
    algorithm='dir', # 直接使用密钥加密
    encryption='A256GCM' # 加密算法
)

print(f'加密后的令牌:{encrypted_token.decode('utf8')}')

# 解密令牌
decrypted_data = jwe.decrypt(
    encrypted_token,
    SECRET_KEY
)
print(f'解密后的令牌:{decrypted_data}')