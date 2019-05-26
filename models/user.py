from models import Model


# 定义一个 Uer class 用于保存 用户信息
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = int(form.get('id', -1))

    def exist(self):
        """
        判断对象是否存在
        """
        # 得到所有对象
        users = User.all()
        # 遍历每个对象，看他的name和password是否和self的name password相等
        for u in users:
            if self.username == u.username and self.password == u.password:
                return True
        return False

    def validate_register(self):
        """
        有待完善，
        1，不能让人无限注册
        2，不能让用户名重复
        """
        return len(self.username) > 2 and len(self.password) > 2
