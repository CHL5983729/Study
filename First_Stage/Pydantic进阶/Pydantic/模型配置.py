from pydantic import BaseModel,ConfigDict,Field

'''进行全局统一的模型配置'''
class User(BaseModel):
    username:str = Field(...,min_length=2,max_length=10,description='用户名')
    password:str = Field(...,description='密码')

    # 进行模型配置
    model_config = ConfigDict(
        extra='forbid', # 数据校验
        str_strip_whitespace=True # 去除空格
    )

user_1 = User(
    username='   alice',
    password='123'
)
print(user_1.model_dump())

'''
extra	处理额外字段的模式：'ignore'（默认v2忽略）、'forbid'（抛出错误）、'allow'（保留在模型中）
frozen	模型是否可哈希（不可变），不可变模型可以当字典key
validate_assignment	设置属性时是否触发验证，默认True
populate_by_name	允许通过字段原名或别名赋值，默认False
str_strip_whitespace	字符串字段自动 strip
str_min_length / str_max_length	全局字符串长度限制
arbitrary_types_allowed	是否允许任意类型字段（默认False）
use_enum_values	序列化枚举时是否使用枚举值而非枚举对象
ser_json_timedelta	timedelta序列化为'iso8601'或数字
ser_json_bytes	bytes序列化为'utf8'或'base64'
coerce_numbers_to_str	数字是否允许转为字符串
'''