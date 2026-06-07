from pydantic_settings import BaseSettings,SettingsConfigDict

'''创建一个继承自BaseSettings的类,并定义字段'''

# 定义基本配置模型
class Settings(BaseSettings):
    name:str
    host:str
    port:int

# 实例化配置
settings = Settings(
    name='MyDataBase',
    host='localhost',
    port=8000
)

# 使用配置  Pydantic Settings 会自动从环境变量中读取配置值。
print(f''
      f'name:{settings.name},'
      f'host:{settings.host},'
      f'port:{settings.port},'
      )


# 从.env文件中加载配置
class DataBase(BaseSettings):
    db_name:str
    db_url:str
    db_password:str

    model_config = SettingsConfigDict(
        env_file='db.env', # 指定env文件
        env_file_encoding='utf-8', # 指定编码
        extra='ignore' # 忽略未在配置中定义的环境变量
    )
# 会读取.env文件中的配置,不用手动填入字段 不区分大小写
db = DataBase()
print(db)

'''
Pydantic Settings 按照以下优先级顺序加载配置（从高到低）
1（最高）初始化参数实例化模型时直接传入的值
2系统环境变量操作系统中设置的环境变量
3.env 文件变量项目目录下的 .env 文件中定义的值
4配置文件JSON、YAML、TOML 等配置文件
5秘密文件Docker secrets 或 Kubernetes secrets
6（最低）类默认值在配置类中定义的默认值
'''