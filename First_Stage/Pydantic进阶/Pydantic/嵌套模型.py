from pydantic import BaseModel,Field


'''当数据结构复杂时,可以使用嵌套模型来组织数据，Pydantic 会自动递归验证所有嵌套字段。'''

# 基本嵌套  一对一

# 子模型
class Address(BaseModel):
    province:str = Field(...,description='省份')
    city:str = Field(...,description='城市')
    detail:str = Field(...,description='详细地址')

# 父模型
class User(BaseModel):
    id:int = Field(...,description='用户ID')
    username:str = Field(...,description='用户名')
    address:Address # 嵌套Address模型

user_1 = User(
    id=1,
    username='张三',
    address=Address(
        province='huebi',
        city='wuhan',
        detail='hubeiwuhanxxx'
    )
)
print(user_1.model_dump())


# 多层嵌套

class Comment(BaseModel):
    id:int
    content:str
    author:str

class Article(BaseModel):
    id:int
    title:str
    comment:Comment # 第一层嵌套

class User(BaseModel):
    id:int
    username:str
    article:Article # 第二层嵌套

user_2 = User(
    id=1,
    username='张三',
    article=Article(
        id=1,
        title='why',
        comment=Comment(
            id=1,
            content='xxxxx',
            author='张三'
        )
    )
)
print(user_2.model_dump())

