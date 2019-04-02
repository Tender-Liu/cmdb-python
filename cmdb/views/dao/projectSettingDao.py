from django.core.paginator import Paginator
from cmdb.models import ProjectSetting
from devops.settings import ProjectPath
import os, pathlib, shutil
from django.utils import timezone


#: 分页查询项目配置文件信息，包含项目以及配置文件名模糊匹配
def getAllFromProjectSettingByPage(page=1, count=10, projectId=None, ambientId=None, fileName=None):
    filter_dict = dict()
    if projectId:
        filter_dict['project_id'] = projectId
    if ambientId:
        filter_dict['ambient_id'] = ambientId
    if fileName:
        filter_dict['file_name__contains'] = fileName
    projectSettingList = ProjectSetting.objects.values(
        'setting_id', 'project__project_name', 'ambient__ambient_name', 'file_name', 'remote_path', 'update_time', 'remarks'
        ).filter(**filter_dict).order_by('setting_id')

    paginator = Paginator(projectSettingList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 添加项目配置文件信息
def addFromProjectSettingByProjectIdAndAmbientId(projectId, ambientId, fileName, remotePath, remarks):
    projectSetting = ProjectSetting.objects.create(
        project_id=projectId,
        ambient_id=ambientId,
        file_name=fileName,
        remote_path=remotePath,
        remarks=remarks,
    )
    projectSetting.save()
    localPath = os.getcwd()+'/'+ProjectPath['setting']+'/'+projectId+'/'+ambientId
    if not os.path.exists(localPath):
        os.makedirs(localPath)
        pathlib.Path(localPath+'/'+fileName).touch()
    return projectSetting.setting_id


#: 编辑配置文件 #内容#
def editFromProjectSettingByProjectId(settingId, content=''):
    projectSetting = ProjectSetting.objects.get(setting_id=settingId)
    localPath = os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) +'/' + str(projectSetting.ambient_id) + '/' + projectSetting.file_name
    wfile = open(localPath, 'w+', encoding='utf-8')
    wfile.write(content)
    wfile.close()
    projectSetting.update_time = timezone.now()
    projectSetting.save()



#: 查看指定文件 #内容#
def getContentFromProjectSettingByProjectId(settingId):
    projectSetting = ProjectSetting.objects.get(setting_id=settingId)
    localPath = os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) + '/' + str(projectSetting.ambient_id) + '/' + projectSetting.file_name
    file = open(localPath, 'r+', encoding='utf-8')
    content = ''
    for line in file:
        content += line
    file.close()
    return content


#: 查看指定配置  #文件信息#
def getAllFromProjectSettingByProjectId(settingId):
    projectSetting = ProjectSetting.objects.get(setting_id=settingId)
    return projectSetting


#: 修改指定配置 #文件信息#
def updFromProjectSettingByProjectId(settingId, projectId, ambientId, fileName, remotePath, remarks=None):
    projectSetting = ProjectSetting.objects.get(setting_id=settingId)
    #: 文件路径--老
    oldLocalPath = os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) + '/' + str(projectSetting.ambient_id) + '/' + projectSetting.file_name
    projectSetting.remarks = remarks
    if projectId:
        projectSetting.project_id = projectId
    if ambientId:
        projectSetting.ambient_id =ambientId
    if fileName:
        projectSetting.file_name = fileName
    if remotePath:
        projectSetting.remote_path = remotePath
    projectSetting.update_time = timezone.now()
    projectSetting.save()
    #: 文件路径--新
    newLocalPath = os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) + '/' + str(projectSetting.ambient_id) + '/' + projectSetting.file_name
    #: 文件移动
    if oldLocalPath != newLocalPath:
        if not os.path.exists(os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) + '/' + str(projectSetting.ambient_id)):
            print(os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) + '/' + str(projectSetting.ambient_id))
            os.makedirs(os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) + '/' + str(projectSetting.ambient_id))
        shutil.move(oldLocalPath, newLocalPath)
        #: 删除空文件夹
        clearNullFolder(os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id))


#: 删除配置文件
def delFromProjectSettingByProjectId(settingId):
    projectSetting = ProjectSetting.objects.get(setting_id=settingId)
    #: 删除配置文件
    localPath = os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id) + '/' + str(projectSetting.ambient_id) + '/' + projectSetting.file_name
    os.remove(localPath)
    #: 删除空文件夹
    clearNullFolder(os.getcwd() + '/' + ProjectPath['setting'] + '/' + str(projectSetting.project_id))
    projectSetting.delete()


#: 清理空文件夹
def clearNullFolder(filePath):
    for dir in os.listdir(filePath):
        if os.path.isdir(filePath + '/' + dir):
            if not os.listdir(filePath + '/' + dir):
                os.rmdir(filePath + '/' + dir)
