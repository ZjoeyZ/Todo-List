import json
from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是一个序列化/反序列化 list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    # json.dumps 序列化得到json格式字符串
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        # 字符串转字典
        return json.loads(s)


# Model 是用于存储数据的基类
class Model(object):
    # @classmethod 说明这是一个 类方法
    # 类方法的调用方式是  类名.类方法()
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是 class
        # 所以我们可以得到 class 的名字
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Msg(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例 在序列中
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def findby(cls, **kwargs):
        """
        根据kwargs中的参数，找到对象
        """
        k = ''
        v = ''
        for key, value in kwargs.items():
            k, v = key, value
        models = cls.all()
        for m in models:
            if m.__dict__[k] == v:
                return m
            else:
                return None

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        # 如果models为空，则新ID为1
        if len(models) == 0:
            self.id = 1
            models.append(self)
            log('append 0th object', self.__dict__)
        # 如果id = -1 说明之前不存在，赋值新id
        elif self.id == -1:
            self.id = models[-1].id + 1
            models.append(self)
            log('append last object', self.__dict__)
        # 若果id != -1 说明之前存在，找到之前的对象，并替换
        else:
            for index, m in enumerate(models):
                if m.id == self.id:
                    models[index] = self
                    log('replace one object', self.__dict__)
                    break
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def remove(self):
        """
        save 函数用于把一个 Model 的实例从文件中删除
        """
        models = self.all()
        for i, m in enumerate(models):
            if m.id == self.id:
                del models[i]
                break
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        """
        这是一个 魔法函数 返回 string representation of a object
        当调用 str(oject) 的时候
        若没有 __str__
        就调用 __repr__
        """
        # 类名
        classname = self.__class__.__name__
        # 所有的属性和值
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
