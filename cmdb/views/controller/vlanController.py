from django.shortcuts import HttpResponse
from cmdb.views.dao import vlanDao
from utils.JsonResponse import JsonResponse
from utils.JsonResponse import OrmConversion
from utils.UserSession import checkUserSession


#: 作用: 添加vlan
#: url: vlan/setFromVlan
#: 参数: vlanName, gateway, network
def setFromVlan(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        vlanName = requset.GET.get('vlanName')
        gateway = requset.GET.get('gateway')
        network = requset.GET.get('network')
        if vlanName and gateway and network:
            vlanInfo = vlanDao.getAllFromVlanByVlanName(vlanName)
            if vlanInfo != None:
                raise Exception("vlan名已存在，请修改vlan名！")
            vlanDao.setFromVlan(vlanName, gateway, network)
            code, message = 200, '添加成功'
        else:
            raise Exception('参数报错: vlanName, gateway, network 都不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 删除vlan
#: url: vlan/delFromVlanById
#: 参数: id
def delFromVlanById(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        id= requset.GET.get('id')
        if id and id.isdigit():
            vlanDao.delFromVlanById(id)
            code, message = 200, '删除成功'
        else:
            raise Exception('参数报错： id不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看分页vlan
#: url: vlan/getAllFromVlanByPage
#: 参数: page, vlanName
def getAllFromVlanByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        vlanName = requset.GET.get('vlanName')
        if page:
            vlanList, numPages = vlanDao.getAllFromVlanByPage(page=page, vlanName=vlanName)
            code = 200
            data = {
                'vlanList': OrmConversion(list(vlanList)),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 更新vlan信息
#: url: vlan/updAllFromVlanById
#: 参数: id, vlanName, gateway, network
def updAllFromVlanById(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        id = requset.GET.get('id')
        vlanName = requset.GET.get('vlanName')
        gateway = requset.GET.get('gateway')
        network = requset.GET.get('network')
        if id and id.isdigit():
            vlanDao.updAllFromVlanById(id, vlanName=vlanName, gateway=gateway, network=network)
            code, message = 200, '更新成功'
        else:
            raise Exception('参数报错： id不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看指定vlan信息
#: url: vlan/getAllFromValnById
#: 参数: id
def getAllFromValnById(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        id = requset.GET.get('id')
        if id and id.isdigit():
            vlanInfo = vlanDao.getAllFromValnById(id)
            code, data = 200, { 'vlan': OrmConversion(vlanInfo) }
        else:
            raise Exception('参数报错： id不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看所有vlan信息
#: url: vlan/getIdAndVlanNameFromVlan
#: 参数: None
def getIdAndVlanNameFromVlan(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        vlanList = vlanDao.getIdAndVlanNameFromVlan()
        code, data = 200, {'vlanList': list(vlanList)}
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())