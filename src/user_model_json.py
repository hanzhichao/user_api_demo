import json
from sign import md5
import os

class User(object):
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__), 'user_data.json')
        self.load()

    def load(self):
        with open(self.path, encoding='utf-8') as f:
            self.data = json.load(f)

    def getAll(self):
        return self.data

    def getUserById(self, id):
        users = list(filter(lambda user: user.get('id') == id, self.data))
        return users[0] if users else None

    def getUserByName(self, name):
        users = list(filter(lambda user: user.get('name') == name, self.data))
        return users[0] if users else None

    def checkUser(self, name, password):
        if self.getUserByName(name):
            return True if md5(password) == self.getUserByName(name).get('password') else False
        else:
            return None

    def addUser(self, name, password): 
        if self.getUserByName(name):
            return -1
        else:
            id = int(self.data[-1].get('id')) + 1
            self.data.append({"id": id, "name": name, "password": md5(password)})
            with open(self.path, 'w') as f:
                json.dump(self.data, f)
            self.load()
            return self.checkUser(name, password)

    def modifyUser(self, name, password): 
        if not self.getUserByName(name):
            return -1
        else:
            id = int(self.data[-1].get('id')) + 1
            self.getUserByName(name).update({"id": id, "name": name, "password": md5(password)})
            with open(self.path, 'w') as f:
                json.dump(self.data, f)
            self.load()
            return self.checkUser(name, password)

    def updateUser(self, name, password): 
        if self.getUserByName(name):
            return self.modifyUser(name, password)
        else:
            return self.addUser(name, password)

    def delUser(self, name): 
        user = self.getUserByName(name)
        if not user:
            return None
        else:
            self.data.pop(self.data.index(user))
            with open(self.path, 'w') as f:
                json.dump(self.data, f)
            self.load()
            return False if self.getUserByName(name) else True


if __name__ == '__main__':
    u = User("user_data.json")
    print(u.getAll())
    print(u.getUserById(1))
    print(u.getUserByName("张三"))
    print(md5('123456'))
    print(u.checkUser("张三", '123456'))
    print(u.addUser("李四", '234567'))
    print(u.modifyUser("李四", '134567'))