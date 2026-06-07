from passlib.context import CryptContext

'''这是 passlib 最强大的功能，允许你同时支持新旧算法，并在用户登录时自动升级'''

# 配置上下文,支持三种算法,优先使用argon2
password_context = CryptContext(
    # 支持的算法列表,顺序表示优先级
    schemes=['argon2','bcrypt','pbkdf2_sha256'],
    # 默认使用的算法
    default='argon2',
    # 被标记为废弃的算法,使用时会自动升级
    deprecated=['pbkdf2_sha256']
)

# 配置的导出

# 导出为INI格式文件
config_ini = password_context.to_string()
print(f'INI格式配置:{config_ini}')


# 导入配置
# INI字符串导入
pwd_context_ini = CryptContext.from_string(config_ini)

# 从INI文件导入
pwd_context_path = CryptContext.from_path('config.ini')