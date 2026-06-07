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

# 1.对称算法
'''
HS256/HS384/HS512：使用 HMAC-SHA 系列算法，同一个密钥用于签名和验证
优点：速度快、实现简单
缺点：密钥泄露会导致完全不安全，不适合分布式系统
'''
token_1 = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
print(f'对称算法加密:{token_1}')
info_1 = jwt.decode(token_1,SECRET_KEY,algorithms=['HS256'])
print(f'对称算法解密:{info_1}')

# 2.非对称算法
'''
RS256/RS384/RS512：使用 RSA 非对称加密算法，私钥签名，公钥验证
优点：安全性高，公钥可以公开分发
缺点：速度比对称算法慢
对于 RS256，你需要一个RSA 私钥文件（PEM 格式），而不是一个普通的字符串密钥。
'''
# 私钥(用于签名)
with open("private_key.pem", "r") as f:
    private_key = f.read()
token_2 = jwt.encode(payload,private_key,algorithm='RS256')
print(f'对称算法加密:{token_2}')

# 公钥(用于验证)
with open("public_key.pem", "r") as f:
    public_key = f.read()
info_2 = jwt.decode(token_2,public_key,algorithms=['RS256'])
print(f'对称算法解密:{info_2}')

# 3.椭圆曲线算法
'''
ES256/ES384/ES512：使用椭圆曲线数字签名算法
优点：相同安全级别下，密钥长度更短，签名和验证速度更快
推荐：现代应用优先使用 ES256
'''
# 私钥(用于签名)
with open("ec_private_key.pem", "r") as f:
    ec_private_key = f.read()
token_3 = jwt.encode(payload,ec_private_key,algorithm='ES256')
print(f'椭圆曲线算法加密:{token_3}')

# 公钥(用于验证)
with open("ec_public_key.pem", "r") as f:
    ec_public_key = f.read()
info_3 = jwt.decode(token_3,ec_public_key,algorithms=['ES256'])
print(f'椭圆曲线算法解密:{info_3}')
















