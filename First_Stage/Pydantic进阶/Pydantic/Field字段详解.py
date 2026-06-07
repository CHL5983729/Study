from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime, timezone

'''Field是 Pydantic 中用于自定义单个字段行为的核心函数，可实现参数校验、默认值、文档说明、别名等功能。'''

class User(BaseModel):
    # 可选字段,带默认值和最大最小值
    username:str = Field(...,min_length=2,max_length=10,description='用户名')

    # 必填字段,带最大值和最小值
    age:int = Field(...,ge=1,le=120,description='年龄')

    # 必填字段,可以使用正则表达式来限制
    email:Optional[str] = Field(None,pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',description='邮箱')

    # 隐藏字段,序列化时不返回
    password:str = Field(...,min_length=6,exclude=True,description='密码')

    # 只读字段
    create_at:datetime = Field(default_factory=lambda:datetime.now(),json_schema_extra={'readOnly':True},description='创建时间')


# 验证
if __name__ == '__main__':
    # 正确字段
    user_1 = User(
        username='张三',
        age=18,
        email='zhangsan@123.com',
        password='123456',
    )
    print(user_1.model_dump())

    # 错误字段
    try:
        user_2 = User(
            username='李', # 长度不够
            age=0, # 年龄过小
            email='123-w', # 邮箱格式错误
            password='123' # 密码过短
        )
        print(user_2.model_dump())
    # 捕获异常会给出详细的错误地方
    except Exception as e:
        print(e)