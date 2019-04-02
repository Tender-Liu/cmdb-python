from cmdb.models import UserGroup
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#: 根据groupId查询查询用户组信息
def getAllFromUserGroupByGroupId(groupId):
    userGroup = UserGroup.objects.get(group_id=groupId)
    return userGroup

#: 根据groupName查询查询用户组信息
def getAllFromUserGroupByGroupName(groupName):
    userGroup = UserGroup.objects.filter(group_name=groupName).first()
    return userGroup


#: 添加用户分组信息
def setFromUserGroup(groupName, roleId, remarks):
    userGroup = UserGroup.objects.create(
        group_name=groupName,
        role_id=roleId,
        remarks=remarks
    )
    userGroup.save()
    return userGroup.group_id


#: 根据groupId更新用户信息
def updAllFromUserGroupByGroupId(groupId, groupName, roleId, remarks):
    userGroup = UserGroup.objects.get(group_id=groupId)
    if groupId:
        userGroup.group_id=groupId
    if groupName:
        userGroup.group_name=groupName
    if roleId:
        userGroup.role_id=roleId
    if remarks:
        userGroup.remarks = remarks
    userGroup.save()


#: 根据groupId删除角色信息
def delFromUserGroupByGroupId(groupId):
    UserGroup.objects.get(group_id=groupId).delete()


#: 用户组分页查询带模糊查询功能
def getListFromUserGroupByPage(page=1, count=10, groupName=None):
    filter_dict = dict()
    if groupName:
        filter_dict['group_name__contains'] = groupName

    userGroupList = UserGroup.objects.values('group_id', 'group_name', 'role__role_name',
                                             'remarks', 'create_time').filter(**filter_dict).order_by("group_id")
    paginator = Paginator(userGroupList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 获取所有用户组与用户组Id
def getGroupIdAndGroupNameFromUserGroup():
    userGroupList = UserGroup.objects.values('group_id', 'group_name').all().iterator()
    return userGroupList


#: 根据角色Id查询用户组,并且更新用户组roleId为空
def updRoleIdIsNoneFromUserGroupByRoleId(roleId):
    userGroupList = UserGroup.objects.filter(role_id=roleId)
    for userGroup in userGroupList:
        userGroup.role_id = ''
        userGroup.save()