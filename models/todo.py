from models import Model
import sqlite3

# 定义一个 class 用于保存 Todo
class Todo(Model):
    def __init__(self, form):
        self.title = form.get('title', '')
        self.id = int(form.get('id', -1))
        self.user_id = int(form.get('user_id', -1))


    def exist(self):
        """
        判断对象是否存在
        """
        # 得到所有对象
        todo = self.select()
        # 遍历每个对象，看他的name和password是否和self的name password相等
        if len(todo) != 0:
            return True
        return False


    def save(self):
        """
        save 函数用于把一个 todo 的实例保存到文件中
        """
        path = "db/User.sqlite"
        conn = sqlite3.connect(path)
        sql_insert = '''
        INSERT INTO
            Todo(title,user_id)
        VALUES
            (?, ?);
        '''
        conn.execute(sql_insert, (self.title, self.user_id))
        print('插入数据成功')
        conn.commit()
        conn.close()


    @classmethod
    def all(cls, user_id):
        """
        得到todo的所有存储的数据， 在list中每个tuple中
        """
        path = "db/User.sqlite"
        conn = sqlite3.connect(path)
        sql_select = '''
        SELECT
            *
        FROM
            Todo
        WHERE
            user_id=?
        '''
        # 这是读取数据的套路
        cursor = conn.execute(sql_select, (user_id,))
        todos = list(cursor)
        conn.commit()
        conn.close()
        return todos


    def select(self):
        path = "db/User.sqlite"
        conn = sqlite3.connect(path)
        sql = '''
        SELECT
           *
        FROM
            Todo
        WHERE
            id=? and user_id=? 
        '''
        # 这是读取数据的套路
        cursor = conn.execute(sql, (self.id, self.user_id))
        todo = list(cursor)
        conn.commit()
        conn.close()
        return todo

    def remove(self):
        path = "db/User.sqlite"
        conn = sqlite3.connect(path)
        sql_delete = '''
        DELETE FROM
            Todo
        WHERE
            id=?
        '''
        # 注意, execute 的第二个参数是一个 tuple
        # tuple 只有一个元素的时候必须是这样的写法
        conn.execute(sql_delete, (self.id,))
        conn.commit()
        conn.close()


    def update(self):
        path = "db/User.sqlite"
        conn = sqlite3.connect(path)
        sql_update = '''
        UPDATE
            `Todo`
        SET
            `title`=?
        WHERE
            `id`=?
        '''
        conn.execute(sql_update, (self.title, self.id))
        conn.commit()
        conn.close()
