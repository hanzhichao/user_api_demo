#!/usr/bin/python3
import os
import uuid
import configparser
from functools import wraps

import redis
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import session
from flask import render_template
from flask import make_response
from flask import Response

from flask_session import Session
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Api
from flask_restful import Resource

from sign import checkSign
from sign import md5


# import sys
# sys.path.append("/usr/local/lib/python3.6/site-packages")
# from flask_cors import *

cf = configparser.ConfigParser()
conf_path = os.path.join(os.path.dirname(__file__), "db.conf")
cf.read(os.path.join(os.path.dirname(__file__), "db.conf"))


app = Flask(__name__)
app.secret_key = md5("user")
api = Api(app)
# CORS(app, supports_credentials=True)


if cf.get("DEFAULT", 'redis') == 'on':
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host=cf.get("REDIS", 'redis_server'), port=int(cf.get("REDIS", 'redis_port')))
    Session(app)
    redis_db1 = redis.Redis(host=cf.get("REDIS", 'redis_server'), port=int(cf.get("REDIS", 'redis_port')), db=1)

if cf.get('DEFAULT', 'mysql') == 'on':
    from user_model_mysql import User
else:
    from user_model_json import User


# 表单类加法接口
@app.route("/add/", methods=["GET", "POST"])
def add():
    a = request.values.get("a")
    b = request.values.get("b")
    return str(int(a)+int(b))


# Rest类减法接口
@app.route("/sub/", methods=["POST"])
def sub():
    if not request.json:
        return jsonify({"code": "100001", "msg": "数据格式错误","data": {"result": None}})
    elif "a" not in request.json or "b" not in request.json:
        return jsonify({"code": "100002", "msg": "参数a或b缺失","data": {"result": None}})
    else:
        a=request.json.get("a")
        b=request.json.get("b")
    
    result = float(a) + float(b)
    return jsonify({"code": "100000", "msg": "成功", "data": {"result": result}})


# 01-注册接口，需要参数化
@app.route("/api/user/reg/", methods=["POST"])
def reg():
    # 参数验证
    if not request.json:
        code = '100003'
        msg = '请求数据格式错误(非JSON格式)'
        return jsonify({"code": code, "msg": msg, "data": {}})

    if 'name' not in request.json:
        code = '100004'
        msg = 'name参数缺失'
        return jsonify({"code": code, "msg": msg, "data": {}})

    if 'password' not in request.json:
        code = '100004'
        msg = 'password参数缺失'
        return jsonify({"code": code, "msg": msg, "data": {}})

    name = request.json.get('name')
    password = request.json.get('password')
    u = User()
    status = u.addUser(name, password)
    if status is True:
        code = '100000'
        msg = '成功'
        session_id = str(uuid.uuid1())
        session['session_id'] = True
        response = make_response(jsonify({"code": code, "msg": msg, "data": {"name": name, "password": md5(password)}}))
        response.set_cookie('SESSION_ID', session_id, expires=120)
        return response
    elif status == -1:
        code = '100001'
        msg = '失败，用户已存在'
    else:
        code = '100002'
        msg = '失败，添加用户失败'
    return jsonify({"code": code, "msg": msg, "data": {"name": name, "password": md5(password)}})


