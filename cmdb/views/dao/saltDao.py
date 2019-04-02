#!/usr/bin/env python
# -*-coding:utf-8-*-
from sdk_api import saltstack
import logging


#: 获取Linux主机远程端口
def getHostSsh(saltIdList):
    salt_api = saltstack.SaltAPI()
    tgt = saltIdList
    fun = 'cmd.run'
    arg = "netstat -lnpt | grep sshd | grep -v 'tcp6' | awk '{print $4}' | awk -F':' '{print $2}' | head -1"
    data = salt_api.salt_command(tgt, fun, arg)
    return data['return'][0]


#: salt-minion主机连接测试
def getSaltTest(saltIdList):
    salt_api = saltstack.SaltAPI()
    tgt = saltIdList
    fun = 'test.ping'
    data = salt_api.salt_command(tgt, fun)
    return data['return'][0]


#: salt ganins信息获取
def getSaltGrains(saltIdList):
    salt_api = saltstack.SaltAPI()
    tgt = saltIdList
    fun = 'grains.items'
    data = salt_api.salt_command(tgt, fun)
    return data['return'][0]


#: salt获取磁盘信息
def getSaltDisk(saltIdList):
    salt_api = saltstack.SaltAPI()
    tgt = saltIdList
    fun = 'cmd.run'
    arg = "fdisk -l | grep Disk | grep -vE '(identifier|/dev/mapper|label type)'"
    data = salt_api.salt_command(tgt, fun, arg)
    return data['return'][0]


#: salt获取内存信息
def getSaltMem(saltIdList):
    salt_api = saltstack.SaltAPI()
    tgt = saltIdList
    fun = 'status.meminfo'
    data = salt_api.salt_command(tgt, fun)
    return data['return'][0]


#: salt执行指定主机执行操作命令
def getCommandFromSaltBySaltIdList(saltIdList, command):
    salt_api = saltstack.SaltAPI()
    tgt = saltIdList
    fun = 'cmd.run'
    arg = command
    data = salt_api.salt_command(tgt, fun, arg)
    return data['return'][0]


#: salt检查指定主机得指定文件夹是否存在
def getCheckFolderFromSaltBysaltIdList(saltId, path):
    salt_api = saltstack.SaltAPI()
    tgt = saltId
    fun = 'file.directory_exists'
    arg = path
    data = salt_api.salt_command(tgt, fun, arg=arg)
    return data['return'][0]


