from spyne import Application, rpc, ServiceBase
from spyne import Integer, Unicode, Array, ComplexModel, Iterable
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from wsgiref.simple_server import make_server
import sys
import json
from sign import md5
import os

DB_FILE = os.path.join(os.path.dirname(__file__), 'user_data.json')


class UserService(ServiceBase):
    global data
    with open(DB_FILE, encoding='utf-8') as f:
        data = json.load(f)

    @rpc(_returns=Iterable(Unicode))
    def getAll(self):
        global data
        for user in data:
            yield str(user['id']) + ', ' + user['name'] + ', ' + user['password']
    
    @rpc(Integer, _returns=Iterable(Unicode))
    def getUserById(self, id):
        global data
        users = list(filter(lambda user: user.get('id') == id, data))
        for user in users:
            yield str(user['id']) + ', ' + user['name'] + ', ' + user['password']

    @rpc(Unicode, _returns=Iterable(Unicode))
    def getUserByName(self, name):
        global data
        users = list(filter(lambda user: user.get('name') == name, data))
        for user in users:
            yield str(user['id']) + ', ' + user['name'] + ', ' + user['password']

    @rpc(Unicode, Unicode, _returns=Unicode)
    def checkUser(self, name, password):
        global data
        user = list(filter(lambda user: user.get('name') == name, data))
        if user:
            return '验证成功' if md5(password) == user[0].get('password') else '用户名或密码错误'
        else:
            return '用户不存在'

    @rpc(Unicode, Unicode, _returns=Unicode)
    def addUser(self, name, password): 
        global data
        user = list(filter(lambda user: user.get('name') == name, data))
        if user:
            return '用户已存在'
        else:
            id = int(data[-1].get('id')) + 1
            data.append({"id": id, "name": name, "password": md5(password)})
            with open(DB_FILE, 'w') as f:
                json.dump(data, f)
            with open(DB_FILE, encoding='utf-8') as f:
                data = json.load(f)
            user = list(filter(lambda user: user.get('name') == name, data))
            if user:
                return '添加成功' if md5(password) == user[0].get('password') else '添加失败，密码错误'
            else:
                return '添加失败，用户不存在'

    @rpc(Unicode, Unicode, _returns=Unicode)
    def modifyUser(self, name, password): 
        global data
        user = list(filter(lambda user: user.get('name') == name, data))
        if not user:
            return '用户不存在'
        else:
            id = int(data[-1].get('id')) + 1
            user[0].update({"id": id, "name": name, "password": md5(password)})
            with open(DB_FILE, 'w') as f:
                json.dump(data, f)
            with open(DB_FILE, encoding='utf-8') as f:
                data = json.load(f)
            user = list(filter(lambda user: user.get('name') == name, data))
            if user:
                return '修改成功' if md5(password) == user[0].get('password') else '修改失败，密码错误'
            else:
                return '修改失败，用户不存在'


    @rpc(Unicode, _returns=Unicode)
    def delUser(self, name): 
        global data
        user = list(filter(lambda user: user.get('name') == name, data))
        if not user:
            return '用户不存在'
        else:
            data.pop(data.index(user[0]))
            with open(DB_FILE, 'w') as f:
                json.dump(data, f)
            with open(DB_FILE, encoding='utf-8') as f:
                data = json.load(f)
            user = list(filter(lambda user: user.get('name') == name, data))
            if not user:
                return '删除成功'
            else:
                return '删除失败'



if __name__ == '__main__':
    soap_app = Application([UserService], 'UserService', in_protocol=Soap11(validator="lxml"), out_protocol=Soap11())
    wsgi_app = WsgiApplication(soap_app)
    server = make_server('127.0.0.1', 5001, wsgi_app)
    sys.exit(server.serve_forever())
