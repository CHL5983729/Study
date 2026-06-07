from pydantic import BaseModel,Field,field_validator,model_validator

'''定义自定义验证器来对字段进行验证'''



class User(BaseModel):
    username:str = Field(...,description='用户名')
    age:int = Field(...,description='用户年龄')

    # 字段验证器
    # 进行字段的验证
    @field_validator('username')
    @classmethod
    def check_username(cls,username:str):
        # 判断username是否没有特殊字符
        if username.isalpha():
            return username
        else:
            raise ValueError('username不符合要求')

    # 模型验证器
    # 比较username与age的关系
    @model_validator(mode='after')
    def check_relationships(self):
        # 自定义检查
        if self.username == '张三' and self.age == 18:
            return self
        else:
            raise ValueError('错误')

user_1 = User(
    username='张三',
    age=18
)
print(user_1.model_dump())