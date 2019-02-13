import json
import configparser
import pymysql
from sign import md5
import os


class User(object):
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read(os.path.join(os.path.dirname(__file__), "db.conf"), encoding="utf-8")

        self.conn = pymysql.connect(host=cf.get('DB', 'db_host'),
                               port=int(cf.get('DB', 'db_port')),
                               user=cf.get('DB', 'db_user'),
                               password=cf.get('DB', 'db_password'),
                               db=cf.get('DB', 'db_name'),
                               charset='utf8')

        self.cur = self.conn.cursor()
        
    def __del__(self):
        self.cur.close()
        self.conn.close()

    def getAll(self):
        self.cur.execute("select * from user")
        result = []
        for item in self.cur.fetchall():
            result.append(dict(zip(('id', 'name', 'password'), item)))
        return result

    def getUserById(self, id):
        self.cur.execute("select * from user where id=%d" % int(id))
        result = self.cur.fetchone()
        if result:
            return dict(zip(('id', 'name', 'password'), result))
        else:
            return None


    def getUserByName(self, name):
        self.cur.execute("select * from user where name='%s'" % name)
        result = self.cur.fetchone()
        if result:
            return dict(zip(('id', 'name', 'password'), result))
        else:
            return None

    def checkUser(self, name, password):
        if self.getUserByName(name):
            return True if md5(password) == self.getUserByName(name).get('password') else False
        else:
            return None

    def addUser(self, name, password): 
        if self.getUserByName(name):
            return -1
        else:
            self.cur.execute("insert into user (name, password) values ('%s', '%s')" % (name, md5(password)))
            self.conn.commit()
            return self.checkUser(name, password)

    def modifyUser(self, name, password): 
        if not self.getUserByName(name):
            return -1
        else:
            self.cur.execute("update user set name='%s', password='%s' where name='%s'" % (name, md5(password),name))
            self.conn.commit()
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
            self.cur.execute("delete from user where name='%s'" % name)
            self.conn.commit()
            return False if self.getUserByName(name) else True


if __name__ == '__main__':
    u = User()
    print(u.getAll())
    # print(u.getUserById(1))
    # print(u.getUserByName("张三"))
    # print(md5('123456'))
    # print(u.checkUser("张三", '123456'))
    # print(u.addUser("李四", '123456'))
    # print(u.modifyUser("李四", '123456'))
    # print(u.delUser("李四"))
