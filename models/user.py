from models import Model


# 定义一个 Uer class 用于保存 用户信息
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        return self.username == 'xxx' and self.password == 'xxx'

    def validate_register(self):
        """有待完善，不能让人无线注册"""
        return len(self.username) > 2 and len(self.password) > 2

