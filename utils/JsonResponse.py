#!/usr/bin python
# _*_ coding:utf-8 _*_
from django.forms.models import model_to_dict
import json
from utils.DateEncoder import DateEncoder


#: orm对象转换
def OrmConversion(params):
    if type(params) is list:
        data_list = []
        for param in params:
            data_list.append(model_to_dict(param))
        return data_list
    else:
        data = model_to_dict(params)
        return data


#: api返回json格式标准
class JsonResponse(object):
    def __init__(self, code, message=None, data=None):
        self.code = code
        self.message = message
        self.data = data


    def getJson(self):
        responseData = {
            'code': self.code,
            'message': self.message,
            'data': self.data,
        }
        try:
            return json.dumps(responseData, cls=DateEncoder, ensure_ascii=False).encode('utf-8')
        except Exception as e:
            return json.dumps(responseData, cls=DateEncoder).encode('utf-8')



