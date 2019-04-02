from utils.JsonResponse import JsonResponse, OrmConversion
from utils.UserSession import checkUserSession
from django.shortcuts import HttpResponse
from cmdb.views.dao import projectSettingDao
from utils.JsonResponse import JsonResponse
from utils.JsonResponse import OrmConversion


#: 作用: 分页查询项目配置文件信息，包含项目以及配置文件名模糊匹配
#: url: projectSetting/getAllFromProjectSettingByPage
#: 参数: page, projectId, fileName
def getAllFromProjectSettingByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        projectId = requset.GET.get('projectId')
        ambientId = requset.GET.get('ambientId')
        fileName = requset.GET.get('fileName')
        projectSettingList, numPages = projectSettingDao.getAllFromProjectSettingByPage(page=page, projectId=projectId, ambientId=ambientId, fileName=fileName)
        code = 200
        data = {
            'projectSettingList': list(projectSettingList),
            'numPages': numPages,
            'page': int(page)
        }
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加项目配置文件
#: url: projectSetting/addFromProjectSettingByProjectIdAndAmbientId
#: 参数: projectId, ambientId, fileName, remotePath, remarks
def addFromProjectSettingByProjectIdAndAmbientId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        projectId = requset.GET.get('projectId')
        ambientId = requset.GET.get('ambientId')
        fileName = requset.GET.get('fileName')
        remotePath = requset.GET.get('remotePath')
        remarks = requset.GET.get('remarks')
        if projectId and ambientId and fileName and remotePath:
            projectSettingDao.addFromProjectSettingByProjectIdAndAmbientId(projectId, ambientId, fileName, remotePath, remarks)
            code, message = 200, '新建项目配置文件完成'
        else:
            raise Exception('参数报错: projectId, ambientId, fileName, remotePath 都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 编辑配置文件 #内容#
#: url: projectSetting/editFromProjectSettingByProjectId
#: 参数: settingId, content
def editFromProjectSettingByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        settingId = requset.GET.get('settingId')
        content = requset.GET.get('content')
        if settingId:
            projectSettingDao.editFromProjectSettingByProjectId(settingId, content=content)
            code, message = 200, "编辑内容，保存完成"
        else:
            raise Exception('参数报错: settingId, content 都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看指定文件 #内容#
#: url: projectSetting/getContentFromProjectSettingByProjectId
#: 参数: settingId
def getContentFromProjectSettingByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        settingId = requset.GET.get('settingId')
        if settingId:
            content = projectSettingDao.getContentFromProjectSettingByProjectId(settingId)
            code, data = 200, {'content': content}
        else:
            raise Exception('参数报错: settingId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看指定配置  #文件信息#
#: url: projectSetting/getAllFromProjectSettingByProjectId
#: 参数: settingId
def getAllFromProjectSettingByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        settingId = requset.GET.get('settingId')
        if settingId:
            projectSetting = projectSettingDao.getAllFromProjectSettingByProjectId(settingId)
            code, data = 200, {'projectSetting': OrmConversion(projectSetting)}
        else:
            raise Exception('参数报错: settingId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 修改指定配置 #文件信息#
#: url: projectSetting/updFromProjectSettingByProjectId
#: 参数: settingId, projectId, ambientId, fileName, remotePath
def updFromProjectSettingByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        settingId = requset.GET.get('settingId')
        projectId = requset.GET.get('projectId')
        ambientId = requset.GET.get('ambientId')
        fileName = requset.GET.get('fileName')
        remotePath = requset.GET.get('remotePath')
        remarks = requset.GET.get('remarks')
        if settingId and projectId and ambientId and fileName and remotePath:
            projectSettingDao.updFromProjectSettingByProjectId(settingId, projectId, ambientId, fileName, remotePath, remarks=remarks)
            code, message = 200, '配置文件信息，更新完成'
        else:
            raise Exception('参数报错: settingId, projectId, ambientId, fileName, remotePath 都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 删除配置文件
#: url: projectSetting/delFromProjectSettingByProjectId
#: 参数: settingId
def delFromProjectSettingByProjectId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        settingId = requset.GET.get('settingId')
        if settingId:
            projectSettingDao.delFromProjectSettingByProjectId(settingId)
            code, message = 200, '删除配置文件完成'
        else:
            raise Exception('参数报错: settingId 不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())