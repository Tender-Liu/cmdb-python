import json, os, shutil
from django.core.paginator import Paginator
from django.utils import timezone
from cmdb.models import ProjectInfo, HostInfo
from cmdb.views.dao import hostInfoDao
from devops.settings import ProjectPath


#: 作用: 查看分页项目信息
def getAllFromProjectInfoByPage(page=1, count=10, projectName=None):
    filter_dict = dict()
    if projectName:
        filter_dict['project_name__contains'] = projectName
    ProjectInfoList = ProjectInfo.objects.filter(**filter_dict).order_by('project_id')

    paginator = Paginator(ProjectInfoList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 添加项目信息
def setFromProjectInfo(projectName, projectPath, packagePath, projectPort, projectType, githubUrl,
                       gitId=None, mavenPath=None, remarks=None):
    projectInfo = ProjectInfo.objects.create(
        project_name=projectName,
        project_path=projectPath,
        package_path=packagePath,
        project_port=projectPort,
        project_type=projectType,
        github_url=githubUrl,
        git_id=gitId,
        maven_path=mavenPath,
        remarks=remarks
    )
    projectInfo.save()
    #： 检查项目构建仓库路径是否村存在，不存在则创建
    if os.path.exists(ProjectPath['build']+'/'+projectName) == False:
        os.makedirs(ProjectPath['build']+'/'+projectName)
    return projectInfo.project_id


#: 修改项目信息
def updFromProjectInfoByProjectId(projectId, projectName, projectPath, packagePath, projectPort, projectType,
                                  githubUrl, gitId=None, mavenPath=None, remarks=None):
    projectInfo = ProjectInfo.objects.get(project_id=projectId)
    oldProjectName = None
    if projectName:
        oldProjectName = ProjectPath['build'] + '/' + projectInfo.project_name
        projectInfo.project_name = projectName
    if projectPath:
        projectInfo.project_path = projectPath
    if packagePath:
        projectInfo.package_path = packagePath
    if projectPort:
        projectInfo.project_port = projectPort
    if projectType:
        projectInfo.project_type = projectType
    if githubUrl:
        projectInfo.github_url = githubUrl
    projectInfo.git_id = gitId
    projectInfo.maven_path = mavenPath
    projectInfo.remarks = remarks
    projectInfo.update_time = timezone.now()
    projectInfo.save()
    if oldProjectName is not None:
        os.rename(oldProjectName, ProjectPath['build'] + '/' + projectInfo.project_name)
    return projectInfo.project_id


#: 删除项目,同时删除主机保存次项目的Id
def delFromProjectInfoByProjectId(projectId):
    hostInfoList = HostInfo.objects.values('host_id', 'project_list').all()
    for hostInfo in hostInfoList:
        projectList = hostInfo['project_list']
        if projectList is not None and projectList != '[]':
            projectList = json.loads(projectList)
            if projectId in projectList:
                projectList.remove(projectId)
            hostInfoDao.updProjectListFromHostInfoByHostId(hostInfo['host_id'], json.dumps(projectList))
    projectInfo = ProjectInfo.objects.get(project_id=projectId)
    projectName = projectInfo.project_name
    projectInfo.delete()
    shutil.rmtree(ProjectPath['build'] + '/' + projectName)
    if os.path.exists(os.getcwd() + '/' + ProjectPath['setting'] + '/' + projectId):
        shutil.rmtree(os.getcwd() + '/' + ProjectPath['setting'] + '/' + projectId)


#: 查询指定项目详情
def getAllFromProjectInfoByProjectId(projectId):
    projectInfo = ProjectInfo.objects.values(
        "project_id", "project_name", "project_path", "package_path", "project_port", "project_type", "git__git_name",
        "git", "github_url", "maven_path", "update_time", "remarks").get(project_id=projectId)
    return projectInfo


#: 根据projectIdList查询项目名
def getProjectNameFromProjectInfoByProjectIdList(projectIdList):
    projectInfoList = ProjectInfo.objects.values('project_id', 'project_name').filter(project_id__in=projectIdList)
    return projectInfoList


#: 查询所有项目名与项目Id
def getProjectNameFromProjectInfo():
    projectInfoList = ProjectInfo.objects.values('project_id', 'project_name').all().iterator()
    return projectInfoList


#: 查询所有项目id与项目路径
def getProjectPathProjectNameFromProjectInfo():
    projectInfoList = ProjectInfo.objects.values('project_id', 'project_path').all()
    return projectInfoList


#: 查询所有指定的gitId的项目
def getAllFromProjectNameFromGitId(gitId):
    projectInfoList = ProjectInfo.objects.values('project_id', 'project_name').filter(git=gitId).iterator()
    return projectInfoList