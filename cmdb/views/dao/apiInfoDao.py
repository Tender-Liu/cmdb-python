from cmdb.models import ApiInfo, RoleInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


#: 根据apiId查询api信息
def getAllFromApiInfoByApiId(apiId):
    apiInfo = ApiInfo.objects.get(api_id=apiId)
    return apiInfo


#: 添加api信息
def setFromApiInfo(apiUrl, apiName, remarks):
    apiInfo = ApiInfo.objects.create(
        api_url=apiUrl,
        api_name=apiName,
        remarks=remarks
    )
    apiInfo.save()
    return apiInfo.api_id


#: 根据apiId更新api信息
def updAllFromApiInfoByApiId(apiId, apiUrl=None, apiName=None, remarks=None):
    apiInfo = ApiInfo.objects.get(api_id=apiId)
    if apiUrl:
        apiInfo.api_url = apiUrl
    if apiName:
        apiInfo.api_name = apiName
    if remarks:
        apiInfo.remarks = remarks
    apiInfo.save()


#: 根据apiId删除指定api信息
def delFromApiInfoByApiId(apiId):
    apiInfoList = RoleInfo.objects.filter(api_list__contains=apiId)
    for apiInfo in apiInfoList:
        apiList = json.loads(apiInfo.api_list)
        apiList.remove(int(apiId))
        apiInfo.api_list = json.dumps(apiList)
        apiInfo.save()
    ApiInfo.objects.get(api_id=apiId).delete()


#: apiInfo分页查询带模糊查询功能
def getListFromApiInfoByPage(page=1, count=10, apiUrl=None):
    if apiUrl:
        apiInfoList = ApiInfo.objects.filter(api_url__contains=apiUrl).order_by("-create_time")
    else:
        apiInfoList = ApiInfo.objects.all().order_by("-create_time")

    paginator = Paginator(apiInfoList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 根据apiUrl查询api是否存在，返回apiId
def getApiIdFromApiInfoByApiUrl(apiUrl):
    apiInfo = ApiInfo.objects.filter(api_url=apiUrl).values('api_id').first()
    return apiInfo['api_id']


#: 查询apiId列表查询api信息
def getAllFromApiInfoByApiIdList(apiIdList):
    apiInfoList = ApiInfo.objects.filter(api_id__in=apiIdList).iterator()
    return apiInfoList


#: 查询除apiId列表中的api信息
def getAllFromApiInfoByNotApiIdList(apiIdList):
    apiInfoList = ApiInfo.objects.exclude(api_id__in=apiIdList).iterator()
    return apiInfoList


#: 查询所有api信息，管理员使用
def getAllFromApiInfo():
    apiInfoList = ApiInfo.objects.all().iterator()
    return apiInfoList