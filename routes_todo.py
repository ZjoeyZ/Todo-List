from utils import log
from models.user import User
from models.todo import Todo
from routes import session


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
    log("cookies", request.cookies)
    session_id = request.cookies.get('user')
    log('route todo session_id and session', session_id, session)
    u_id = session.get(session_id, -1)
    if u_id == -1:
        return redirect('login')
    headers = {
        'Content-Type': 'text/html',
    }
    # 得到所有的todo
    todo_list = Todo.all()
    todos = []
    i = 1
    # 注入属于用户的todo
    for t in todo_list:
        if t.id == u_id:
            delete_href = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
            edit_href = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
            s = '<h3>{} : {}  {}  {}</h3>'.format(i, t.title, delete_href, edit_href)
            i = i + 1
            todos.append(s)
    todo_html = ''.join(todos)
    # 替换模板文件中的标记字符串
    body = template('todo.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_edit_todo(request):
    """
     编辑todo的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    # 替换模板文件中的标记字符串
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', t.title)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_add_todo(request):
    """
    增加一个todo的处理函数
    """
    # 得到用户信息
    session_id = request.cookies.get('user')
    u_id = session.get(session_id, -1)
    if u_id == -1:
        return redirect('login')
    form = request.form()
    todo = Todo.new(form)
    # 增加user_id
    todo.user_id = u_id
    todo.save()
    return redirect('/todo')


def route_update_todo(request):
    """
    删除一个todo的处理函数
    """
    # 得到用户信息
    session_id = request.cookies.get('user')
    log('route todo session_id and session', session_id, session)
    u_id = session.get(session_id, -1)
    # 得到todo对象
    form = request.form()
    todo_id = int(form.get('id', None))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u_id:
        return redirect('/todo')
    t.title = form.get('title', '')
    t.save()
    return redirect('/todo')


def route_delete_todo(request):
    """
    删除一个todo的处理函数
    """
    # 得到todo对象
    todo_id = int(request.query.get('id', None))
    t = Todo.find_by(id=todo_id)
    # 删除
    if t is not None:
        t.remove()
    return redirect('/todo')


route_todo_dict = {
    '/todo': route_todo,
    '/todo/add': route_add_todo,
    '/todo/delete': route_delete_todo,
    '/todo/edit': route_edit_todo,
    "/todo/update": route_update_todo,
}
