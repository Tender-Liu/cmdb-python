from cmdb.models import RoleInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#: 根据roleId查询角色信息
def getAllFromRoleInfoByRoleId(roleId):
    roleInfo = RoleInfo.objects.get(role_id=roleId)
    return roleInfo


#: 添加角色信息
def setFromRoleInfo(roleName, remarks):
    roleInfo = RoleInfo.objects.create(
        role_name=roleName,
        remarks=remarks
    )
    roleInfo.save()
    return roleInfo.role_id


#: 根据roleId更新角色信息
def updAllFromRoleInfoByRoleId(roleId, roleName=None, apiList=None, remarks=None):
    roleInfo = RoleInfo.objects.get(role_id=roleId)
    if roleName:
        roleInfo.role_name = roleName
    if apiList:
        roleInfo.api_list = apiList
    if remarks:
        roleInfo.remarks = remarks
    roleInfo.save()


#: 根据roleId删除角色信息
def delFromRoleInfoByRoleId(roleId):
    RoleInfo.objects.get(role_id=roleId).delete()


#: 角色分页查询带模糊查询功能
def getListFromRoleInfoByPage(page=1, count=10, roleName=None):
    if roleName:
        roleInfoList = RoleInfo.objects.filter(role_name__contains=roleName).order_by("role_id")
    else:
        roleInfoList = RoleInfo.objects.all().order_by("role_id")

    paginator = Paginator(roleInfoList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 查询全部角色id与角色名
def getRoleIdAndRoleNameFromRoleInfo():
    roleInfoList = RoleInfo.objects.values("role_id", "role_name").all().iterator()
    return roleInfoList
