from utils import log, template, salted_password
from models.user import User
import random




session = {}

def get_uid(request):
    session_id = request.cookies.get('user', '')
    u_id = session.get(session_id, -1)
    return u_id

def random_str():
    '''生成一个随机字符串'''
    seed = '1234567890qwertyuiopasdfghjkl'
    session_id = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 1)
        session_id += seed[random_index]
    return session_id


def route_login(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n{}\r\n'
    if request.method == 'POST':
        # 生成对象，验证对象
        form = request.form()
        u = User.new(form)
        if u.exist():
            u = u.find_by(username=u.username)
            #  生成session，与用户名称建立联系
            session_id = random_str()
            session[session_id] = u.id
            # 在要返回的headers字段里增加set-cookie字段，加入session
            set_cookie = 'Set-Cookie: user={}'.format(session_id)
            header = header.replace('{}', set_cookie)
            result = '登录成功   <a href="/todo">todo list</a>'
            log('set cookie headers', header)
        else:
            result = '用户名或者密码错误'
    else:
        result = '请登录'
    body = template('login.html', result=result)
    r = header + '\r\n' + body
    log('login 的响应', r)
    return r.encode(encoding='utf-8')


def route_register(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User.new(form)
        u.password = salted_password(u.password)
        if u.validate_register():
            u.save()
            result = '注册成功<br><a href="/login">请登录</a>'
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html', result=result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
}
