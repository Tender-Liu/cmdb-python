from sdk_api.ZabbixApi import ZabbixAPI,ZabbixAPIException
from cmdb.models import *
from django.core.paginator import Paginator
from devops import settings

zabbix_host_url = settings.zabbix_host_url
zabbix_username = settings.zabbix_username
zabbix_password = settings.zabbix_password

def createHost(host_ip):
	try:
		zapi = ZabbixAPI(url=zabbix_host_url, user=zabbix_username, password=zabbix_password)

		params_json = {
			"host": host_ip,
			"interfaces": [
				{
					"type": 1,
					"main": 1,
					"useip": 1,
					"ip": host_ip,
					"dns": "",
					"port": "10050"
				}
			],
			"groups": [
				{
					"groupid": "2"
				}
			],
			"templates": [
				{
					"templateid": "10001"
				}
			]
		}

		zapi.do_request('host.create', params=params_json)
		result = {'code':200,'data':'create success'}
		return result
	except ZabbixAPIException as e:
		result  = {'code':300,'data':e.data}
		return result

#: 查看监控分页主机信息
def getAllHostInfoByPage(page=1, count=10):
	hostInfoList = HostInfo.objects.filter(delete=0).values("host_id", "host_name").order_by("-host_id")
	paginator = Paginator(hostInfoList, count)
	pageList = paginator.page(number=page)
	return pageList, paginator.num_pages

#参数：主机列表
#功能：获取hostid
#data['result']
"""
[{u'host': u'172.31.0.20', u'hostid': u'10261'}, 
 {u'host': u'172.31.0.96', u'hostid': u'10260'}, 
 {u'host': u'Zabbix server', u'hostid': u'10084'}
]
"""
#host_ip_D
"""
{u'Zabbix server': u'10084', u'172.31.0.20': u'10261', u'172.31.0.96': u'10260'}
"""
def getAllHostID(hostip_list=None):
	try:
		zapi = ZabbixAPI(url=zabbix_host_url, user=zabbix_username, password=zabbix_password)
		params_json = {
			"output": ["hostid","host"],
			"filter": {
				"host": hostip_list
			}
		}

		host_ip_D = {}
		data = zapi.do_request('host.get', params=params_json)
		for key in data['result']:
			host_ip_D[key['host']] = key['hostid']
		return host_ip_D
	except ZabbixAPIException as e:
		print(e)
		return None




# 参数：hostid字典，key是监控项
# 功能：获取CPU使用率
# all_host_d
"""
{'IP1':[use_cpu,use_mem,use_load5],'IP2':[use_cpu,use_mem,use_load5]}
"""
def getAllItem(hostid=None):
	all_host_d = {}

	if hostid:
		for k,v in hostid.items():
			system_cpu = float(getItem(v,"system.cpu.util[,system]"))
			user_cpu = float(getItem(v,"system.cpu.util[,user]"))
			use_cpu = format((system_cpu + user_cpu),'.2f')
			total_mem = int(getItem(v,"vm.memory.size[total]"))
			available_mem = int(getItem(v,"vm.memory.size[available]"))
			if total_mem !=0:
				use_mem = format((total_mem - available_mem)/total_mem,'.2f')
			else:
				use_mem = 0
			use_load5 = float(getItem(v,"system.cpu.load[percpu,avg5]"))
			use_load5_format = format(use_load5,'.2f')
			all_host_d[k] = [use_cpu,use_mem,use_load5_format]

			host_id = Network.objects.filter(ip_address=k).first().host_id

			exist_host_id = Monitor.objects.filter(host_id=host_id).first()
			if exist_host_id:
				exist_host_id.cpu_use = use_cpu
				exist_host_id.mem_use = use_mem
				exist_host_id.load5 = use_load5_format
				exist_host_id.save()
			else:
				monitor = Monitor.objects.create(cpu_use=use_cpu,mem_use=use_mem,load5=use_load5_format,host_id=host_id)
				monitor.save()

		return all_host_d

# 参数：hostid字符串，key是监控项
# 功能：获取CPU使用率
# data
"""
[{u'itemid': u'28578', u'lastvalue': u'0.1042'}]
"""
def getItem(hostid=None,key=None):
	try:
		zapi = ZabbixAPI(url=zabbix_host_url, user=zabbix_username, password=zabbix_password)
		params_json = {
			"output": ["lastvalue"],
			"hostids": hostid,
			"search": {
                "key_": key,
            },
		}

		data = zapi.do_request('item.get', params=params_json)
		return data['result'][0]['lastvalue']
	except ZabbixAPIException as e:
		return None



