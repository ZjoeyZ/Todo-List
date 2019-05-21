from utils import log
from models.user import User
from models.todo import Todo


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def redirect(path):
    headers = {
        'Location': path,
    }
    return response_with_headers(headers, 302).encode('utf-8')

def template(path):
    path = 'templates/' + path
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


def route_todo(request):
    """
    todo_list 首页的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    #得到所有的todo
    todo_list = Todo.all()
    todos = []
    i = 1
    for t in todo_list:
        delete_href = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{} : {}  {}</h3>'.format(i, t.title, delete_href)
        i = i + 1
        todos.append(s)
    todo_html = ''.join(todos)
    # 替换模板文件中的标记字符串
    body = template('todo.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_add_todo(request):
    """
    增加一个todo的处理函数
    """
    #得到所有的todo
    form = request.form()
    todo = Todo.new(form)
    todo.save()
    return redirect('/todo')


def route_delete_todo(request):
    """
    删除一个todo的处理函数
    """
    #得到todo对象
    todo_id = int(request.query.get('id', None))
    t = Todo.findby(id = todo_id)
    #删除他
    t.remove()
    return redirect('/todo')


route_todo_dict = {
    '/todo': route_todo,
    '/todo/add': route_add_todo,
    '/todo/delete': route_delete_todo,
}
