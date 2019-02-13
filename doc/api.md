[TOC]
# 接口Demo
## 加法&减法接口
### 加法接口
    
**简要描述：** 

加法接口(Flask搭建接口练习)

**请求URL：** 
` http://127.0.0.1:5000/add/`
  
**请求方式：**
GET, POST 

**请求类型：**
URL/FORM

**请求示例**
``` 
http://127.0.0.1:5000/add/?a=3&b=5
```
或
```
http://127.0.0.1:5000/add/

data = "?a=3&b=5"
```

**参数**

|参数名   |必选|类型  |说明   |
|:--------|:---|:-----|-------|
|a     |是  |Integer&String|整数或整数的字符串格式 |
|b   |是  |Integer&String|整数或整数的字符串格式   |


 **返回示例**
成功：
``` 
'8'
```

### 减法接口
    
**简要描述：** 

减法(Flask搭建REST类接口练习)

**请求URL：** 
` http://127.0.0.1:5000/sub/`
  
**请求方式：**
POST 

**请求类型：**
JSON

**请求示例**
``` 
{
    "a": 5.2,
    "b": 1.1
}
```

**参数**

|参数名   |必选|类型  |说明   |
|:--------|:---|:-----|-------|
|a     |是  |Float&String|浮点型或数字的支付串形式 |
|b   |是  |Float&String|浮点型或数字的支付串形式 |


 **返回示例**
成功：
``` 
{
  "code": "100000",
  "msg": "成功",
  "data": {
    "result": 4.1
  }
}
```
数据格式错误(非json格式请求)：
```
{
  "code": "100001",
  "msg": "数据格式错误",
  "data": {
    "result": null
  }
}
```
参数a或b缺失：
```
{
  "code": "100002",
  "msg": "参数a或b缺失",
  "data": {
   "result": null
  }
}
```
 **返回参数说明** 

|参数  |类型  |说明                                      |
|:-----|------|------------------------------------------|
|code  |String|接口返回状态码                            |
|msg   |String|接口信息                                  |
|data  |Object|返回数据|


 **状态码**

|Code  |说明        |
|:-----|------------|
|100000|成功    |
|100001|数据格式错误  |
|100002|参数a或b缺失|

## User模块各种接口Demo

### 注册接口
    
**简要描述：** 

