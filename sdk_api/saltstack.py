#!/usr/bin/env python
# -*-coding:utf-8-*-
import urllib
import urllib.parse
import urllib.request
import ssl
import json
from devops.settings import SaltStackApi

#: 解决saltstack api ssh连接报错
context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context


class SaltAPI(object):
    __token_id = ''

    #: 类变量定义
    def __init__(self):
        self.__url = SaltStackApi['url']
        self.__user = SaltStackApi['user']
        self.__password = SaltStackApi['password']

    #: 获取请求成功参数token值
    def token_id(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode_params = urllib.parse.urlencode(params).encode(encoding='utf-8')
        content = self.post_request(encode_params, prefix='/login')
        self.__token_id = content['return'][0]['token']

    #: 使用post请求，配置请求参数
    def post_request(self, params, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, params, headers=headers)
        data = urllib.request.urlopen(req).read().decode("utf-8")
        content = json.loads(data)
        return content

    #: 获取各主机信息
    def salt_command(self, tgt, fun, arg=None):
        self.token_id()
        params = {'client': 'local'}
        try:
            if tgt and fun:
                if type(tgt) == list:
                    params['expr_form'] = 'list'
                    params['tgt'] = ','.join(tgt)
                else:
                    params['tgt'] = tgt
                params['fun'] = fun
            else:
                raise Exception("salt语法有误,请检查!")
            if arg:
                params['arg'] = arg
            encode_params = urllib.parse.urlencode(params).encode(encoding='utf-8')
            content = self.post_request(encode_params)
            return content
        except Exception as e:
            return str(e)