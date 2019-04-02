from django.shortcuts import HttpResponse
from cmdb.views.dao import taskListDao
from django.forms.models import model_to_dict
from cmdb.views.dao import taskLogListDao
import json
from utils.DateEncoder import DateEncoder
from utils.JsonResponse import JsonResponse
from utils.UserSession import checkUserSession


#: 作用: 返回所有任务count
#: url: taskList/getCountFromTaskList
#: 参数: userId
def getCountFromTaskList(request):
    data = {}
    userId = request.GET.get('userId')
    count = taskListDao.getAllTaskCount(userId)
    data['count'] = count
    return HttpResponse(json.dumps(data).encode('utf-8'))


#: 作用: 返回所有任务各种状态count
#: url: taskList/getCountFromTaskListByTaskState
#: 参数: userId, taskState
def getCountFromTaskListByTaskState(request):
    data = {}
    userId = request.GET.get('userId')
    taskState = request.GET.get('taskState')
    if taskState is None:
        data['message'] = '任务状态不能为空！'
    else:
        count = taskListDao.getTaskStateCount(taskState, userId=userId)
        data['count'] = count
    return HttpResponse(json.dumps(data).encode('utf-8'))


#: 作用: 返回指定任务详情
#: url: taskList/getAllFromTaskListByTaskId
#: 参数: taskId
def getAllFromTaskListByTaskId(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        taskId = request.GET.get('taskId')
        if taskId is None:
            raise Exception('taskId不能为空')
        else:
            taskList = taskListDao.getAllFromTaskListByTaskId(taskId)
            code, data = 200, {'taskList': taskList}
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加任务
#: url: taskList/setAllFromTaskList
#: 参数: taskName, taskInfo, executeId, authorizerId, modifyDate
def setAllFromTaskList(request):
    code, data, message = None, None, None
    try:
        createId = checkUserSession(request)['user_id']
        taskName = request.GET.get('taskName')
        executeId = request.GET.get('executeId')
        authorizerId = request.GET.get('authorizerId')
        taskInfo = request.GET.get('taskInfo')
        modifyDate = request.GET.get('modifyDate')
        if taskInfo and executeId and authorizerId and modifyDate:
            taskId = taskListDao.setAllFromTaskList(taskName, taskInfo, createId, executeId, authorizerId, modifyDate)
            taskListDao.sendEmailFromTaskListByTaskId(taskId)
            code, data, message = 200, {'taskId': taskId}, '添加完成'
        else:
            raise Exception('参数报错:taskInfo, executeId, authorizerId, modifyDate都不能为空!')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 修改任务信息
#: url: taskList/updAllFromTaskListByTaskId
#: 参数: taskId,taskState,taskInfo,executeId,authorizerId,modifyDate
def updAllFromTaskListByTaskId(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        taskId = request.GET.get('taskId')
        taskInfo = request.GET.get('taskInfo')
        executeId = request.GET.get('executeId')
        authorizerId = request.GET.get('authorizerId')
        modifyDate = request.GET.get('modifyDate')

        if taskId is None:
            raise Exception('taskId不能为空')
        taskList = taskListDao.getAllFromTaskListByTaskId(taskId)
        if userInfo['user_name'] == 'admin':
            taskListDao.updAllFromTaskListByTaskId(taskId, taskInfo=taskInfo, executeId=executeId,
                                                   authorizerId=authorizerId, modifyDate=modifyDate)
            code, data, message = 200, None, '修改完成'
            return
        if taskList['task_state'] == 2 or taskList['task_state'] == 4 or taskList['task_state'] == 3:
            raise Exception("修改失败：任务已经授权或完成操作，不能再修改任务内容！")
        else:
            taskListDao.updAllFromTaskListByTaskId(taskId, taskInfo=taskInfo, executeId=executeId, authorizerId=authorizerId, modifyDate=modifyDate)
            code, data, message = 200, None, '修改完成'
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 更新任务状态
#: url: taskList/updTaskStateFromTaskListByTaskId
#: 参数: taskId,taskState
def updTaskStateFromTaskListByTaskId(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        taskId = request.GET.get('taskId')
        taskState = request.GET.get('taskState')
        remarks = request.GET.get('remarks')
        if userInfo['user_name'] == 'admin':
            taskListDao.updAllFromTaskListByTaskId(taskId, taskState=taskState, remarks=remarks)
            taskListDao.sendEmailFromTaskListByTaskId(taskId)
            code, message = 200, "任务状态更新完成"
            return
        if taskId is None and taskState is None:
            raise Exception('参数报错：taskId, taskState 都不能为空')
        if taskState.isdigit():
            taskState = int(taskState)
        taskList = taskListDao.getAllFromTaskListByTaskId(taskId)
        if taskList['task_state'] == 2 or taskList['task_state'] == 4:
            raise Exception("不能再次修改内容")
        elif taskState == 1:
            raise Exception("不能再将任务修改为审核中！")
        elif taskState == 2 or taskState == 3:
            if taskList['task_state'] == 1 and userInfo['user_id'] == taskList['authorizer_id']:
                taskListDao.updAllFromTaskListByTaskId(taskId, taskState=taskState, remarks=remarks)
            elif taskList['task_state'] != 1:
                raise Exception('任务状态必须为审核中！')
            else:
                raise Exception('操作权限失败，任务授权人不是您！')
        elif taskState == 4:
            if taskList['task_state'] == 3 and userInfo['user_id'] == taskList['execute_id']:
                taskListDao.updAllFromTaskListByTaskId(taskId, taskState=taskState)
            elif taskList['task_state'] != 3:
                raise Exception('任务状态必须为审核完成！')
            else:
                raise Exception('操作权限失败，任务执行人不是您！')
        else:
            raise Exception('暂无您指定的状态')
        taskListDao.sendEmailFromTaskListByTaskId(taskId)
        code, message = 200, "任务状态更新完成"
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查询任务操作日志
#: url: taskList/getAllFromTaskLogListByTaskId
#: 参数: taskId
def getAllFromTaskLogListByTaskId(request):
    data = {}
    taskId = request.GET.get('taskId')
    try:
        checkUserSession(request)
        if taskId is None:
            data['message'] = '参数报错: taskId不能为空!'
        else:
            taskLogList = taskLogListDao.getAllFromTaskLogListByTaskId(taskId)
            for taskLog in taskLogList:
                data[taskLog.log_id] = model_to_dict(taskLog)
    except Exception as e:
        data['message'] = str(e)
    finally:
        return HttpResponse(json.dumps(data, cls=DateEncoder, ensure_ascii=False).encode('utf-8'))


#: 作用: 添加任务操作日志
#: url: taskList/setAllFromTaskLogListByTaskId
#: 参数: taskId,execute,logInfo
def setAllFromTaskLogListByTaskId(request):
    data = {}
    taskId = request.GET.get('taskId')
    execute = request.GET.get('execute')
    logInfo = request.GET.get('logInfo')
    try:
        userInfo = checkUserSession(request)
        if taskId and execute and logInfo:
            logId = taskLogListDao.setFromTaskLogListByTaskId(taskId, execute, logInfo)
            data['logId'] = logId
        else:
            data['message'] = '参数报错: taskId,execute,logInfo不能为空!'
    except Exception as e:
        data['message'] = str(e)
    finally:
        return HttpResponse(json.dumps(data).encode('utf-8'))


#: 作用: 任务分页查询
#: url: taskList/getAllFromTaskListByPage
#: 参数: page,userId,taskState
def getAllFromTaskListByPage(request):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(request)
        page = request.GET.get('page')
        taskState = request.GET.get('taskState')
        type = request.GET.get('type')
        taskName = request.GET.get('taskName')
        userId = None
        if type == 'user' and userInfo['user_name'] != 'admin':
            userId = userInfo['user_id']
        if page:
            taskList, num_pages = taskListDao.getAllFromTaskListByPage(page, taskName=taskName, taskState=taskState, userId=userId)
            data = {
                'taskList':  list(taskList),
                'num_pages': num_pages,
                'page': int(page)
            }
            code = 200
        else:
            raise Exception('参数报错: page不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())
