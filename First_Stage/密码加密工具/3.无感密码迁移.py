from passlib.context import CryptContext

'''用户登录时，验证密码成功后，自动用新算法重新哈希并保存。'''

# 配置支持新旧算法的上下文
pwd_context = CryptContext(
    schemes=['argon2','bcrypt','pbkdf2_sha256','md5_crypt'],
    default='argon2',
    deprecated=['pbkdf2_sha256','md5_crypt']
)

def login(password:str):
    # 从数据库中获取哈希密码
    hash_password = '$1$PbhGhcI6$PU5dPZbHfnSDEcO5uaAIU/'
    # 验证密码并且检查是否需要升级
    result,new_hash = pwd_context.verify_and_update(
        password,hash_password
    )
    if not result:
        print('密码错误')
    if new_hash:
        # 将新的hash密码保存到数据库
        print(f'新hash密码:{new_hash}')


login('password')