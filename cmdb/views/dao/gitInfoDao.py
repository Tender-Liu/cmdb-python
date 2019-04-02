#!/usr/bin/env python
# -*-coding:utf-8-*-
from cmdb.models import GitInfo, ProjectInfo
from cmdb.views.dao import projectInfoDao
from django.core.paginator import Paginator
from django.utils import timezone
from utils.githot import githot
from devops.settings import ProjectPath
import os


#: 添加git信息
def addFromGitInfo(gitName, gitKey=None, gitPass=None, remarks=None):
    gitInfo = GitInfo.objects.create(
        git_name=gitName,
        git_key=gitKey,
        git_pass=gitPass,
        remarks=remarks
    )
    gitInfo.save()
    return gitInfo.git_id


#: 删除git信息
def delFromGitInfoByGitId(gitId):
    #: 去除项目中指定的gitId
    projectInfoList = ProjectInfo.objects.filter(git_id=gitId)
    for projectInfo in projectInfoList:
        projectInfo.git_id = None
        projectInfo.save()
    GitInfo.objects.get(git_id=gitId).delete()


#: 更新git信息
def updAllFromGitInfoByGitId(gitId, remarks, gitKey, gitPass=None, gitName=None):
    gitInfo = GitInfo.objects.get(git_id=gitId)
    if gitName:
        gitInfo.git_name = gitName

    gitInfo.git_pass = gitPass
    gitInfo.git_key = gitKey
    gitInfo.remarks = remarks
    gitInfo.update_time = timezone.now()
    gitInfo.save()
    return gitInfo.git_id


#: 查询指定git信息
def getAllFromGitInfoByGitId(gitId):
    gitInfo = GitInfo.objects.get(git_id=gitId)
    return gitInfo


#: 查询所有git名称，前端使用
def getGitNameFromGitInfo():
    gitInfoList = GitInfo.objects.values("git_id", "git_name").all()
    return gitInfoList


#: 分页查询,带模糊查询
def getAllFromGitInfoByPage(page, count=10, gitName=None):
    filter_dict = dict()
    if gitName:
        filter_dict['git_name__contains'] = gitName
    gitInfoList = GitInfo.objects.filter(**filter_dict).order_by('git_id')

    paginator = Paginator(gitInfoList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 根据项目id，获取所有git分支名
def getBranchsFromGitByProjectId(projectId):
    projectInfo = projectInfoDao.getAllFromProjectInfoByProjectId(projectId)
    if projectInfo['github_url'] is None or projectInfo['git'] is None:
        raise Exception('数据报错: 次项目git地址与git账号密码不能为空！')
    gitInfo = getAllFromGitInfoByGitId(projectInfo['git'])
    localPath = ProjectPath['build']+'/' + projectInfo['project_name']
    if os.path.exists(localPath) == False:
        os.makedirs(localPath)
    gitHot = githot(projectInfo['github_url'], gitInfo.git_name, gitInfo.git_pass, localPath)
    branchs = gitHot.getBranchsFromGit()
    return branchs