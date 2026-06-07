from passlib.context import CryptContext

# 配置上下文,支持三种算法,优先使用argon2
password_context = CryptContext(
    # 支持的算法列表,顺序表示优先级
    schemes=['argon2','bcrypt','pbkdf2_sha256'],
    # 默认使用的算法
    default='argon2',
    # 被标记为废弃的算法,使用时会自动升级
    deprecated=['pbkdf2_sha256']
)

# 识别hash算法
hash_str = '$argon2id$v=19$m=65536,t=3,p=4$...'
print(password_context.identify(hash_str))

