from django.shortcuts import HttpResponse
from cmdb.views.dao import hostInfoDao, saltDao, networkDao, diskInfoDao, projectInfoDao
from utils.JsonResponse import JsonResponse
import json
from utils.UserSession import checkUserSession


#: 作用: salt收集新主机信息
#: url: salt/setNewHostInfo
#: 参数: saltIdList
def setNewHostInfo(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        saltIdList = requset.GET.get('saltIdList')
        if saltIdList:
            saltIdList = json.loads(saltIdList)
            if type(saltIdList) == list:
                hostInfoDao.setSaltHostInfo(saltIdList)
                code, message = 200, "添加完成"
            else:
                 raise Exception("saltIdList转换list类型异常")
        else:
            raise Exception("saltIdList不能为空")
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: salt发现新主机
#: url: salt/getNewSaltId
#: 参数: None
def getNewSaltId(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        newHost = hostInfoDao.getNewSaltId()
        if newHost:
            data = newHost
        else:
            raise Exception("暂无新主机")
        code = 200
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: salt更新全部主机资源
#: url: salt/updAllHostInfoBySalt
#: 参数: hostId
def updAllHostInfoBySalt(request):
    code, data, message = None, None, None
    try:
        # session回话验证
        checkUserSession(request)
        hostId = request.GET.get('hostId')
        if hostId and hostId.isdigit() == False:
            raise Exception('参数报错: hostId必须为整数')
        hostInfoList = hostInfoDao.getSaltIdFromHostInfo(hostId=hostId)
        if len(hostInfoList) == 0:
            raise Exception('主机处于已删除状态，无法更新！')
        # 获取存在的saltId
        saltIdList = [ hostInfo['salt_id'] for hostInfo in hostInfoList ]
        # salt检查主机是否正常
        saltCheckList = saltDao.getSaltTest(saltIdList)
        # 如果不正常更新状态为下线,状态正常添加到主机列表中，进行更新

        for host in hostInfoList:
            if saltCheckList[host['salt_id']] != True:
                saltIdList.remove(host['salt_id'])
                hostInfoDao.updAllHostInfobyHostId(host['host_id'], state=1)

        if hostInfoList is not None:
            # 针对正常主机，获取主机信息，进行更新
            saltGrains = saltDao.getSaltGrains(saltIdList)
            saltSsh = saltDao.getHostSsh(saltIdList)
            saltDisk = saltDao.getSaltDisk(saltIdList)
            saltMem = saltDao.getSaltMem(saltIdList)
            for saltId in saltIdList:
                # 主机详细更新
                hostName = saltGrains[saltId]['nodename']
                aliesName = saltGrains[saltId]['host']
                osFullName = saltGrains[saltId]['osfullname']
                osRelease = saltGrains[saltId]['osrelease']
                kernelRelease = saltGrains[saltId]['kernelrelease']
                cpuModel = saltGrains[saltId]['cpu_model']
                cpusNumber = saltGrains[saltId]['num_cpus']
                hostType = saltGrains[saltId]['virtual']
                sshPort = saltSsh[saltId]
                mem = saltMem[saltId]['MemTotal']['value']
                swap = saltMem[saltId]['SwapTotal']['value']
                hostId = hostInfoDao.updAllHostInfobyHostId(saltId=saltId, hostName=hostName, aliesName=aliesName, memory=None, swap=None,
                                                   osFullname=osFullName, osRelease=osRelease, kernelRelease=kernelRelease,
                                                   cpuModel=cpuModel, cpusNumber=cpusNumber, hostType=hostType, sshPort=sshPort, state=0)
                # 网卡数据更新
                networkDao.delFromNetworkById(hostId)
                for key, values in saltGrains[saltId]['ip4_interfaces'].items():
                    if key == "lo" or len(values) == 0:
                        continue
                    network = networkDao.getFromNetworkByHostId(hostId, key)
                    if network:
                        networkDao.updFromNetworkByHostId(network.id, values[0])
                    else:
                        networkDao.setFromNetworkByHostId(hostId, key, values[0])
                # 磁盘数据更新
                diskInfoDao.delFromDiskInfoByHostId(hostId)
                diskList = saltDisk[saltId].split('\n')
                for diskStr in diskList:
                    diskStrList = diskStr.split(' ')
                    diskInfo = diskInfoDao.getFromDiskInfoById(hostId, diskStrList[1].strip(':'))
                    if diskInfo:
                        diskInfoDao.updFromDiskInfoByHostId(diskInfo.id, diskStrList[2], diskStrList[4])
                    else:
                        diskInfoDao.setFromDiskInfo(hostId, diskStrList[1].strip(':'), diskStrList[2], diskStrList[4])

        code, message = 200, '更新完成'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 主机远程批量命令执行
#: url: salt/getCommandFromSaltBySaltIdList
#: 参数: saltIdList, command
def getCommandFromSaltBySaltIdList(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        saltIdList = request.GET.get('saltIdList')
        command = request.GET.get('command')
        if saltIdList is None or command is None or saltIdList == '':
            raise Exception('参数报错: saltIdList, command不能为空！')
        saltIdList = saltIdList.split(',')
        normalSaltIdList = hostInfoDao.getSaltIdListFromHostInfoByState(saltIdList)
        commandResult = {}
        if normalSaltIdList:
            commandResult = saltDao.getCommandFromSaltBySaltIdList(normalSaltIdList, command)
        abnormalsetSaltIdList = list(set(saltIdList) - set(normalSaltIdList))
        for saltId in abnormalsetSaltIdList:
            commandResult[saltId] = 'salt无法连接，请检查主机salt-minion是否正常！'
        code, data = 200, {'commandResult': commandResult}
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 收集与更新主机项目列表
#: url: salt/getProjectListFromHostInfoBySalt
#: 参数: None
def getProjectListFromHostInfoBySalt(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        hostInfoList = hostInfoDao.getALlFromHostInfoByState()
        projectInfoList = projectInfoDao.getProjectPathProjectNameFromProjectInfo()

        for hostInfo in hostInfoList:
            projectList = []
            for projectInfo in projectInfoList:
                saltResult = saltDao.getCheckFolderFromSaltBysaltIdList(hostInfo['salt_id'], projectInfo['project_path'])
                if saltResult[hostInfo['salt_id']] == True:
                    projectList.append(projectInfo['project_id'])
            hostInfoDao.updProjectListFromHostInfoByHostId(hostInfo['host_id'], json.dumps(projectList))

        code, message= 200, '主机项目一键收集与更新完成'
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())
