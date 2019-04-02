from utils.JsonResponse import JsonResponse, OrmConversion
from utils.UserSession import checkUserSession
from django.shortcuts import HttpResponse
from cmdb.views.dao import releaseOrderDao


#: 作用: 发布工单分页查询，带模糊查询
#: url: releaseOrder/getListFromReleaseOrderByPage
#: 参数: page, orderTitle, status
def getListFromReleaseOrderByPage(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        page = requset.GET.get('page')
        orderTitle = requset.GET.get('orderTitle')
        status = requset.GET.get('status')
        if page:
            releaseOrderList, numPages= releaseOrderDao.getListFromReleaseOrderByPage(page, orderTitle=orderTitle, status=status)
            code = 200
            data = {
                'releaseOrderList': list(releaseOrderList),
                'numPages': numPages,
                'page': int(page)
            }
        else:
            raise Exception('参数报错: page 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 查询指定orderId的工单信息
#: url: releaseOrder/getAllFromReleaseOrderByOrderId
#: 参数: orderId
def getAllFromReleaseOrderByOrderId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        orderId = requset.GET.get('orderId')
        if orderId:
            releaseOrder = releaseOrderDao.getAllFromReleaseOrderByOrderId(orderId)
            code, data = 200, {'releaseOrder': releaseOrder}
        else:
            raise Exception('参数报错: orderId不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 添加发布工单信息
#: url: releaseOrder/setFromReleaseOrder
#: 参数: orderTitle, orderContent, releaseTime, ambientId, artisanId, authorId, productId, remarks, ftpPath
def setFromReleaseOrder(requset):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(requset)
        orderTitle = requset.GET.get('orderTitle')
        orderContent = requset.GET.get('orderContent')
        releaseTime = requset.GET.get('releaseTime')
        executorId = requset.GET.get('executorId')
        ambientId = requset.GET.get('ambientId')
        artisanId = requset.GET.get('artisanId')
        authorId = userInfo['user_id']
        productId = requset.GET.get('productId')
        remarks = requset.GET.get('remarks')
        ftpPath = requset.GET.get('ftpPath')
        if orderTitle and orderContent and releaseTime and ambientId and artisanId and authorId and productId and executorId:
            releaseOrder = releaseOrderDao.setFromReleaseOrder(orderTitle, orderContent, releaseTime, ambientId, executorId,
                                                               artisanId, authorId, productId, remarks=remarks, ftpPath=ftpPath)
            code, message = 200, '添加工单完成'
        else:
            raise Exception('参数报错: orderTitle, orderContent, releaseTime, ambientId, executorId, artisanId, authorId, productId 都不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 删除发布工单信息
#: url: releaseOrder/delFromReleaseOrderByOrderId
#: 参数: orderId
def delFromReleaseOrderByOrderId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        orderId = requset.GET.get('orderId')
        if orderId:
            releaseOrderDao.delFromReleaseOrderByOrderId(orderId)
            code, message = 200, '删除工单完成'
        else:
            raise Exception('参数报错: orderId 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 指定orderId, 修改工单内容
#: url: releaseOrder/updContentFromReleaseOrdeByOrderId
#: 参数: orderId, orderTitle, orderContent, ambientId, releaseTime, ftpPath, remarks
def updContentFromReleaseOrdeByOrderId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        orderId = requset.GET.get('orderId')
        orderTitle = requset.GET.get('orderTitle')
        orderContent = requset.GET.get('orderContent')
        ambientId = requset.GET.get('ambientId')
        releaseTime = requset.GET.get('releaseTime')
        executorId = requset.GET.get('executorId')
        artisanId = requset.GET.get('artisanId')
        productId = requset.GET.get('productId')
        ftpPath = requset.GET.get('ftpPath')
        remarks = requset.GET.get('remarks')
        if orderId:
            releaseOrderDao.updContentFromReleaseOrdeByOrderId(orderId, orderTitle, orderContent, ambientId, releaseTime,
                                                               executorId, artisanId, productId, ftpPath=ftpPath, remarks=remarks)
            code, message = 200, '更新工单内容成功'
        else:
            raise Exception('参数报错: orderId 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 指定orderId,修改工单授权
#: url: releaseOrder/updAuthorizerFromReleaseOrdeByOrderId
#: 参数: userId, orderId, authorizer
def updAuthorizerFromReleaseOrdeByOrderId(requset):
    code, data, message = None, None, None
    try:
        userInfo = checkUserSession(requset)
        userId = userInfo['userId']
        orderId = requset.GET.get('orderId')
        authorizer = requset.GET.get('authorizer')
        if userId:
            releaseOrderDao.updAuthorizerFromReleaseOrdeByOrderId(userId, orderId, authorizer)
            code, message = 200, '发布工单授权完成'
        else:
            raise Exception('参数报错: orderId 不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())


#: 作用: 指定orderId,修改工单状态
#: url: releaseOrder/updStatusFromReleaseOrderByOrderId
#: 参数: orderId, status
def updStatusFromReleaseOrderByOrderId(requset):
    code, data, message = None, None, None
    try:
        checkUserSession(requset)
        orderId = requset.GET.get('orderId')
        status = requset.GET.get('status')
        if orderId and status:
            releaseOrderDao.updStatusFromReleaseOrderByOrderId(orderId, status)
            code, message = 200, '工单状态更新完成'
        else:
            raise Exception('参数报错: orderId, status 都不能为空')
    except Exception as e:
        code, data, message = 300, None, str(e)
    finally:
        return HttpResponse(JsonResponse(code=code, message=message, data=data).getJson())