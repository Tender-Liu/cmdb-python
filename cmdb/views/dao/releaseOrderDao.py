from django.utils import timezone
from cmdb.models import ReleaseOrder
import json
from django.core.paginator import Paginator


#: 发布工单分页查询，带模糊查询
def getListFromReleaseOrderByPage(page, count=10, orderTitle=None, status=None):
    filter_dict = dict()
    if orderTitle:
        filter_dict['order_title__contains'] = orderTitle
    if status:
        filter_dict['status'] = status
    releaseOederList = ReleaseOrder.objects.filter(**filter_dict).values("order_id", "order_title", "authorizer",
                                                                "status", "order_content", "release_time",).order_by("-update_time")
    paginator = Paginator(releaseOederList, count)
    pageList = paginator.page(number=page)
    for releaseOeder in pageList:
        if releaseOeder['authorizer'] == '{"artisan": 1, "product": 1}':
            releaseOeder['authorizer'] = 1
        elif releaseOeder['authorizer'] == '{"artisan": 2, "product": 2}':
            releaseOeder['authorizer'] = 3
        elif '-1' in releaseOeder['authorizer']:
            releaseOeder['authorizer'] = -1
        else:
            releaseOeder['authorizer'] = 2
    return pageList, paginator.num_pages


#: 查询指定orderId的工单信息
def getAllFromReleaseOrderByOrderId(orderId):
    releaseOrder = ReleaseOrder.objects.values("order_id", "order_title", "order_content", "authorizer", "status", "ftp_path",
                                    "ambient_id", "ambient__ambient_name" ,"artisan_id", "artisan__user_name", "author_id",
                                    "author__user_name", "executor_id", "executor__user_name", "product_id", "product__user_name",
                                    "release_time", "update_time","remarks").get(order_id=orderId)
    releaseOrder['authorizerList'] = json.loads(releaseOrder['authorizer'], encoding='utf-8')
    if -1 in releaseOrder['authorizerList'].values():
        releaseOrder['authorizer'] = -1
    elif releaseOrder['authorizerList']['artisan'] == 1 and releaseOrder['authorizerList']['product'] == 1:
        releaseOrder['authorizer'] = 1
    elif releaseOrder['authorizerList']['artisan'] == 2 and releaseOrder['authorizerList']['product'] == 2:
        releaseOrder['authorizer'] = 3
    else:
        releaseOrder['authorizer'] = 2
    return releaseOrder


#: 添加发布工单信息
def setFromReleaseOrder(orderTitle, orderContent, releaseTime, ambientId, executorId,
                        artisanId, authorId, productId, remarks=None, ftpPath=None):
    releaseOrder = ReleaseOrder.objects.create(
        order_title=orderTitle,
        order_content=orderContent,
        release_time=releaseTime,
        ftp_path=ftpPath,
        ambient_id=ambientId,
        executor_id=executorId,
        artisan_id=artisanId,
        author_id=authorId,
        product_id=productId,
        remarks=remarks
    )
    releaseOrder.save()
    return releaseOrder.order_id


#: 删除发布工单信息
def delFromReleaseOrderByOrderId(orderId):
    releaseOrder = ReleaseOrder.objects.get(order_id=orderId)
    if releaseOrder.status == 3 or releaseOrder.status == 2:
        raise Exception("工单报错: 工单处于运行状态或等待执行状态，无法删除工单")
    releaseOrder.save()


#: 指定orderId, 修改工单内容
def updContentFromReleaseOrdeByOrderId(orderId, orderTitle, orderContent, ambientId,releaseTime,
                                       executorId, artisanId, productId, ftpPath=None, remarks=None):
    releaseOrder = ReleaseOrder.objects.get(order_id=orderId)
    authorizerList = json.loads(releaseOrder.authorizer, encoding='utf-8')
    if authorizerList['artisan'] == 2 and authorizerList['product'] == 2:
        raise Exception("工单报错: 工单已经通过授权，不能再修改工单内容，如有疑问，请联系运维！")
    if orderTitle:
        releaseOrder.order_title = orderTitle
    if orderContent:
        releaseOrder.order_content = orderContent
    if ambientId:
        releaseOrder.ambient_id = ambientId
    if releaseTime:
        releaseOrder.release_time = releaseTime
    if executorId:
        releaseOrder.executor_id = executorId
    if productId:
        releaseOrder.product_id = productId
    if artisanId:
        releaseOrder.artisan_id = artisanId
    releaseOrder.ftp_path = ftpPath
    releaseOrder.remarks = remarks
    releaseOrder.update_time = timezone.now()
    releaseOrder.save()


#: 指定orderId,修改工单授权
def updAuthorizerFromReleaseOrdeByOrderId(userId, orderId, authorizer):
    releaseOrder = ReleaseOrder.objects.get(order_id=orderId)
    if releaseOrder.artisan_id != userId and releaseOrder.product_id != userId:
        raise Exception("工单报错: 你没有权限授权次工单！")
    authorizerList = json.loads(releaseOrder.authorizer, encoding='utf-8')
    if releaseOrder.artisan_id == userId:
        authorizerList['artisan'] = authorizer
    if releaseOrder.product_id == userId:
        authorizerList['product'] = authorizer
    releaseOrder.authorizer = json.dumps(authorizerList)
    releaseOrder.update_time = timezone.now()
    releaseOrder.save()


#: 指定orderId,修改工单状态
def updStatusFromReleaseOrderByOrderId(orderId, status):
    if 0 > int(status) or int(status) > 6:
        raise Exception("工单报错: 无法识别的工单状态！")
    releaseOrder = ReleaseOrder.objects.get(order_id=orderId)
    if releaseOrder.authorizer != '{"artisan": 1, "product": 1}':
        raise Exception("工单报错: 工单授权暂未通过,无法修改工单状态!")
    releaseOrder.status = status
    releaseOrder.update_time = timezone.now()
    releaseOrder.save()
