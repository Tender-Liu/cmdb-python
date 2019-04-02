#!/usr/bin python
# _*_ coding:utf-8 _*_
from cmdb.models import *


#: 获取指定任务操作日志
def getAllFromTaskLogListByTaskId(taskId):
    taskLogList = TaskLogList.objects.filter(task_id=taskId).iterator()
    return taskLogList


#: 添加操作日志
def setFromTaskLogListByTaskId(taskId, execute, logInfo):
    logList = TaskLogList.objects.create(
        task_id=taskId,
        execute=execute,
        log_info=logInfo
    )
    logList.save()
    return logList.log_id
