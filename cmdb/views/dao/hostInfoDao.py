#!/usr/bin/env python
# -*-coding:utf-8-*-
from cmdb.views.dao import saltDao
from cmdb.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.db.models import Q


#: 获取数据库中不存在的新主机
def getNewSaltId():
    newHost = []
    saltHostList = saltDao.getSaltTest("*")
    for saltHostInfo in saltHostList.keys():
        if saltHostList[saltHostInfo] == True:
            hostInfo = HostInfo.objects.filter(salt_id=saltHostInfo).first()
            if hostInfo is None:
                newHost.append(saltHostInfo)
    return newHost


#: salt收集主机信息，保存数据库
#: 使用此方法，请先使用test方法，测试salt-minion连接性
def setSaltHostInfo(saltIdList):
    saltGrains = saltDao.getSaltGrains(saltIdList)
    saltSsh = saltDao.getHostSsh(saltIdList)
    saltDisk = saltDao.getSaltDisk(saltIdList)
    saltMem = saltDao.getSaltMem(saltIdList)
    for saltId in saltIdList:
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

        hostInfo = HostInfo.objects.create(
            salt_id=saltId,
            host_name=hostName,
            alies_name=aliesName,
            os_fullname=osFullName,
            os_release=osRelease,
            kernel_release=kernelRelease,
            cpu_model=cpuModel,
            cpus_number = cpusNumber,
            host_type = hostType,
            memory=mem,
            swap=swap,
            ssh_port=sshPort,
        )
        hostInfo.save()
        for key, values in saltGrains[saltId]['ip4_interfaces'].items():
            if key == "lo" or len(values) == 0:
                continue
            network = Network.objects.create(
                host_id=hostInfo.host_id,
                network_name=key,
                ip_address=values[0]
            ).save()
        diskList = saltDisk[saltId].split('\n')
        for diskStr in diskList:
            diskInfo = diskStr.split(' ')
            DiskInfo.objects.create(
                host_id=hostInfo.host_id,
                disk_name=diskInfo[1].strip(':'),
                size_gb=diskInfo[2],
                size_bytes=diskInfo[4]
            ).save()


#: 查看分页主机信息
def getAllHostInfoByPage(page=1, count=10, projectId=None, ambientId=None, ip=None):
    filter_dict = dict()
    if ambientId:
        filter_dict['ambient__id'] = ambientId
    if ip:
        filter_dict['network_host__ip_address__contains'] = ip
    hostInfoList = HostInfo.objects.filter(**filter_dict).values(
        "host_id", "salt_id", "host_name", "ambient__ambient_name",
        "memory", "os_release", "cpus_number", "state", "project_list").order_by("-created_time")

    #: 过滤不保存项目Id的主机
    if projectId:
        tempHostInfoList = []
        for hostInfo in hostInfoList:
            if hostInfo['project_list'] is not None and int(projectId) in json.loads(hostInfo['project_list']):
                tempHostInfoList.append(hostInfo)
        hostInfoList = tempHostInfoList

    paginator = Paginator(hostInfoList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 查询指定主机详情
def getAllHostInfoByHostId(hostId):
    hostInfo = HostInfo.objects.values("host_id", "salt_id", "host_name", "alies_name", "vlan__vlan_name",
                                           "ambient__ambient_name", "memory", "swap", "os_fullname", "os_release",
                                           "kernel_release", "cpu_model", "cpus_number", "host_type", "ssh_port",
                                           "state", "delete", "remarks", "created_time", "project_list"
                                       ).get(host_id=hostId)
    return hostInfo


#: 更新主机信息
def updAllHostInfobyHostId(hostId=None,saltId=None, hostName=None, aliesName=None, vlanId=None, ambientId=None,
                           memory=None, swap=None, osFullname=None, osRelease=None, kernelRelease=None,
                           cpuModel=None, cpusNumber=None, hostType=None, sshPort=None, state=None, delete=None,
                           remarks=None):
    hostInfo = None
    if hostId:
        hostInfo = HostInfo.objects.get(host_id=hostId)
    elif saltId:
        hostInfo = HostInfo.objects.get(salt_id=saltId)
    else:
        raise Exception("参数报错: hostId与saltId，必须有个值不能为空！")
    if hostName:
        hostInfo.host_name = hostName
    if aliesName:
        hostInfo.alies_name = aliesName
    if vlanId:
        hostInfo.vlan_id = vlanId
    if ambientId:
        hostInfo.ambient_id = ambientId
    if memory:
        hostInfo.memory = memory
    if swap:
        hostInfo.swap = swap
    if osFullname:
        hostInfo.os_fullname = osFullname
    if osRelease:
        hostInfo.os_release = osRelease
    if kernelRelease:
        hostInfo.kernel_release = kernelRelease
    if cpuModel:
        hostInfo.cpu_model = cpuModel
    if cpusNumber:
        hostInfo.cpus_number = cpusNumber
    if hostType:
        hostInfo.host_type = hostType
    if sshPort:
        hostInfo.ssh_port = sshPort
    if state is not None:
        hostInfo.state = state
    if delete:
        hostInfo.delete = delete
    if remarks:
        hostInfo.remarks = remarks
    hostInfo.save()
    return hostInfo.host_id


#: 查询所有主机saltId
def getSaltIdFromHostInfo(hostId=None):
    hostInfo = None
    if hostId:
        hostInfo = HostInfo.objects.filter(host_id=hostId, delete=0).values("host_id", "salt_id")
    else:
        hostInfo = HostInfo.objects.filter(delete=0).values("host_id", "salt_id")
    return hostInfo


#: 查看指定hostId的主机信息
def getHostInfoByHostId(hostId):
    hostInfo = HostInfo.objects.get(host_id=hostId)
    return hostInfo


#: 根据saltIdList查询主机信息返回状态为0得主机信息
def getSaltIdListFromHostInfoByState(saltIdList):
    hostInfoList = HostInfo.objects.values('salt_id').filter(state=0, salt_id__in=saltIdList).iterator()
    saltIdList = [hostInfo['salt_id'] for hostInfo in hostInfoList]
    return saltIdList


#: 查询主机状态不异常并且管理中得主机信息
def getALlFromHostInfoByState():
    hostInfoList = HostInfo.objects.values('host_id', 'salt_id', 'project_list').filter().exclude(Q(state=1 )| Q(delete=1))
    return hostInfoList


#: 跟新主机项目列表
def updProjectListFromHostInfoByHostId(hostId, projectList):
    hostInfo = HostInfo.objects.get(host_id=hostId)
    hostInfo.project_list = projectList
    hostInfo.save()