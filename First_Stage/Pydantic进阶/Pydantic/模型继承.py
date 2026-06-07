from pydantic import BaseModel,Field
from typing import Optional

'''模型继承是 Pydantic 中代码复用的核心手段，可以避免重复定义相同的字段。'''


# 基础模型
class UserBase(BaseModel):
    username:str = Field(...,min_length=2,max_length=10,description='用户名')
    email:Optional[str] = Field(None,description='用户邮箱')
    age:Optional[int] = Field(None,ge=1,le=120,description='年龄')


# 创建用户模型
class User(UserBase):
    password:str = Field(...,description='密码')


# 创建User模型时会继承UserBase里面所有字段
user_1 = User(
    username='张三',
    password='123'
)

print(user_1)