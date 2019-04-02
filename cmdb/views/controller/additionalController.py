from django.shortcuts import HttpResponse
from utils.JsonResponse import JsonResponse


#: 作用: 404
#: url: *
#: 参数: None
def getNotFindUrl():
    return HttpResponse(JsonResponse(code=404, message="url无效，系统暂无此api！", data=None).getJson())
