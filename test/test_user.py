import requests
import pytest
import json
from db2 import DB2
import hashlib
import re


def md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf8'))
    return m.hexdigest()

def makeSign(data):
    sign=''
    for key in sorted(data.keys()):
        sign += key + '=' + str(data[key]) + '&'
    sign += 'appsecret=NTA3ZTU2ZWM5ZmVkYTVmMDBkMDM3YTBi'
    data['sign'] = md5(sign)
    return data

class TestUser(): # pytest识别不能用__init__方法
    base_url = 'http://127.0.0.1:5000'
    db = DB()

    def test_login(self):
        url = self.base_url + '/api/user/login/'
        data = {"name": "张三", "password": "123456"}
        resp = requests.post(url=url, data=data)

        #断言
        assert resp.status_code == 200
        assert '登录成功' in resp.text

    def test_reg(self):
        url = self.base_url + '/api/user/reg/'
        headers = {"Content-Type": "application/json"}
        data = {'name': '张10', 'password': '123456'}
        resp = requests.post(url=url, headers=headers, data=json.dumps(data))

        #断言
        assert resp.json()['code'] == '100000'
        assert resp.json()['msg'] == '成功'
        assert self.db.getUserByName('张10') is not None


    def test_uploadImage(self):
        url = self.base_url + '/api/user/uploadImage/'
        files = {'file': open("复习.txt")}
        resp = requests.post(url=url, files=files)

        #断言
        assert resp.status_code == 200
        assert '成功' in resp.text
        # todo 服务器断言

    def test_getUserList(self):
        session = requests.session()
        login_url = self.base_url + '/api/user/login/'
        login_data = {"name": "张三", "password": "123456"}
        session.post(url=login_url, data=login_data)

        url = self.base_url + '/api/user/getUserList/'
        resp = session.get(url=url)

        #断言
        assert resp.status_code == 200
        assert '用户列表' in resp.text
        assert re.findall('\w{32}',t2) is not None

    def test_updateUser(self):
        session = requests.session()  # 接口依赖的接口需要用session
        get_token_url = self.base_url + '/api/user/getToken/'
        params = {"appid": '136425'}
        token_resp = session.get(url=get_token_url, params=params)
        assert re.findall('token=\w{32}$') is not None
        token = token_resp.text.split('=')[1]

        url = self.base_url + '/api/user/updateUser/?token=' + token
        data = {'name': '张三', 'password': '234567'}
        headers = {"Content-Type": "application/json"}
        resp = session.post(url=url, headers=headers, data=json.dumps(data))

        #断言
        assert resp.status_code == 200
        assert resp.json()['code'] == '100000'
        assert resp.json()['msg'] == '成功'
        assert self.db.checkUser('张三', '234567')

    def test_delUser(self):
        url = self.base_url + '/api/user/delUser/'
        headers = {"Content-Type": "application/json"}
        data = {'name': '张10', 'password': '123456'}
        data = makeSign(data)
        resp = requests.post(url=url, headers=headers, data=json.dumps(data))

        #断言
        assert resp.status_code == 200
        assert resp.json()['code'] == '100000'
        assert resp.json()['msg'] == '成功' 
        # assert self.db.getUserByName('张10') is None


if __name__ == '__main__':
    t = TestUser()
    # t.test_updateUser()
    # t.test_updateUser()
    t.test_delUser()
    # pytest.main("-q test_user2.py")