注册接口(POST,REST接口练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/reg/`
  
**请求方式：**
POST 

**请求类型：**
JSON

**请求示例**
``` 
{
    "name": "李六",
    "password": "123456"
}
```

**参数**

|参数名   |必选|类型  |说明   |
|:--------|:---|:-----|-------|
|name     |是  |string|用户名 |
|password   |是  |string|密码   |


 **返回示例**
成功：
``` 
{
  "code": "100000",
  "msg": "成功",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```
用户已存在：
```
{
  "code": "100001",
  "msg": "失败，用户已存在",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```
添加用户失败：
```
{
  "code": "100002",
  "msg": "失败，添加用户失败",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```
 **返回参数说明** 

|参数  |类型  |说明                                      |
|:-----|------|------------------------------------------|
|code  |String|接口返回状态码                            |
|msg   |String|接口信息                                  |
|data  |Object|返回数据,包含请求的用户名和md5加密后的密码|


 **状态码**

|Code  |说明        |
|:-----|------------|
|100000|成功    |
|100001|失败，用户已存在  |
|100002|失败，添加用户失败|


### 登录接口
    
**简要描述：** 

登录接口(POST表单接口练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/login/`
  
**请求方式：**
POST 

**请求类型：**
FORM

**请求示例**

|参数名   |参数值|
|:--------|:-----|
|name     |张三  |
|password   |123456|

**参数**

|参数名   |必选|类型  |说明   |
|:--------|:---|:-----|-------|
|name     |是  |string|用户名 |
|password   |是  |string|密码   |


 **返回示例**
成功：

登录成功

失败：

失败，用户不存在

失败，用户名或密码错误

### 登出接口
    
**简要描述：** 

登出示例(GET请求练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/logout/?name=张三`
  
**请求方式：**
GET 

**参数**

|参数名|参数值|
|:---|:---|
|name|张三|


 **返回示例**
成功：

退出登录成功

### 上传用户文件接口
    
**简要描述：** 

用于上传用户文件(上传接口文件练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/uploadImage/`
  
**请求方式：**
- GET 显示上传页面
- POST 上传文件

**文件**
图片文件


 **返回示例**
成功：

上传成功

失败：

上传文件失败

**备注**
- GET请求需要登录
- 上传的图片会放在uploads文件夹下


### 获取所有用户信息接口
    
**简要描述：** 

获取所有用户姓名和密码(需要登录接口练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/getUserList/`
  
**请求方式：**
GET

**参数**
无

 **返回示例**
成功：

|ID    |用户名|密码                            |
|:-----|------|--------------------------------|
|1     |张三  |e10adc3949ba59abbe56e057f20f883e|
|2     |李四  |7235ce1a737d16c95a51e3f9efabaea5|
|3     |王五  |e10adc3949ba59abbe56e057f20f883e|

失败：

失败，尚未登录

**备注**
需要登录获取session或登录一次后携带cookies


### 更新用户信息接口
    
**简要描述：** 

用于修改用户信息或新建用户(带token接口练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/updateUser/?token=****`
  
**请求方式：**
POST 

**请求类型：**
JSON

**请求示例**
http://127.0.0.1:5000/api/user/updateUser/?token=b3f80a264a3d11e8956b54ee75704366
``` 
{
    "name": "李六",
    "password": "123456"
}
```

**参数**

|参数名   |必选|类型  |说明   |
|:--------|:---|:-----|-------|
|token    |是  |string|用户token, 从getToken接口获取|
|name     |是  |string|用户名 |
|password   |是  |string|密码   |


 **返回示例**
成功：
``` 
{
  "code": "100000",
  "msg": "成功",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```
失败：
```
{
  "code": "100001",
  "msg": "更新用户信息失败",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```
 **返回参数说明** 

|参数  |类型  |说明                                      |
|:-----|------|------------------------------------------|
|code  |String|接口返回状态码                            |
|msg   |String|接口信息                                  |
|data  |Object|返回数据,包含请求的用户名和md5加密后的密码|


 **状态码**

|Code  |说明        |
|:-----|------------|
|100000|成功        |
|100007|更新用户信息失败|

**备注**
需要携带token

### 获取token接口
    
**简要描述：** 

通过appid获取token(带token接口练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/getToken/?appid=136425`
  
**请求方式：**
GET 

**参数**

|参数名   |必选|类型  |说明   |
|:--------|:---|:-----|-------|
|appid    |是  |String|校验id |


 **返回示例**
成功：

token=b3f80a264a3d11e8956b54ee75704366

失败：

appid错误

**备注**
appid使用136425

### 删除用户接口
    
**简要描述：** 

删除用户接口(带签名接口练习)

**请求URL：** 
` http://127.0.0.1:5000/api/user/reg/`
  
**请求方式：**
DELETE

**请求类型：**
JSON

**请求示例**
``` 
{
    "name": "李六",
    "password": "123456",
    "sign": "c25d81703228310dfab5e429b05053a6"
}
```

**参数**

|参数名   |必选|类型  |说明   |
|:--------|:---|:-----|-------|
|name     |是  |string|用户名 |
|password   |是  |string|密码   |
|sign     |是  |string|签名,详见备注|


 **返回示例**
成功：
``` 
{
  "code": "100000",
  "msg": "成功",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```
失败：
```
{
  "code": "100003",
  "msg": "失败，用户不存在",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```

```
{
  "code": "100008",
  "msg": "失败，删除用户失败",
  "data": {
    "name": "李六",
    "password": "e10adc3949ba59abbe56e057f20f883e"
  }
}
```
 **返回参数说明** 

|参数  |类型  |说明                                      |
|:-----|------|------------------------------------------|
|code  |String|接口返回状态码                            |
|msg   |String|接口信息                                  |
|data  |Object|返回数据,包含请求的用户名和md5加密后的密码|


 **状态码**

|Code  |说明        |
|:-----|------------|
|100000|成功    |
|100003|失败，用户不存在  |
|100008|失败，删除用户失败|

**备注**
需要携带签名

>appsecret使用NTA3ZTU2ZWM5ZmVkYTVmMDBkMDM3YTBi

签名加密方法：

1. 将字典类型的请求参数，按键值的字母排序，然后拼接为key1=value1&key2=value2&...的字符串
2. 将拼接的字符串末尾拼接appsecret=NTA3ZTU2ZWM5ZmVkYTVmMDBkMDM3YTBi，然后进行md5加密
3. 将加密后的签名放到请求参数的'sign'字段中

如原始数据：
```
{
    "name": "李六",
    "password": "123456"
}
```
- 排序并拼接为 name=李六&password=e10adc3949ba59abbe56e057f20f883e&appsecret=NTA3ZTU2ZWM5ZmVkYTVmMDBkMDM3YTBi
- 进行md5加密为得到：e212dcad0878a9ea061bd1cc6c2e6fe2
- 为请求参数添加签名字段sign得到
```
{
    "name": "李六",
    "password": "123456"
    "sign": "c25d81703228310dfab5e429b05053a6"
}
```
## RPC接口练习
### SOAP接口

**简要描述：** 

用户操作(SOAP接口接口练习)

**请求URL：** 
` http://127.0.0.1:5001/?wsdl`
  
**请求方式：**
WebService(SOAP)

**请求类型：**
XML

**接口对象实例方法**

- getAll()
- getUserById(id)
- getUserByName(name)
- checkUser(name, password)
- addUser(name, password)
- modifyUser(name, password)
- delUser(name)

### XML-RPC接口

**简要描述：** 

用户操作(XML-RPC接口练习)

**请求URL：** 
` http://127.0.0.1:5002`
  
**请求方式：**
XML-RPC

**请求类型：**
XML

**接口对象实例方法**

- getAll()
- getUserById(id)
- getUserByName(name)
- checkUser(name, password)
- addUser(name, password)
- modifyUser(name, password)
- delUser(name)