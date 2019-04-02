from utils.JsonResponse import JsonResponse, OrmConversion
from utils.UserSession import checkUserSession
from django.shortcuts import HttpResponse
from cmdb.views.dao import projectInfoDao
from django.db.utils import IntegrityError


#: 作用: 查看分页项目信息
#: url: projectInfo/getAllFromProjectInfoByPage
#: 参数: page, projectName
def getAllFromProjectInfoByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        projectName = requset.GET.get('projectName')
        if page:
            projectInfoList, numPages = projectInfoDao.getAllFromProjectInfoByPage(page, projectName=projectName)
            code = 200
            data = {
                'projectInfoList': OrmConversion(list(projectInfoList)),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加项目信息
#: url: projectInfo/setFromProjectInfo
#: 参数: projectName, projectPath, packagePath, projectPort, projectType, githubUrl, gitId, mavenPath, remarks
def setFromProjectInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        projectName = requset.GET.get('projectName')
        projectPath = requset.GET.get('projectPath')
        packagePath = requset.GET.get('packagePath')
        projectPort = requset.GET.get('projectPort')
        projectType = requset.GET.get('projectType')
        githubUrl = requset.GET.get('githubUrl')
        gitId = requset.GET.get('gitId')
        mavenPath = requset.GET.get('mavenPath')
        remarks = requset.GET.get('remarks')
        if projectName and projectPath and packagePath and projectPort and projectType and githubUrl:
            projectInfoDao.setFromProjectInfo(projectName, projectPath, packagePath, projectPort, projectType, githubUrl,
                                                      gitId=gitId, mavenPath=mavenPath, remarks=remarks)
            code, message = 200, '项目信息添加成功'
        else:
            raise Exception('参数报错: projectName, projectPath, packagePath, projectPort, projectType, githubUrl 都不能为空！')
    except IntegrityError:
        code, data, message = 300, None, '项目已存在'
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 更新项目信息
#: url: projectInfo/updFromProjectInfoByProjectId
#: 参数: projectId, projectName, projectPath, packagePath
#:       projectPort, projectType, githubUrl, githubId, mavenPath, remarks
def updFromProjectInfoByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        projectId = requset.GET.get('projectId')
        projectName = requset.GET.get('projectName')
        projectPath = requset.GET.get('projectPath')
        packagePath = requset.GET.get('packagePath')
        projectPort = requset.GET.get('projectPort')
        projectType = requset.GET.get('projectType')
        githubUrl = requset.GET.get('githubUrl')
        gitId = requset.GET.get('gitId')
        mavenPath = requset.GET.get('mavenPath')
        remarks = requset.GET.get('remarks')
        if projectId and projectName and packagePath and packagePath and projectPort and projectType and githubUrl:
            projectInfoDao.updFromProjectInfoByProjectId(projectId, projectName, projectPath, packagePath, projectPort, projectType,
                                                         githubUrl, gitId=gitId, mavenPath=mavenPath, remarks=remarks)
            code, message = 200, '项目信息更新成功'
        else:
            raise Exception('参数报错: projectId, projectName, projectPath, packagePath, projectPort, projectType, githubUrl 都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 删除项目信息
#: url: projectInfo/delFromProjectInfoByProjectId
#: 参数: projectId
def delFromProjectInfoByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        projectId = requset.GET.get('projectId')
        if projectId:
            projectInfoDao.delFromProjectInfoByProjectId(projectId)
            code, message = 200, '项目信息删除成功'
        else:
            raise Exception('参数报错: projectId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看指定项目信息
#: url: projectInfo/getAllFromProjectInfoByProjectId
#: 参数: projectId
def getAllFromProjectInfoByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        projectId = requset.GET.get('projectId')
        if projectId:
            projectInfo = projectInfoDao.getAllFromProjectInfoByProjectId(projectId)
            code, data = 200, {'projectInfo': projectInfo}
        else:
            raise Exception('参数报错: projectId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 获取全部项目id与项目名
#: url: projectInfo/getProjectNameFromProjectInfo
#: 参数: None
def getProjectNameFromProjectInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        projectInfoList = projectInfoDao.getProjectNameFromProjectInfo()
        code, data = 200, {'projectInfoList': list(projectInfoList)}
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查询所有指定的gitId的项目
#: url: projectInfo/getAllFromProjectNameFromGitId
#: 参数: gitId
def getAllFromProjectNameFromGitId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        gitId = requset.GET.get('gitId')
        if gitId:
            projectInfoList = projectInfoDao.getAllFromProjectNameFromGitId(gitId)
            code, data = 200, {'projectInfoList': list(projectInfoList)}
        else:
            raise Exception('参数报错: projectId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())
