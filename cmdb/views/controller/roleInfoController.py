from django.shortcuts import HttpResponse
from cmdb.views.dao import roleInfoDao, apiInfoDao, userGroupDao
from utils.JsonResponse import JsonResponse
from utils.JsonResponse import OrmConversion
from utils.UserSession import checkUserSession
import json


#: 作用: 根据roleId查询角色信息
#: url: roleInfo/getAllFromRoleInfoByRoleId
#: 参数: roleId
def getAllFromRoleInfoByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiId = requset.GET.get('roleId')
        if apiId:
            roleInfo = roleInfoDao.getAllFromRoleInfoByRoleId(apiId)
            code = 200
            data = {'roleInfo': OrmConversion(roleInfo)}
        else:
            raise Exception('参数报错: roleId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据roleId查询角色信息与角色权限详情
#: url: roleInfo/getAllFromRoleInfoAndApiInfoByRoleId
#: 参数: roleId
def getAllFromRoleInfoAndApiInfoByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiId = requset.GET.get('roleId')
        if apiId:
            roleInfo = roleInfoDao.getAllFromRoleInfoByRoleId(apiId)
            if roleInfo.api_list == '*':
                apiInfoList = apiInfoDao.getAllFromApiInfo()
            elif roleInfo.api_list:
                apiIdList = json.loads(roleInfo.api_list)
                apiInfoList = apiInfoDao.getAllFromApiInfoByApiIdList(apiIdList)
            else:
                apiInfoList = []
            code = 200
            data = {
                'roleInfo': OrmConversion(roleInfo),
                'apiInfoList': OrmConversion(list(apiInfoList))
            }
        else:
            raise Exception('参数报错: roleId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加角色信息
#: url: roleInfo/setFromRoleInfo
#: 参数: roleName, remarks
def setFromRoleInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        roleName = requset.GET.get('roleName')
        remarks = requset.GET.get('remarks')
        if roleName:
            roleInfoDao.setFromRoleInfo(roleName, remarks)
            code, message = 200, '添加完成'
        else:
            raise Exception('参数报错: roleName  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据roleId更新角色信息
#: url: roleInfo/updAllFromRoleInfoByRoleId
#: 参数: roleId, roleName, apiList, remarks
def updAllFromRoleInfoByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        roleId = requset.GET.get('roleId')
        roleName = requset.GET.get('roleName')
        remarks = requset.GET.get('remarks')
        if roleId:
            roleInfoDao.updAllFromRoleInfoByRoleId(roleId, roleName=roleName, remarks=remarks)
            code, message = 200, '更新完成'
        else:
            raise Exception('参数报错: roleId  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())



#: 作用: 根据roleId删除指定角色信息
#: url: roleInfo/delFromRoleInfoByRoleId
#: 参数: roleId
def delFromRoleInfoByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        roleId = requset.GET.get('roleId')
        if roleId:
            userGroupDao.updRoleIdIsNoneFromUserGroupByRoleId(roleId)
            roleInfoDao.delFromRoleInfoByRoleId(roleId)
            code, message = 200, '更新完成'
        else:
            raise Exception('参数报错: apiId  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: roleInfo分页查询带模糊查询功能
#: url: roleInfo/getListFromRoleInfoByPage
#: 参数: page, roleName
def getListFromRoleInfoByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        roleName = requset.GET.get('roleName')
        if page:
            roleInfoList, numPages = roleInfoDao.getListFromRoleInfoByPage(page=page, roleName=roleName)
            code = 200
            data = {
                'roleInfoList': OrmConversion(list(roleInfoList)),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查询全部角色id与角色名
#: url: roleInfo/getRoleIdAndRoleNameFromRoleInfo
#: 参数: page, roleName
def getRoleIdAndRoleNameFromRoleInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)

        roleInfoList = roleInfoDao.getRoleIdAndRoleNameFromRoleInfo()
        code, data = 200, {'roleInfoList': list(roleInfoList)}
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据roleId查询角色信息与角色拥有的权限详情与未拥有的权限详情
#: url: roleInfo/getListFromRoleInfoAndApiInfoByRoleId
#: 参数: roleId
def getListFromRoleInfoAndApiInfoByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        apiId = requset.GET.get('roleId')
        if apiId:
            roleInfo = roleInfoDao.getAllFromRoleInfoByRoleId(apiId)
            if roleInfo.api_list == '*':
                apiInfoList = apiInfoDao.getAllFromApiInfo()
                notApiInfoList = []
            elif roleInfo.api_list:
                apiIdList = json.loads(roleInfo.api_list)
                apiInfoList = apiInfoDao.getAllFromApiInfoByApiIdList(apiIdList)
                notApiInfoList = apiInfoDao.getAllFromApiInfoByNotApiIdList(apiIdList)
            else:
                apiInfoList = []
                notApiInfoList = apiInfoDao.getAllFromApiInfo()
            code = 200
            data = {
                'roleInfo': OrmConversion(roleInfo),
                'apiInfoList': OrmConversion(list(apiInfoList)),
                'notApiInfoList': OrmConversion(list(notApiInfoList))
            }
        else:
            raise Exception('参数报错: roleId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加角色权限
#: url: roleInfo/addApiListFromRoleIdByRoleId
#: 参数: roleId, apiList
def addApiListFromRoleIdByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        roleId = requset.GET.get('roleId')
        apiList = requset.GET.get('apiList')
        if roleId and apiList:
            roleInfo = roleInfoDao.getAllFromRoleInfoByRoleId(roleId)
            if roleInfo.api_list == '*':
                raise Exception("权限报错: 不能修改admin权限！")
            apiList = json.loads(apiList)
            if roleInfo.api_list and roleInfoDao != 'null':
                dbApiList = json.loads(roleInfo.api_list)
                apiList = list(set(apiList).difference(set(dbApiList)))
                dbApiList.extend(apiList)
            else:
                dbApiList = apiList
            roleInfoDao.updAllFromRoleInfoByRoleId(roleId, apiList=json.dumps(dbApiList))
            code, message = 200, '添加权限完成'
        else:
            raise Exception('参数报错: roleId, apiList 都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 删除角色权限
#: url: roleInfo/delApiListFromRoleIdByRoleId
#: 参数: roleId, apiList
def delApiListFromRoleIdByRoleId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        roleId = requset.GET.get('roleId')
        apiList = requset.GET.get('apiList')
        if roleId and apiList:
            roleInfo = roleInfoDao.getAllFromRoleInfoByRoleId(roleId)
            if roleInfo.api_list == '*':
                raise Exception("权限报错: 不能修改admin权限！")
            apiList = json.loads(apiList)
            if roleInfo.api_list:
                dbApiList = json.loads(roleInfo.api_list)
                dbApiList = list(set(dbApiList).difference(set(apiList)))
                roleInfoDao.updAllFromRoleInfoByRoleId(roleId, apiList=json.dumps(dbApiList))
                code, message = 200, '删除权限完成'
            else:
                raise Exception('权限报错: 该角色没有需要删除的权限！')
        else:
            raise Exception('参数报错: roleId, apiList 都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())