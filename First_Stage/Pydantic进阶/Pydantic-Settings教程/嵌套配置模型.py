from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



class MySQLConfig(BaseModel):
    MySQL_name: str
    MySQL_host: str
    MySQL_password: str

    # 将url标记为属性 可以像访问普通属性一样访问这个方法
    @property
    # 返回数据库连接URL
    def mysql_url(self):
        return f'{self.MySQL_name}:{self.MySQL_host}:{self.MySQL_password}'


class RedisConfig(BaseModel):
    Redis_name: str
    Redis_host: str
    Redis_password: str

    @property
    def redis_url(self):
        return f'{self.Redis_name}:{self.Redis_host}:{self.Redis_password}'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='db.env',
        env_nested_delimiter='__',  # 嵌套环境变量分割符
    )
    # 嵌套配置
    # 在.env文件中的格式是 XXX__XXX=XXX

    mysql_config: MySQLConfig
    redis_config: RedisConfig

settings = Settings()

print(settings.mysql_config.mysql_url)
print(settings.redis_config.redis_url)
