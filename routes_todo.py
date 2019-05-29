from models.user import User
from models.todo import Todo
from routes import get_uid
from utils import *



def route_todo(request):
    """
    todo_list 首页的路由函数
    """
    u_id = get_uid(request)
    if u_id == -1:
        return redirect('login')
    headers = {
        'Content-Type': 'text/html',
    }
    # 得到所有的todo
    todos = Todo.all()
    # 注入属于用户的todo
    body = template('todo.html', todos=todos)
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
    body = template('todo_edit.html', todo=t)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_add_todo(request):
    """
    增加一个todo的处理函数
    """
    # 得到用户信息
    u_id = get_uid(request)
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
    u_id = get_uid(request)
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
