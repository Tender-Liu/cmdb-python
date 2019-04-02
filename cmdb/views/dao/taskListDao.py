#!/usr/bin python
# _*_ coding:utf-8 _*_
from cmdb.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from utils import sendemail


#: 获取全部任务数，或个人任务数
def getAllTaskCount(userId=None):
    if userId:
        taskList = TaskList.objects.filter(create=userId)
    else:
        taskList = TaskList.objects.filter()
    count = taskList.count()
    return count


#: 获取任务各种状态的任务数
def getTaskStateCount(taskState, userId=None):
    if userId:
        taskList = TaskList.objects.filter(create=userId, task_state=taskState)
    else:
        taskList = TaskList.objects.filter(task_state=taskState)
    count = taskList.count()
    return count


#: 获取指定taskId任务信息
def getAllFromTaskListByTaskId(taskId):
    taskList = TaskList.objects.values(
            "task_id", "task_name", "task_state", "task_info",
            "create_id", "create__user_name", "execute_id", "execute__user_name", "authorizer_id", "authorizer__user_name",
            "remarks", "created_date", "modify_date"
        ).get(task_id=taskId)
    return taskList


#: 插入task_list数据
def setAllFromTaskList(taskName, taskInfo, createId, executeId, authorizerId, modifyDate):
    taskList = TaskList.objects.create(
        task_name=taskName,
        task_info=taskInfo,
        task_state=1,
        create_id=createId,
        execute_id=executeId,
        authorizer_id=authorizerId,
        modify_date=modifyDate
    )
    taskList.save()
    return taskList.task_id


#: 更新指定任务信息
def updAllFromTaskListByTaskId(taskId, taskState=None, taskInfo=None, executeId=None, authorizerId=None, modifyDate=None, remarks=None):
    taskList = TaskList.objects.get(task_id=taskId)
    if taskState:
        taskList.task_state = taskState
    if taskInfo:
        taskList.task_info = taskInfo
    if executeId:
        taskList.execute_id = executeId
    if authorizerId:
        taskList.authorizer_id = authorizerId
    if modifyDate:
        taskList.modify_date = modifyDate
    taskList.remarks = remarks
    taskList.save()


#: 任务分页功能
def getAllFromTaskListByPage(page=1, count=10, taskName=None, taskState=None, userId=None):
    filter_dict = dict()
    if taskName:
        filter_dict['task_name__contains'] = taskName
    if taskState:
        filter_dict['task_state'] = taskState
    if userId:
        taskList = TaskList.objects.filter(Q(create_id=userId)|Q(execute_id=userId)|Q(authorizer_id=userId), **filter_dict).values(
            "task_id", "task_name", "task_state", "task_info", "create__user_name", "execute__user_name",
            "authorizer__user_name", "remarks", "created_date", "modify_date"
        ).order_by("-created_date")
    else:
        taskList = TaskList.objects.filter(**filter_dict).values(
            "task_id", "task_name", "task_state", "task_info", "create__user_name", "execute__user_name",
            "authorizer__user_name", "remarks", "created_date", "modify_date"
        ).order_by("-created_date")
    paginator = Paginator(taskList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 查询任务信息发送提示邮件
def sendEmailFromTaskListByTaskId(taskId):
    taskInfo = TaskList.objects.values(
        "task_id", "task_name", "task_state", "task_info", "create__user_name", "create__email", "execute__user_name",
        "execute__email", "authorizer__user_name", "authorizer__email", "remarks", "created_date", "modify_date"
    ).get(task_id=taskId)
    subject = '任务提示'
    addressee = [taskInfo['create__email'], taskInfo['execute__email'], taskInfo['authorizer__email']]
    html = 'task-info.html'
    sendEmail = sendemail.SendEmail()
    message = sendEmail.sendMail(subject=subject, addressee=addressee, html=html, data=taskInfo)
    if message is not True:
        raise Exception('任务提示邮件, 发送失败！')
