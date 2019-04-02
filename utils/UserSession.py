from cmdb.views.dao import userInfoDao
from cmdb.views.dao import apiInfoDao
import json

def checkUserSession(request):
    try:
        userId = request.session["userId"]
        userInfo = userInfoDao.getAllFromUsreInfoByUserId(userId=userId)
        apiStr = userInfo['group__role__api_list']
        if apiStr != '*':
            apiList = json.loads(apiStr)
            apiUrl = request.path[1:]
            apiId = apiInfoDao.getApiIdFromApiInfoByApiUrl(apiUrl)
            if apiId not in apiList:
                raise Exception('您暂无权限，请联系管理员，给您附加权限，谢谢！')
        return userInfo
    except KeyError:
        raise Exception("请求api失败,请登录后操作！")
    except Exception as e:
        raise Exception('您暂无权限，请联系管理员，给您附加权限，谢谢！%s', e)
