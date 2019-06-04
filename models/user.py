from models import Model
import hashlib
import sqlite3
from utils import salted_password
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
        self.password = salted_password(self.password)
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


    def save(self):
        """
        sql_save 函数用于把一个 User的实例保存到sqlite中
        """
        #不用管user_id，在数据库里自增

        path = self.sql_path()
        conn = sqlite3.connect(path)
        sql_insert = '''
        INSERT INTO
            user(username,password)
        VALUES
            (?, ?);
        '''
        conn.execute(sql_insert, (self.username, self.password))
        print('插入数据成功')
        conn.commit()
        conn.close()
