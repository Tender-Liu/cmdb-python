from django.shortcuts import HttpResponse, redirect, render, render_to_response
from cmdb.views.dao import monitorInfoDao, networkDao
from utils.JsonResponse import JsonResponse
from utils.UserSession import checkUserSession


#: 作用: 一键安装新主机
#: url: monitorInfo/createHost
#: 参数: None
def createHost(request):
    code, data, message = None, None, None
    try:
        checkUserSession(request)
        host_ip = request.GET.get('host_ip')

        if host_ip:
            result = monitorInfoDao.createHost(host_ip)
            if result['code'] == 200:
                code, message = 200, '安装监控成功'
            else:
                raise Exception(result['data'])
        else:
            raise Exception('host_ip为空')
    except Exception as e:
        code, message = 300, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=None).getJson())


#: 作用: 查看主机监控信息
#: url: monitorInfo/getAllHostInfoByPage
#: 参数: page
def getAllHostInfoByPage(requset):
    code, data, message = None, None, None
    try:
        #checkUserSession(requset)
        zabbix_hostip = []
        page = requset.GET.get('page')
        if page:
            hostInfoList, numPages = monitorInfoDao.getAllHostInfoByPage(page=page)
            for hostInfo in hostInfoList:
                networkList = networkDao.getAllFromNetworkByHostId(hostInfo['host_id'], state=0)
                host_ip = ''
                for network in networkList:
                    if 'eth0' in network.network_name or 'en' in network.network_name or 'em' in network.network_name:
                        host_ip = network.ip_address
                        break
                hostInfo['ip'] = host_ip
                zabbix_hostip.append(host_ip)

            ip_id_D = monitorInfoDao.getAllHostID(zabbix_hostip)
            if ip_id_D:
                host_monitor_D = monitorInfoDao.getAllItem(ip_id_D)
                for k in hostInfoList:
                    for key, item in host_monitor_D.items():
                        if key in k['ip']:
                            k['cpu_use'] = item[0]
                            k['mem_use'] = item[1]
                            k['load5_use'] = item[2]
                            break
                        else:
                            k['cpu_use'] = ''
                            k['mem_use'] = ''
                            k['load5_use'] = ''
                data = {
                    'hostInfoList': list(hostInfoList),
                    'numPages': numPages,
                    'page': int(page)
                }
                code = 200
            else:
                for k in hostInfoList:
                    k['cpu_use'] = ''
                    k['mem_use'] = ''
                    k['load5_use'] = ''

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