# 02-登录接口
@app.route("/api/user/login/", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if not request.form:
        return '<h1>请求数据为空</h1>'
    if 'name' not in request.form:
        return '<h1>name参数缺失</h1>'

    if 'password' not in request.form:
        return '<h1>password参数缺失</h1>'

    name = request.values.get('name')
    password = request.values.get('password')
    u = User()
    status = u.checkUser(name, password)
    if status is True:
        session_id = str(uuid.uuid1())
        session[session_id] = True
        if app.config.get('SESSION_REDIS'):
            redis_db1.set(name, "logined")
        response = make_response('<h1>登录成功</h1>')
        response.set_cookie('PYSESSID', session_id)
        return response
    elif status is None:
        return '<h1>失败，用户不存在</h1>'
    else:
        return '<h1>失败，用户名或密码错误</h1>'


# 03-登出接口
@app.route("/api/user/logout/", methods=["GET"])
def logout():
    name = request.values.get("name")
    session_id = request.cookies.get('PYSESSID')
    if session_id in session:
        session.pop(session_id)
        # redis_db1.delete(name)
    return '<h1>退出登录成功</h1>'


# 04-上传用文件接口
@app.route("/api/user/uploadImage/", methods=['GET', 'POST'])
def uploadImage():
    if request.method == 'POST':
        img = request.files.get('file')
        if not img:
            return '<h1>上传文件失败</h1>'
        else:
            img_name = img.filename
            img.save(os.path.join(os.path.dirname(__file__), 'uploads', img_name))
            return '<h1>上传成功</h1>'
    session_id = request.cookies.get('SESSION_ID')
    if not session_id in session:
        return '<h1>失败，尚未登录</h1>'
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>上传图片</h1>
    <form action="." method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


# 05-获取所有用户信息接口
@app.route("/api/user/getUserList/", methods=["GET"])
def getUserList():
    session_id = request.cookies.get('PYSESSID')
    if not session_id in session:
        return '<h1>失败，尚未登录</h1>'
    else:
        u = User()
        data = u.getAll()
        TEMPLATE_MAIN = '''
            <html><body>
            <h1>用户列表</h1>
            <table border=1>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>用户名</th>
                        <th>密码</th>
                    </tr>
                </thead>
                <tbody>
                    {template_tr}
                </tbody>
            </body></html>
                    '''
        TEMPLATE_TR = '''
                <tr>
                <td>{id}</td>
                <td>{name}</td>
                <td>{password}</td>
                </tr>'''
        template_tr = ''
        for user in data:
            template_tr += TEMPLATE_TR.format(id=user.get('id'), name=user.get('name'), password=user.get('password'))
        return TEMPLATE_MAIN.format(template_tr=template_tr)


# 06-获取token接口
@app.route("/api/user/getToken/", methods=['GET'])
def getToken():
    appid = request.values.get('appid')
    if not appid or appid != '136425':
        return '<h1>appid错误</h1>'
    token = str(uuid.uuid1()).replace("-", "").lower()
    return 'token=' + token


# 06-更新用户信息接口
@app.route("/api/user/updateUser/", methods=['POST'])
def updateUser():
    # 参数验证
    if not request.json:
        code = '100003'
        msg = '请求数据格式错误(非JSON格式)'
        return jsonify({"code": code, "msg": msg, "data": {}})

    if 'name' not in request.json:
        code = '100004'
        msg = 'name参数缺失'
        return jsonify({"code": code, "msg": msg, "data": {}})

    if 'password' not in request.json:
        code = '100004'
        msg = 'password参数缺失'
        return jsonify({"code": code, "msg": msg, "data": {}})

    token = request.values.get('token')
    if not token or len(token) != 32:
        return jsonify({"code": '100007', "msg": '鉴权失败', "data": None})
    else:
        u = User()
        name = request.json.get('name')
        password = request.json.get('password')
        if u.updateUser(name, password):
            code = '100000'
            msg = '成功'
        else:
            code = '100007'
            msg = '更新用户信息失败'
        return jsonify({"code": code, "msg": msg, "data": {"name": name, "passwod": md5(password)}})          


# 07-带签名接口
@app.route("/api/user/delUser/", methods=['POST'])
def detUser():
    # 参数验证
    if not request.json:
        code = '100003'
        msg = '请求数据格式错误(非JSON格式)'
        return jsonify({"code": code, "msg": msg, "data": {}})

    if 'name' not in request.json:
        code = '100004'
        msg = 'name参数缺失'
        return jsonify({"code": code, "msg": msg, "data": {}})

    elif 'sign' not in request.json or not checkSign(request.json):
        return jsonify({"code": '100007', "msg": '鉴权失败', "data": None})
    else:
        name = request.json.get('name')
        u = User()
        result = u.delUser(name)
        if result:
            return jsonify({"code": '100000', "msg": '成功', "data": {"name": name}})
        elif result is None:
            return jsonify({"code": '100003', "msg": '失败，用户不存在', "data": {"name": name}})
        else:
            return jsonify({"code": '100008', "msg": '失败，删除用户失败', "data": {"name": name}})

# 08-各种请求方法
TODOS = {
    'todo1': {'task': '打开冰箱门'},
    'todo2': {'task': '把大象放进冰箱'},
    'todo3': {'task': '关闭冰箱门'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="任务 {} 不存在".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


# Todo
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


# 授权接口
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response("授权失败", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/api/user/login2/', methods=["GET", "POST"])
@requires_auth
def login2():
    return "<h1>登录成功</h1>"


if __name__ == '__main__':
    app.run(port=5000)
