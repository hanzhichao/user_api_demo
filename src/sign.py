import hashlib

appsecret = "NTA3ZTU2ZWM5ZmVkYTVmMDBkMDM3YTBi"

def md5(str):
    m = hashlib.md5()
    m.update(str.encode('utf8'))
    return m.hexdigest()  #返回摘要，作为十六进制数据字符串值


def makeSign(params):
    if not isinstance(params, dict):
        print("参数格式不正确，必须为字典格式")
        return None
    if 'sign' in params:
        params.pop('sign')
    sign = ''
    for key in sorted(params.keys()):
        sign = sign + key + '=' + str(params[key]) + '&'
    sign = md5(sign + 'appsecret=' + appsecret)
    params['sign'] = sign
    return params

def checkSign(params):
    if 'sign' not in params:
        return False
    else:
        sign = params.pop('sign')
        return True if sign == makeSign(params).get('sign') else False



if __name__ == '__main__':

    p = makeSign({"name":"张14","password":"123456"})
    print(p)
    print(md5('name=李六&password=e10adc3949ba59abbe56e057f20f883e&appsecret=NTA3ZTU2ZWM5ZmVkYTVmMDBkMDM3YTBi'))
    print(checkSign(p))
