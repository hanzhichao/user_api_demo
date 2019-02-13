# 接口Demo
>卡卡制作，接口测试练习使用 微信: lockingfree
## 包含接口
> 接口文档请查看[doc/api.html](./doc/api.md)

- 加法&减法接口
    - 加法接口(Flask搭建接口练习)
    - 减法接口(Flask搭建REST接口练习)
- User模块各种接口Demo
    - 注册接口(REST类接口测试练习)
    - 登录接口(表单类接口测试练习)
    - 登出接口(Session依赖接口测试练习)
    - 上传用户文件接口(上传文件接口测试练习)
    - 获取所有用户信息接口(Session依赖接口测试练习)
    - 更新用户信息接口(Token依赖接口测试练习)
    - 获取token接口(Token依赖接口测试练习)
    - 删除用户接口(数字签名接口测试练习)
- RPC接口练习
    - SOAP接口(SOAP接口测试练习)
    - XML-RPC接口(XML-RPC接口测试练习)

## 使用方法
> 使用Python3+
### 安装依赖
```
pip install flask flask-session mysqlclient pymysql redis spyne
```
### 启动接口
1. 启动rest接口
```
python src/rest_user_api.py 
```
2. 启动soap接口
```
python src/soap_user_api.py 
```
3. 启动xml-rpc接口
```
python src/xmlrpc_user_api.py 
```

### 使用mysql
> 默认使用data/user_data.json本地文件存储用户数据

1. 本地搭建MySQL,新建数据库及user表
```
create database if not exists api;
use api;
create table user(
  id  int primary key auto_increment,
  name  varchar(50), 
  passwd varchar(100) 
);
```

2. 修改src/db.conf
```
[DEFAULT]
mysql = on
```
3. 修改src/db.conf, DB段配置为自己数据的配置
4. 重启接口

### 使用Redis
> 默认session存储与内存中, 练习redis断言可以开启

1. 本地搭建并启动Redis Server
2. 修改conf/db.conf中redis=on,及REDIS段为自己redis的配置
3. 重启接口

### 跨域请求
1. pip install flask_cors
2. 将src/rest_user_api.py 12行及21启用

### 使用Python3测试接口
1. 安装工具包
```
pip install requests suds pytest pytest-html
```
2. 编写用例: 参考test/test_user.py
3. 运行用例
```
pytest -q test/test_user.py --html=report.html
```

## 常见问题
1. 重启接口时端口占用
解决方法: 更改端口src/rest_user_api.py中app.run(port=6000),重新启动
或 lsof -i:5000, 查看进程pid并结束进程,重启接口
2. 加法接口, 测试小数相加报错: 接口bug, 不支持小数相加
3. 返回404, 查看参数名是否正确, name, password, 接口地址后应以"/"结尾
