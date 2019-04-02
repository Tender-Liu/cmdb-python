from cmdb.views.dao import monitorDashDao
from utils.JsonResponse import JsonResponse, OrmConversion
from utils.UserSession import checkUserSession
from django.shortcuts import HttpResponse

def getMonitorItem(request):
	code, data, message = None, None, None
	data = {}
	cpu_use_20,cpu_use_20_50,cpu_use_50_80,cpu_use_80 = 0,0,0,0
	mem_use_20, mem_use_20_50, mem_use_50_80, mem_use_80 = 0,0,0,0
	load_use_1,load_use_1_5,load_use_5_10,load_use_10 = 0,0,0,0
	try:
		result = monitorDashDao.getMonitorItem()

		for item in OrmConversion(list(result)):
			if float(item['cpu_use']) < 20:
				cpu_use_20 += 1
			if float(item['cpu_use']) >= 20 and float(item['cpu_use']) < 50:
				cpu_use_20_50 += 1
			if float(item['cpu_use']) >= 50 and float(item['cpu_use']) < 80:
				cpu_use_50_80 += 1
			if float(item['cpu_use']) >= 80:
				cpu_use_80 += 1

			if float(item['mem_use']) < 20:
				mem_use_20 += 1
			if float(item['mem_use']) >= 20 and float(item['mem_use']) < 50:
				mem_use_20_50 += 1
			if float(item['mem_use']) >= 50 and float(item['mem_use']) < 80:
				mem_use_50_80 += 1
			if float(item['mem_use']) >= 80:
				mem_use_80 += 1

			if float(item['load5']) < 1:
				load_use_1 += 1
			if float(item['load5']) >= 1 and float(item['load5']) < 5:
				load_use_1_5 += 1
			if float(item['load5']) >= 5 and float(item['load5']) < 10:
				load_use_5_10 += 1
			if float(item['load5']) >= 10:
				load_use_10 += 1

		data['cpu'] = [{'value':cpu_use_20,'name':'20%以下'},
					   {'value':cpu_use_20_50,'name':'20%~50%'},
					   {'value':cpu_use_50_80,'name':'50%~80%'},
					   {'value':cpu_use_80,'name':'80%以上'}]

		data['mem'] = [{'value': mem_use_20, 'name': '20%以下'},
					   {'value': mem_use_20_50, 'name': '20%~50%'},
					   {'value': mem_use_50_80, 'name': '50%~80%'},
					   {'value': mem_use_80, 'name': '80%以上'}]

		data['load5'] = [{'value': load_use_1, 'name': '1以下'},
					   {'value': load_use_1_5, 'name': '1~5'},
					   {'value': load_use_5_10, 'name': '5~10'},
					   {'value': load_use_10, 'name': '10以上'}]
		print(data)
		code, message = 200, 'OK'
	except Exception as e:
		code, data, message = 300, None, str(e)
	finally:
		return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())

