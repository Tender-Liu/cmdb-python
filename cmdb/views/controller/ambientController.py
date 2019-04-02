from django.shortcuts import HttpResponse
from cmdb.views.dao import ambientDao
from utils.JsonResponse import JsonResponse
from utils.JsonResponse import OrmConversion
from utils.UserSession import checkUserSession


#: 作用: 添加Ambient
#: url: ambient/setFromAmbient
#: 参数: ambientName, remarks
def setFromAmbient(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        ambientName= requset.GET.get('ambientName')
        remarks = requset.GET.get('remarks')
        if ambientName:
            ambientDao.setFromAmbient(ambientName, remarks)
            code, message = 200, '添加成功'
        else:
            raise Exception('参数报错: ambientName不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 删除Ambient
#: url: ambient/delFromAmbientById
#: 参数: id
def delFromAmbientById(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        id= requset.GET.get('id')
        if id and id.isdigit():
            ambientDao.delFromAmbientById(id)
            code, message = 200, '删除成功'
        else:
            raise Exception('参数报错： id不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看Ambient
#: url: ambient/getAllFromAmbient
#: 参数: id
def getAllFromAmbient(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        ambientList = ambientDao.getAllFromAmbient()
        code, data = 200, { 'ambientList': OrmConversion(list(ambientList)) }
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 更新Ambient
#: url: ambient/updAllFromAmbientById
#: 参数: id, ambientName, remarks
def updAllFromAmbientById(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        id = requset.GET.get('id')
        ambientName = requset.GET.get('ambientName')
        remarks = requset.GET.get('remarks')
        if id and id.isdigit():
            ambientDao.updAllFromAmbientById(id, ambientName=ambientName, remarks=remarks)
            code, message = 200, '更新成功'
        else:
            raise Exception('参数报错： id不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看指定Ambient信息
#: url: ambient/getAllFromAmbientById
#: 参数: id
def getAllFromAmbientById(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        id = requset.GET.get('id')
        if id and id.isdigit():
            ambient = ambientDao.getAllFromAmbientById(id)
            code, data = 200, { 'ambient': OrmConversion(ambient) }
        else:
            raise Exception('参数报错： id不能为空！')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查看分页Ambient信息
#: url: ambient/getAllFromAmbientByPage
#: 参数: page, ambientName
def getAllFromAmbientByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        ambientName = requset.GET.get('ambientName')
        if page:
            ambientList, numPages = ambientDao.getAllFromAmbientByPage(page=page, ambientName=ambientName)
            code = 200
            data = {
                'ambientList': OrmConversion(list(ambientList)),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())