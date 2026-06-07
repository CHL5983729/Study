"""路由文件"""
from fastapi import APIRouter
import time

# user路由
user = APIRouter(
    prefix='/user',
    tags=['user']
)

# 获取用户信息
@user.get('/user')
async def get_user_info(user_name:str,user_id:int):
    time.sleep(2) # 模拟数据库查询操作
    return {
        'user_id':user_id,
        'user_name':user_name
    }

# 查看用户权限
@user.get('/user/power')
async def check_user_power(user_name:str):
    if user_name == 'vip':
        time.sleep(1.5)
        return {
            'power':'超级会员'
        }
    else:
        time.sleep(3)
        return {
            'power':'普通用户'
        }
