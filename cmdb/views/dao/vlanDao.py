from cmdb.models import Vlan, HostInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#: 添加vlan
def setFromVlan(vlanName, gateway, network):
    vlan = Vlan.objects.create(
        vlan_name=vlanName,
        gateway=gateway,
        network=network
    )
    vlan.save()


#: 删除vlan
def delFromVlanById(id):
    hostInfoList = HostInfo.objects.filter(vlan__id=id).iterator()
    if len(list(hostInfoList)) == 0:
        Vlan.objects.get(id=id).delete()
    else:
        raise Exception('vlan删除失败: vlan中还有主机！')


#: 查看分页vlan
def getAllFromVlanByPage(page=1, count=10, vlanName=None):
    if vlanName:
        vlanList = Vlan.objects.filter(vlan_name__contains=vlanName).order_by("id")
    else:
        vlanList = Vlan.objects.all().order_by("id")
    paginator = Paginator(vlanList, count)
    pageList = paginator.page(number=page)
    return pageList, paginator.num_pages


#: 查看所有vlan信息
def getIdAndVlanNameFromVlan():
    vlanList = Vlan.objects.values('id', 'vlan_name').all().iterator()
    return vlanList


#: 更新vlan
def updAllFromVlanById(id, vlanName=None, gateway=None, network=None):
    vlan = Vlan.objects.get(id=id)
    if vlanName:
        vlan.vlan_name= vlanName
    if gateway:
        vlan.gateway = gateway
    if network:
        vlan.network = network
    vlan.save()


#: 查看指定vlan信息
def getAllFromValnById(id):
    vlan = Vlan.objects.get(id=id)
    return vlan


#: 根据vlan名查询vlan信息
def getAllFromVlanByVlanName(vlanName):
    vlanInfo  = Vlan.objects.filter(vlan_name=vlanName).first()
    return vlanInfo