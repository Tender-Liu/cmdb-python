from django.shortcuts import HttpResponse
from cmdb.views.dao import userGroupDao, userInfoDao
from utils.JsonResponse import JsonResponse
from utils.JsonResponse import OrmConversion
from utils.UserSession import checkUserSession


#: 作用: 根据groupId查询查询用户组信息
#: url: userGroup/getAllFromUserGroupByGroupId
#: 参数: groupId
def getAllFromUserGroupByGroupId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        groupId = requset.GET.get('groupId')
        if groupId:
            userGroup = userGroupDao.getAllFromUserGroupByGroupId(groupId)
            code, data = 200, {'userGroup': OrmConversion(userGroup)}
        else:
            raise Exception('参数报错: groupId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加用户分组信息
#: url: userGroup/setFromUserGroup
#: 参数: groupName, roleId, remarks
def setFromUserGroup(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        groupName = requset.GET.get('groupName')
        roleId = requset.GET.get('roleId')
        remarks = requset.GET.get('remarks')
        if groupName:
            userGroupDao.setFromUserGroup(groupName, roleId, remarks)
            code, message = 200, '添加完成'
        else:
            raise Exception('参数报错: groupName  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())



#: 作用: 根据groupId更新用户信息
#: url: userGroup/updAllFromUserGroupByGroupId
#: 参数: groupId, groupName, roleId, remarks
def updAllFromUserGroupByGroupId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        groupId = requset.GET.get('groupId')
        groupName = requset.GET.get('groupName')
        roleId = requset.GET.get('roleId')
        remarks = requset.GET.get('remarks')
        if groupId:
            userGroupDao.updAllFromUserGroupByGroupId(groupId, groupName=groupName, roleId=roleId, remarks=remarks)
            code, message = 200, '更新完成'
        else:
            raise Exception('参数报错: groupId  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据groupId删除角色信息
#: url: userGroup/delFromUserGroupByGroupId
#: 参数: groupId
def delFromUserGroupByGroupId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        groupId = requset.GET.get('groupId')
        if groupId:
            userInfoDao.updGroupIdFromUserInfoByGroupId(groupId)
            userGroupDao.delFromUserGroupByGroupId(groupId)
            code, message = 200, '删除完成'
        else:
            raise Exception('参数报错: groupId  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 用户组分页查询带模糊查询功能
#: url: userGroup/getListFromUserGroupByPage
#: 参数: page, groupName
def getListFromUserGroupByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        groupName = requset.GET.get('groupName')
        if page:
            userGroupList, numPages = userGroupDao.getListFromUserGroupByPage(page=page, groupName=groupName)
            code = 200
            data = {
                'userGroupList': list(userGroupList),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page  不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 获取所有用户组与用户组Id
#: url: userGroup/getGroupIdAndGroupNameFromUserGroup
#: 参数: groupId
def getGroupIdAndGroupNameFromUserGroup(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        userGroupList = userGroupDao.getGroupIdAndGroupNameFromUserGroup()
        code, data = 200, {'userGroupList': list(userGroupList)}
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())
