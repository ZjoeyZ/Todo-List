import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict
from routes_todo import route_todo_dict



# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def form(self):
        args = self.body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            # 特殊符号转码
            v = urllib.parse.unquote(v)
            k = urllib.parse.unquote(k)
            f[k] = v
        return f

    def add_headers(self, header):
        """
        传入的header参数如下所示
        [
            'Accept-Language: xxxxxx'
            'Cookie: x=xx; xx=xxx'
        ]
        解析得到字典
        """
        # 清楚上次得到的headers
        self.headers = {}
        lines = header
        for line in lines:
            k, v = line.split(': ', 1)
            self.headers[k] = v
        log('headers', self.headers)
        # 清除 上次的cookies
        self.cookies = {}
        # 加入新cookie
        self.add_cookies()

    def add_cookies(self):
        """
        把headers里的cookies字段取出来
        生成一个字典，｛string：string｝
        加入request对象，
        """
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v
        log('cookies', self.cookies)


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def parsed_path(path):
    """
    把 path 和 query 分离,并解析query
    message=xx&author=xxx
    {
        'message': 'xx',
        'author': 'xxx',
    }
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    r = {
        '/static': route_static,
        # '/': route_index,
        # '/login': route_login,
        # '/messages': route_message,
    }
    r.update(route_dict)
    r.update(route_todo_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=3000):
    """
    启动服务器
    """
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            buffer_size = 1024
            r = b''
            while True:
                request_b = connection.recv(buffer_size)
                r += request_b
                if len(request_b) < buffer_size:
                    break
            r = r.decode('utf-8')
            log('原始请求\r\n', r)
            # 空请求导致 split 得到空 list,判断一下防止程序崩溃
            if len(r.split()) < 2:
                log("空请求", r.split())
                continue
            path = r.split()[1]
            # 设置 request 的 method
            request.method = r.split()[0]
            # 把 body 放入 request 中
            request.body = r.split('\r\n\r\n', 1)[1]
             # 用add_headers函数来得到headers和cookies
            request.add_headers(r.split('\r\n\r\n', 1)[0].split('\r\n')[1:])
            # 用 response_for_path 函数来得到 path 对应的响应内容
            response = response_for_path(path)
            # 把响应发送给客户端
            log("going to send")
            connection.sendall(response)
            log("send successfully")
            # 处理完请求, 关闭连接
            connection.close()
            log("close successfully\r\n\r\n")


request = Request()

if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
