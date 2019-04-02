from django.shortcuts import HttpResponse
from cmdb.views.dao import apiInfoDao
from utils.JsonResponse import JsonResponse
from utils.JsonResponse import OrmConversion
from utils.UserSession import checkUserSession
import json


#: 作用: 根据apiId查询api信息与权限详情
#: url: apiInfo/getAllFromApiInfoByApiId
#: 参数: apiId
def getAllFromApiInfoByApiId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiId = requset.GET.get('apiId')
        if apiId:
            apiInfo = apiInfoDao.getAllFromApiInfoByApiId(apiId)
            code, data = 200, {'apiInfo': OrmConversion(apiInfo)}
        else:
            raise Exception('参数报错: apiId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加api信息
#: url: apiInfo/setFromApiInfo
#: 参数: apiUrl, apiName, remarks
def setFromApiInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiUrl = requset.GET.get('apiUrl')
        apiName = requset.GET.get('apiName')
        remarks = requset.GET.get('remarks')
        if apiUrl and remarks:
            apiInfoDao.setFromApiInfo(apiUrl, apiName, remarks)
            code, message = 200, '添加完成'
        else:
            raise Exception('参数报错: apiUrl,apiName, remarks  都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据apiId更新api信息
#: url: apiInfo/updAllFromApiInfoByApiId
#: 参数: apiId, apiUrl, apiName, remarks
def updAllFromApiInfoByApiId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiId = requset.GET.get('apiId')
        apiUrl = requset.GET.get('apiUrl')
        apiName = requset.GET.get('apiName')
        remarks = requset.GET.get('remarks')
        if apiId:
            apiInfoDao.updAllFromApiInfoByApiId(apiId, apiUrl=apiUrl, apiName=apiName, remarks=remarks)
            code, message = 200, '更新完成'
        else:
            raise Exception('参数报错: apiId  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据apiId删除指定api信息
#: url: apiInfo/delFromApiInfoByApiId
#: 参数: apiId
def delFromApiInfoByApiId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiId = requset.GET.get('apiId')
        if apiId:
            apiInfoDao.delFromApiInfoByApiId(apiId)
            code, message = 200, '更新完成'
        else:
            raise Exception('参数报错: apiId  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: apiInfo分页查询带模糊查询功能
#: url: apiInfo/getListFromApiInfoByPage
#: 参数: page, apiUrl
def getListFromApiInfoByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        apiUrl = requset.GET.get('apiUrl')
        if page:
            apiInfoList, numPages = apiInfoDao.getListFromApiInfoByPage(page=page, apiUrl=apiUrl)
            code = 200
            data = {
                'apiInfoList': OrmConversion(list(apiInfoList)),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据roleId查询api信息列表
#: url: apiInfo/getAllFromApiInfoByApiId
#: 参数: apiId
def getAllFromApiInfoByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiId = requset.GET.get('apiId')
        if apiId:
            apiInfo = apiInfoDao.getAllFromApiInfoByApiId(apiId)
            code, data = 200, {'apiInfo': OrmConversion(apiInfo)}
        else:
            raise Exception('参数报错: apiId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())