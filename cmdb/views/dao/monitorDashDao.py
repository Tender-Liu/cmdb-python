from cmdb.models import *

def getMonitorItem():
	result = Monitor.objects.all().iterator()
	return result

