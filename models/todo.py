from models import Model


# 定义一个 class 用于保存 Todo
class Todo(Model):
    def __init__(self, form):
        self.title = form.get('title', '')
        self.id = int(form.get('id', -1))
