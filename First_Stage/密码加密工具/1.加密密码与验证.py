from passlib.context import CryptContext

'''
CryptContext 是 passlib 的灵魂，它是一个 "密码安全策略指挥中心"，负责：
统一管理多种哈希算法
自动识别数据库中现有哈希的算法
验证密码并在需要时触发升级
集中配置所有安全参数
'''

# 创建上下文 只支持bcrypt算法
password_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

# 获取哈希密码
hash_password = password_context.hash('password')
print(f'加密后的密码:{hash_password}')


# 验证密码
result = password_context.verify('password',hash_password)
print(f'结果:{result}')

result_2 = password_context.verify('123',hash_password)
print(f'结果_2:{result_2}')