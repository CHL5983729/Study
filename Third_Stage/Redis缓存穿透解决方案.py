import random
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped
from sqlalchemy import select, String, Integer
import asyncio
import redis.asyncio as redis
import time
from pybloom_live import BloomFilter

# 数据库模型表
class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(50))

# 数据库连
redis_pool = redis.ConnectionPool(
    host = 'localhost',
    port = 6379,
    decode_responses = True,
    max_connections = 100
)
redis_client = redis.Redis(connection_pool = redis_pool)


URL = 'mysql+aiomysql://root:123456@localhost:3306/study?charset=utf8mb4'
async_engine = create_async_engine(URL,echo=False)
async_session = async_sessionmaker(
    bind = async_engine,
    class_= AsyncSession,
    autoflush = False,
    expire_on_commit = False
)

"""解决方案"""


# 1.缓存空值
async def simulating_penetration_1(user_id:int):
    # 在Redis中查询用户
    key = f'user_id:{user_id}'
    # 先判断用户是否存在
    null_flag = await redis_client.get(f'null_user{user_id}')
    if null_flag == 'null':
        return None
    # 在Redis中查找
    user_data = await redis_client.hgetall(key)
    if user_data:
        # 命中缓存，直接返回数据
        return user_data
    else:
        # 未命中缓存，到数据库中查询
        async with async_session() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user_obj = result.scalar_one_or_none()
            if user_obj:
                user_data = {
                    'id':user_obj.id,
                    'name':user_obj.name
                }
                await redis_client.hset(key,mapping={
                    'id':user_obj.id,
                    'name':user_obj.name
                })
                return user_data
            else:
                null_key = f'null_user{user_id}'
                exp_time = random.randint(180,300)
                await redis_client.set(null_key,'null',nx = True,ex = exp_time)
                return None



# 2.布隆过滤器
# 配置布隆过滤器
bloom_filter = BloomFilter(capacity=1000000,error_rate=0.0001) # 预计存储100万条数据，误判率0.01%
# 初始化布隆过滤器
async def init_bloom_filter():
    async with async_session() as session:
        stmt = select(User.id)
        result = await session.execute(stmt)
        user_ids = result.scalars().all()
    # 将MySQL中的id存入布隆过滤器
    count = 0
    for user_id in user_ids:
        bloom_filter.add(str(user_id))
        count += 1
    print(f'布隆过滤器加载完成!存入:{count}条数据')
# 查询函数
async def simulating_penetration_2(user_id:int):
    # 先判断id是否在布隆过滤器中
    user_id_str = str(user_id)
    if user_id_str not in bloom_filter:
        return None
    else:
        key = f'user_id:{user_id}'
        user_data = await redis_client.hgetall(key)
        if user_data:
            return user_data
        else:
            async with async_session() as session:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                user_obj = result.scalar()
                # 写入Redis
                await redis_client.hset(f'user_id:{user_obj.id}',mapping={
                    'id':user_obj.id,
                    'name':user_obj.name
                })
                return {
                    'id':user_obj.id,
                    'name':user_obj.name
                }



async def main(user_id:int,func):
    await init_bloom_filter()

    total_start = time.time()
    start1 = time.time()
    # 1. 第一次查询
    res1 = await func(user_id)
    end1 = time.time()
    print(f"第一次查询（查MySQL+写Redis）耗时：{end1 - start1}s")

    start2 = time.time()
    # 2. 第二次纯读Redis
    res2 = await func(user_id)
    end2 = time.time()
    print(f"第二次查询（仅Redis读取）耗时：{end2 - start2}s")

    await async_engine.dispose()
    total_end = time.time()
    print(f"程序总运行时长：{total_end - total_start}s")
    print("结果1：", res1, "结果2：", res2)

if __name__ == '__main__':
    asyncio.run(main(1,simulating_penetration_2))




