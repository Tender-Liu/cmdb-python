#!/usr/bin python
# _*_ coding:utf-8 _*_
from cmdb.models import *
from django.core.paginator import Paginator


#: 登录账户密码查询
def getFromUserInfoByLogin(account):
    userInfo = None
    if account.isdigit():
        userInfo = UserInfo.objects.filter(phone=account).first()
    else:
        userInfo = UserInfo.objects.filter(email=account).first()
    if userInfo:
        return userInfo
    else:
        return None


#: 用户注册
def setFromUserInfo(email, phone, userName, password, groupId=None):
    userInfo = UserInfo.objects.create(
        email=email,
        phone=phone,
        user_name=userName,
        password=password,
        group_id=groupId
    )
    userInfo.save()
    return userInfo.user_id


#: 修改用户
def updAllFromUserInfoByUserId(user_id, userName=None, password=None, phone=None, email=None, groupId=None, state=None):
    userInfo = UserInfo.objects.get(user_id=user_id)
    if userName:
        userInfo.user_name = userName
    if password:
        userInfo.password = password
    if phone:
        userInfo.phone = phone
    if email:
        userInfo.email = email
    if groupId:
        userInfo.group_id = groupId
    if state:
        userInfo.state = state
    userInfo.save()


#: 查询用户信息
def getAllFromUsreInfoByUserId(userId):
    userInfo = UserInfo.objects.values("user_id", "user_name", "phone", "email", 'state',
                                       "group__group_id", "group__group_name", "group__role__api_list", "created_time").get(user_id=userId)
    return userInfo


#: 根据UserId查询用户密码
def getPassWordFromUserInfoByUserId(userId):
    userInfo = UserInfo.objects.values('password').get(user_id=userId)
    return userInfo['password']


#: 查询所有用户id与用户名
def getAllUserInfo(groupId=None):
    filter_dict = dict()
    if groupId:
        filter_dict["group_id"] = groupId
    userinfoList = UserInfo.objects.values("user_id", "user_name").filter(**filter_dict).all().iterator()
    return userinfoList


#: 用户信息查询分页功能，模糊查询
def getAllFromUserInfoByPage(page=1, count=10, groupId=None, userName=None):
    filter_dict = dict()
    if groupId and groupId != '0':
        filter_dict['group__group_id'] = groupId
    if userName:
        filter_dict['user_name__contains'] = userName
    userInfoList = UserInfo.objects.filter(**filter_dict).values('user_id', 'user_name', 'group__group_name',
                                                                 'phone', 'email', 'state', 'created_time').order_by('user_id')

    paginator = Paginator(userInfoList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 按部门查询用户，批量修改用户部门为空
def updGroupIdFromUserInfoByGroupId(groupId):
    userInfoList = UserInfo.objects.filter(group_id=groupId).all()
    for userInfo in userInfoList:
        userInfo.group_id = ''
        userInfo.save()
