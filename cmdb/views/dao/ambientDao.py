from cmdb.models import Ambient, HostInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#: 添加Ambient
def setFromAmbient(ambientName, remarks):
    ambient = Ambient.objects.create(
        ambient_name=ambientName,
        remarks=remarks
    )
    ambient.save()


#: 删除Ambient
def delFromAmbientById(id):
    hostInfoList = HostInfo.objects.filter(ambient__id=id).iterator()
    if len(list(hostInfoList)) == 0:
        Ambient.objects.get(id=id).delete()
    else:
        raise Exception("环境删除失败：环境中还有主机存在！")


#: 查看Ambient
def getAllFromAmbient():
    ambient = Ambient.objects.all().iterator()
    return ambient


#: 更新Ambient
def updAllFromAmbientById(id, ambientName=None, remarks=None):
    ambient = Ambient.objects.get(id=id)
    if ambientName:
        ambient.ambient_name = ambientName
    if remarks:
        ambient.remarks = remarks
    ambient.save()


#: 查看指定Ambient信息
def getAllFromAmbientById(id):
    ambient = Ambient.objects.get(id=id)
    return ambient


#: 作用: 查看分页Ambient信息
def getAllFromAmbientByPage(page=1, count=10, ambientName=None):
    if ambientName:
        ambientList = Ambient.objects.filter(ambient_name__contains=ambientName).order_by("id")
    else:
        ambientList = Ambient.objects.all().order_by("id")
    paginator = Paginator(ambientList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages