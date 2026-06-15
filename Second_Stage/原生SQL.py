from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base


'''创建数据库连接'''
engine = create_engine('sqlite:///demo.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 用户表
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    posts = relationship('Post', back_populates='author')

# 文章表
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates='posts')

'''核心执行方式'''
session = Session()
# 执行原生SQL
result = session.execute(text('select * from users where name = "张三"'))
# 获取查询结果
user = result.first()
print(f'ID:{user.id},name:{user.name}')
session.close()

'''参数绑定(防止SQL注入)'''
session = Session()
username = '张三'
result = session.execute(text('select * from users where name = :name'),
                        {'name':username})
user = result.first()
print(f'ID:{user.id},name:{user.name}')
session.close()



