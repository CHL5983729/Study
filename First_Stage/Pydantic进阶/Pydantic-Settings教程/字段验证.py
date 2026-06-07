from pydantic import Field,field_validator
from pydantic_settings import BaseSettings
from typing import Optional



class User(BaseSettings):
    # 进行字段限制
    name:str = Field(...,validation_alias='NAME',description='用户名')
    age:Optional[int] = Field(None,validation_alias='AGE',description='年龄')
    password:str = Field(...,validation_alias='PASSWORD',description='密码')

    # 字段验证器
    @field_validator('name')
    @classmethod
    def check_name(cls,name:str):
        if name.isalpha():
            return name
        else:
            raise ValueError('name不能有特殊字符')


# 如果在Field后加了设置别名,传参时只能使用别名
user_1 = User(
    NAME='alice',
    AGE=18,
    PASSWORD='123'
)
print(user_1.model_dump())
