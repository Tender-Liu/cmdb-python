from utils.JsonResponse import JsonResponse, OrmConversion
from utils.UserSession import checkUserSession
from django.shortcuts import HttpResponse
from cmdb.views.dao import gitInfoDao


#: 作用: 添加git信息
#: url: gitInfo/addFromGitInfo
#: 参数: gitName, gitUser, gitPass, remarks
def addFromGitInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        gitName = requset.GET.get('gitName')
        gitKey = requset.GET.get('gitKey')
        gitPass = requset.GET.get('gitPass')
        remarks = requset.GET.get('remarks')
        if gitName:
            gitInfoDao.addFromGitInfo(gitName, gitKey=gitKey, gitPass=gitPass, remarks=remarks)
            code, message = 200, '添加信息成功'
        else:
            raise Exception('参数报错: gitName, gitUser, gitPass 都不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 删除git信息
#: url: gitInfo/delFromGitInfoByGitId
#: 参数: gitId
def delFromGitInfoByGitId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        gitId = requset.GET.get('gitId')
        if gitId:
            gitInfoDao.delFromGitInfoByGitId(gitId)
            code, message = 200, '删除信息成功'
        else:
            raise Exception('参数报错: gitId 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 更新git信息
#: url: gitInfo/updAllFromGitInfoByGitId
#: 参数: gitId, remarks, gitName, gitUser, gitPass
def updAllFromGitInfoByGitId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        gitId = requset.GET.get('gitId')
        gitName = requset.GET.get('gitName')
        gitKey = requset.GET.get('gitKey')
        gitPass = requset.GET.get('gitPass')
        remarks = requset.GET.get('remarks')
        if gitId:
            gitInfoDao.updAllFromGitInfoByGitId(gitId, remarks, gitName=gitName, gitKey=gitKey, gitPass=gitPass)
            code, message = 200, '更新信息成功'
        else:
            raise Exception('参数报错: gitId 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查询指定git信息
#: url: gitInfo/getAllFromGitInfoByGitId
#: 参数: gitId
def getAllFromGitInfoByGitId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        gitId = requset.GET.get('gitId')
        if gitId:
            gitInfo = gitInfoDao.getAllFromGitInfoByGitId(gitId)
            code, data = 200, {'gitInfo': OrmConversion(gitInfo)}
        else:
            raise Exception('参数报错: gitId 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查询所有git名称，前端使用
#: url: gitInfo/getGitNameFromGitInfo
#: 参数: gitId
def getGitNameFromGitInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        gitInfoList = gitInfoDao.getGitNameFromGitInfo()
        code, data = 200, {'gitInfoList': list(gitInfoList)}
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 分页查询,带模糊查询
#: url: gitInfo/getAllFromGitInfoByPage
#: 参数: gitName
def getAllFromGitInfoByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        gitName = requset.GET.get('gitName')
        if page:
            gitInfoList, numPages = gitInfoDao.getAllFromGitInfoByPage(page, gitName=gitName)
            code, data = 200, {
                'gitInfoList': OrmConversion(list(gitInfoList)),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 根据项目id，获取所有git分支名
#: url: gitInfo/getBranchsFromGitByProjectId
#: 参数: projectId
def getBranchsFromGitByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        projectId = requset.GET.get('projectId')
        if projectId:
            branchs = gitInfoDao.getBranchsFromGitByProjectId(projectId)
            code, data = 200, {'branchs': branchs}
        else:
            raise Exception('参数报错: projectId 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())
