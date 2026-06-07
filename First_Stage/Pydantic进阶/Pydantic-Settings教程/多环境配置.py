import os
from pydantic_settings import BaseSettings,SettingsConfigDict

# 获取当前环境,默认为开发环境
env = os.getenv('ENVIRONMENT','development')
# env = os.getenv('ENVIRONMENT','production')


class User(BaseSettings):
    name:str
    age:int
    password:str

    model_config = SettingsConfigDict(
        env_file=(
            # 根据获取的环境不同,加载不同的配置
            f'{env}.env' # 环境特定配置
        ),
        env_file_encoding='utf-8'
    )


user_1 = User()
print(user_1.model_dump())