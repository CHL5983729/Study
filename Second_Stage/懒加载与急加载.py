from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,select
from sqlalchemy.orm import sessionmaker,relationship,declarative_base
from sqlalchemy.orm import joinedload,selectinload,subqueryload



'''创建数据库连接'''
engine = create_engine('sqlite:///demo.db',echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


'''定义表'''
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    # 定义与Port的一对多关系
    posts = relationship('Post',back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True)
    title = Column(String(100))
    content = Column(String(500))
    user_id = Column(Integer,ForeignKey('users.id'))
    # 定义与User的多对一关系
    author = relationship('User',back_populates='posts')

print('懒加载日志')

'''懒加载'''
session = Session()
# 查询单个用户
stmt = select(User).where(User.name == '张三')
user = session.execute(stmt).scalar_one()
print(f'用户:{user.name}')
# 访问关联的posts属性 到这里才会执行第二条SQL查询
print(f'文章:{len(user.posts)}')
session.close()

'''懒加载产生的N+1问题'''
session = Session()
# 查询所有用户
stmt = select(User)
users = session.execute(stmt).scalars().all()
print(f'用户数量:{len(users)}')
# 遍历每个用户，访问他们的文章，每个用户都会触发一条新的SQL
for user in users:
    print(f'{user.name}写了:{len(user.posts)}篇文章')
session.close()



'''急加载'''
print('-'*100)
print('JOIN连接查询日志')

session = Session()
# 使用joinedload急加载
stmt = select(User).options(joinedload(User.posts)).where(User.name == '张三')
user = session.execute(stmt).unique().scalar_one_or_none()
print(f'用户:{user.name}')
print(f'文章数量:{len(user.posts)}') #  这里不会产生其他的SQL查询
session.close()

print('-'*100)
print('IN子查询日志')
session = Session()
# 使用selectinload急加载
stmt = select(User).options(selectinload(User.posts))
users = session.execute(stmt).scalars().all()
print(f'查询到:{len(users)}条用户')
for user in users:
    print(f'{user.name}写了:{len(user.posts)}篇文章')
session.close()

print('-'*100)
print('子查询日志')
session = Session()
# 使用subqueryload急加载
stmt = select(User).options(subqueryload(User.posts))
users = session.execute(stmt).scalars().all()
print(f'查询到:{len(users)}条用户')
for user in users:
    print(f'{user.name}写了:{len(user.posts)}篇文章')
session.close()


















