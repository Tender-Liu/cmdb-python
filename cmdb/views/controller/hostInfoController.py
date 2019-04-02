from django.shortcuts import HttpResponse
from cmdb.views.dao import hostInfoDao, networkDao, diskInfoDao, projectInfoDao
from utils.JsonResponse import JsonResponse
from utils.JsonResponse import OrmConversion
from utils.UserSession import checkUserSession
import json


#: 作用: 查看分页主机资源信息
#: url: hostInfo/getAllHostInfoByPage
#: 参数: page
def getAllHostInfoByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        projectId = requset.GET.get('projectId')
        ambientId = requset.GET.get('ambientId')
        ip = requset.GET.get('ip')
        if page:
            hostInfoList, numPages = hostInfoDao.getAllHostInfoByPage(page=page, projectId=projectId, ambientId=ambientId, ip=ip)
            for hostInfo in hostInfoList:
                networkList = networkDao.getAllFromNetworkByHostId(hostInfo['host_id'], state=0)
                ipstr = ''
                for network in networkList:
                    ipstr = ipstr + network.network_name + ': '+ network.ip_address + ' || '
                hostInfo['ip'] = ipstr.strip(' || ')
            data = {
                'hostInfoList': list(hostInfoList),
                'numPages': numPages,
                'page': int(page)
            }
            code = 200
        else:
            raise Exception('参数报错: page不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看指定主机详情包含ip列表与disk列表
#: url: hostInfo/getAllHostInfoByHostId
#: 参数: hostId
def getAllHostInfoByHostId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        hostId = requset.GET.get('hostId')
        if hostId and hostId.isdigit():
            hostInfo = hostInfoDao.getAllHostInfoByHostId(hostId)
            ipList = networkDao.getAllFromNetworkByHostId(hostId)
            diskList = diskInfoDao.getAllFromDiskInFoByHostId(hostId)
            if hostInfo['project_list'] is not None and hostInfo['project_list'] != '[]':
                projectInfoList = projectInfoDao.getProjectNameFromProjectInfoByProjectIdList(json.loads(hostInfo['project_list']))
            else:
                projectInfoList = []
            code = 200
            data = {
                'hostInfo': hostInfo,
                'ipList': OrmConversion(list(ipList)),
                'diskList': OrmConversion(list(diskList)),
                'projectInfoList': list(projectInfoList)
            }
        else:
            raise Exception('参数报错: hostId不能为空，并且是数字')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 更新指定主机详情
#: url: hostInfo/updHostInfoByHostId
#: 参数: hostId, vlanId, ambientId, remarks, delete
def updHostInfoByHostId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        hostId = requset.GET.get('hostId')
        vlanId = requset.GET.get('vlanId')
        ambientId = requset.GET.get('ambientId')
        delete = requset.GET.get('delete')
        remarks = requset.GET.get('remarks')
        if hostId and hostId.isdigit():
            hostInfoDao.updAllHostInfobyHostId(hostId=hostId, vlanId=vlanId, ambientId=ambientId, remarks=remarks, delete=delete)
            code, message = 200, '更新完成'
        else:
            raise Exception('参数报错: hostId不能为空，并且是数字')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看指定主机详情
#: url: hostInfo/getHostInfoByHostId
#: 参数: hostId
def getHostInfoByHostId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        hostId = requset.GET.get('hostId')
        if hostId and hostId.isdigit():
            hostInfo = hostInfoDao.getHostInfoByHostId(hostId)
            code, data = 200, {'hostInfo': OrmConversion(hostInfo)}
        else:
            raise Exception('参数报错: hostId不能为空，并且是数字')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())

