from django.shortcuts import *
from cmdb.views.dao import userInfoDao, userGroupDao
from utils.JsonResponse import JsonResponse
import hashlib
from utils.UserSession import checkUserSession


#: 作用: 添加用户
#: url: userInfo/setFromUserInfo
#: 参数: email, phone, userName, password
def setFromUserInfo(request):
    code, data, message = None, None, None
    try:
        email = request.GET.get('email')
        phone = request.GET.get('phone')
        userName = request.GET.get('userName')
        password = request.GET.get('passWord')
        if email and phone and userName and password:
            if userName == 'admin':
                raise Exception('参数报错: 不能注册管理员账号！')
            userInfo = userInfoDao.getFromUserInfoByLogin(phone)
            if userInfo:
                raise Exception("注册失败,手机号码已存在")
            userInfo = userInfoDao.getFromUserInfoByLogin(email)
            if userInfo:
                raise Exception("注册失败,邮箱已存在")
            h = hashlib.sha256()
            h.update(bytes(password, encoding='utf-8'))
            password = h.hexdigest()
            userGroup = userGroupDao.getAllFromUserGroupByGroupName('员工部')
            userInfoDao.setFromUserInfo(email, phone, userName, password, userGroup.group_id)
            code, message = 200, '账号注册成功'
        else:
            raise Exception('参数报错: 邮箱, 手机号码, 用户名, 密码 都不能为空!')
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户信息-个人用户使用
#: url: userInfo/updInfoFromUserInfo
#: 参数: userName, password
def updInfoFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        userName = request.GET.get('userName')
        phone = request.GET.get('phone')
        email = request.GET.get('email')
        if userName:
            if phone:
                checkUserInfo = userInfoDao.getFromUserInfoByLogin(phone)
                if checkUserInfo and checkUserInfo.user_id != userInfo['user_id']:
                    raise Exception("参数报错: 手机号码已存在")
            if email:
                checkUserInfo = userInfoDao.getFromUserInfoByLogin(phone)
                if checkUserInfo and checkUserInfo.user_id != userInfo['user_id']:
                    raise Exception("参数报错: 邮箱已存在")
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], userName=userName, phone=phone, email=email)
            code, message = 200, '信息更新成功'
        else:
            raise Exception('参数报错: 用户名不能修改为空！')
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户密码-个人用户使用
#: url: userInfo/updPassWordFromUserInfo
#: 参数: oldPassWrod, newPassWord
def updPassWordFromUserInfo(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        oldPassWrod = request.GET.get('oldPassWrod')
        newPassWord = request.GET.get('newPassWord')
        if oldPassWrod and newPassWord:
            #: 密旧码验证
            h = hashlib.sha256()
            h.update(bytes(oldPassWrod, encoding='utf-8'))
            oldPassWrod = h.hexdigest()
            dbPassWord = userInfoDao.getPassWordFromUserInfoByUserId(userInfo['user_id'])
            if oldPassWrod != dbPassWord:
                raise Exception('参数报错: 老密码错误，请重新输入谢谢！')
            #: 新密码更新
            p = hashlib.sha256()
            p.update(bytes(newPassWord, encoding='utf-8'))
            newPassWord = p.hexdigest()
            userInfoDao.updAllFromUserInfoByUserId(userInfo['user_id'], password=newPassWord)
            code, message = 200, '密码修改成功'
        else:
            raise Exception("参数报错: 新旧密码不能为空！")
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 登录验证+session
#: url: userInfo/getFromUserInfoByLogin
#: 参数: account, password
def getFromUserInfoByLogin(request):
    code, data, message = None, None, None
    try:
        account = request.GET.get('account')
        password = request.GET.get('password')
        if account and password:
            userInfo = userInfoDao.getFromUserInfoByLogin(account)
            if userInfo:
                if userInfo.state == 2:
                    raise Exception('登录报错: 对不起，您已离职，账号无法再次使用！')
                h = hashlib.sha256()
                h.update(bytes(password, encoding='utf-8'))
                if userInfo.password == h.hexdigest():
                    request.session['userId'] = userInfo.user_id
                    code, data, message = 200, {'userName': userInfo.user_name}, "登录完成"
                else:
                    raise Exception('密码输入错误')
            else:
                raise Exception("用户不存在")
        else:
            raise Exception('参数报错: 登录名与密码不能为空')
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 注销登录
#: url: userInfo/delFromSessionByKey
#: 参数: None
def delFromSessionByKey(request):
    code, data, message = None, None, None
    try:
        del request.session["userId"]
        code, message = 200, '注销完成'
    except Exception as e:
        code, message = 300, '用户没有登录，无需注销'
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 查询指定用户信息-admin用户使用
#: url: userInfo/getAllFromUsreInfoByUserId
#: 参数: userId
def getAllFromUsreInfoByUserId(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        userId = request.GET.get('userId')
        if userId is None:
            raise Exception('参数报错: userId不能为空！')
        userInfo = userInfoDao.getAllFromUsreInfoByUserId(userId)
        code, data = 200, {'userInfo': userInfo}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 查询全部用户id与用户名
#: url: userInfo/getAllUserInfo
#: 参数: None
def getAllUserInfo(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        groupId = request.GET.get("groupId")
        userInfoList = userInfoDao.getAllUserInfo(groupId=groupId)
        code, data = 200, list(userInfoList)
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 用户信息查询分页功能，模糊查询
#: url: userInfo/getAllFromUserInfoByPage
#: 参数: groupId, userName
def getAllFromUserInfoByPage(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        page = request.GET.get('page')
        groupId = request.GET.get('groupId')
        userName = request.GET.get('userName')
        userInfoList, numPages = userInfoDao.getAllFromUserInfoByPage(page=page, groupId=groupId, userName=userName)
        code = 200
        data = {
            'userInfoList': list(userInfoList),
            'numPages': numPages,
            'page': int(page)
        }
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 查询个人用户信息
#: url: userInfo/getAllFromUsreInfoByMyself
#: 参数: userId
def getAllFromUsreInfoByMyself(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        userInfo = userInfoDao.getAllFromUsreInfoByUserId(userInfo['user_id'])
        code, data = 200, {'userInfo': userInfo}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 重置用户密码-管理员使用
#: url: userInfo/updPassWordFromUserInfoByUserId
#: 参数: userId, password
def updPassWordFromUserInfoByUserId(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        userId = request.GET.get('userId')
        password = request.GET.get('password')
        if userId and password:
            h = hashlib.sha256()
            h.update(bytes(password, encoding='utf-8'))
            password = h.hexdigest()
            userInfoDao.updAllFromUserInfoByUserId(userId, password=password)
            code, message = 200, '重置密码成功'
        else:
            raise Exception("参数报错: userId与password 都不能为空！")
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 修改用户分组-管理员使用
#: url: userInfo/updGroupFromUserInfoByUserId
#: 参数: userId, password
def updGroupFromUserInfoByUserId(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        userId = request.GET.get('userId')
        groupId = request.GET.get('groupId')
        state = request.GET.get('state')
        if userId:
            userInfoDao.updAllFromUserInfoByUserId(userId, groupId=groupId, state=state)
            code, message = 200, '修改用户信息完成'
        else:
            raise Exception("参数报错: userId 不能为空！")
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())