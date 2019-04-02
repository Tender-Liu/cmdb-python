# _*_ coding:utf-8 _*_
from django.urls import path
from cmdb.views.controller import userInfoController
from cmdb.views.controller import taskListController
from cmdb.views.controller import hostInfoController
from cmdb.views.controller import saltController
from cmdb.views.controller import ambientController
from cmdb.views.controller import vlanController
from cmdb.views.controller import monitorInfoController
from cmdb.views.controller import apiInfoController
from cmdb.views.controller import roleInfoController
from cmdb.views.controller import userGroupController
from cmdb.views.controller import projectInfoController
from cmdb.views.controller import projectSettingController
from cmdb.views.controller import gitInfoController
from cmdb.views.controller import releaseOrderController
from cmdb.views.controller import monitorDashController



urlpatterns = []

#: 用户API
urlpatterns += [
    #: 添加用户
    path('userInfo/setFromUserInfo', userInfoController.setFromUserInfo),
    #: 更新用户信息
    path('userInfo/updInfoFromUserInfo', userInfoController.updInfoFromUserInfo),
    #: 用户登录验证
    path('userInfo/getFromUserInfoByLogin', userInfoController.getFromUserInfoByLogin),
    #: 注销登录
    path('userInfo/delFromSessionByKey', userInfoController.delFromSessionByKey),
    #: 查询指定用户信息-管理员使用
    path('userInfo/getAllFromUsreInfoByUserId', userInfoController.getAllFromUsreInfoByUserId),
    #: 获取所有用户id与用户名
    path('userInfo/getAllUserInfo', userInfoController.getAllUserInfo),
    #: 用户信息查询分页功能，模糊查询
    path('userInfo/getAllFromUserInfoByPage', userInfoController.getAllFromUserInfoByPage),
    #: 修改用户密码
    path('userInfo/updPassWordFromUserInfo', userInfoController.updPassWordFromUserInfo),
    #: 查询个人用户信息
    path('userInfo/getAllFromUsreInfoByMyself', userInfoController.getAllFromUsreInfoByMyself),
    #: 管理员修改用户密码重置
    path('userInfo/updPassWordFromUserInfoByUserId', userInfoController.updPassWordFromUserInfoByUserId),
    #: 管理员修改用户分组
    path('userInfo/updGroupFromUserInfoByUserId', userInfoController.updGroupFromUserInfoByUserId),
]


#: 任务列表API URL
urlpatterns += [
    #: 返回所有任务count
    path('taskList/getCountFromTaskList', taskListController.getCountFromTaskList),
    #: 返回所有任务各种状态count
    path('taskList/getCountFromTaskListByTaskState', taskListController.getCountFromTaskListByTaskState),
    #: 返回指定任务详情
    path('taskList/getAllFromTaskListByTaskId', taskListController.getAllFromTaskListByTaskId),
    #: 添加任务
    path('taskList/setAllFromTaskList', taskListController.setAllFromTaskList),
    #: 更新任务信息
    path('taskList/updAllFromTaskListByTaskId', taskListController.updAllFromTaskListByTaskId),
    #: 更新任务状态
    path('taskList/updTaskStateFromTaskListByTaskId', taskListController.updTaskStateFromTaskListByTaskId),
    #: 查询任务操作日志
    path('taskList/getAllFromTaskLogListByTaskId', taskListController.getAllFromTaskLogListByTaskId),
    #: 添加任务操作日志
    path('taskList/setAllFromTaskLogListByTaskId', taskListController.setAllFromTaskLogListByTaskId),
    #: 任务分页查询
    path('taskList/getAllFromTaskListByPage', taskListController.getAllFromTaskListByPage),
]


#: 主机信息操作api
urlpatterns += [
    #: 查看分页主机资源信息
    path('hostInfo/getAllHostInfoByPage', hostInfoController.getAllHostInfoByPage),
    #: 查看指定主机详情包含ip列表与disk列表
    path('hostInfo/getAllHostInfoByHostId', hostInfoController.getAllHostInfoByHostId),
    #: 更新指定主机详情
    path('hostInfo/updHostInfoByHostId', hostInfoController.updHostInfoByHostId),
    #: 查看指定主机详情
    path('hostInfo/getHostInfoByHostId', hostInfoController.getHostInfoByHostId),
]


#: saltAPI
urlpatterns += [
    #: 检查新主机，返回saltId
    path('salt/getNewSaltId', saltController.getNewSaltId),
    #: 收集指定saltId主机信息
    path('salt/setNewHostInfo', saltController.setNewHostInfo),
    #: 更新所有数据库中存在的主机资源
    path('salt/updAllHostInfoBySalt', saltController.updAllHostInfoBySalt),
    #: salt执行指定主机执行操作命令
    path('salt/getCommandFromSaltBySaltIdList', saltController.getCommandFromSaltBySaltIdList),
    #: salt收集与更新主机项目列表
    path('salt/getProjectListFromHostInfoBySalt', saltController.getProjectListFromHostInfoBySalt),
]


#: 环境操作API
urlpatterns += [
    #: 添加Ambient
    path('ambient/setFromAmbient', ambientController.setFromAmbient),
    #: 删除Ambient
    path('ambient/delFromAmbientById', ambientController.delFromAmbientById),
    #: 查看Ambient
    path('ambient/getAllFromAmbient', ambientController.getAllFromAmbient),
    #: 更新Ambient
    path('ambient/updAllFromAmbientById', ambientController.updAllFromAmbientById),
    #: 查看指定的Ambient
    path('ambient/getAllFromAmbientById', ambientController.getAllFromAmbientById),
    #: 查看分页Ambient信息
    path('ambient/getAllFromAmbientByPage', ambientController.getAllFromAmbientByPage),
]


#: Vlan操作API
urlpatterns += [
    #: 添加Vlan
    path('vlan/setFromVlan', vlanController.setFromVlan),
    #: 删除Vlan
    path('vlan/delFromVlanById', vlanController.delFromVlanById),
    #: 查看Vlan分页信息
    path('vlan/getAllFromVlanByPage', vlanController.getAllFromVlanByPage),
    #: 更新Vlan
    path('vlan/updAllFromVlanById', vlanController.updAllFromVlanById),
    #: 查看指定的Vlan
    path('vlan/getAllFromValnById', vlanController.getAllFromValnById),
    #: 查看所有vlan信息
    path('vlan/getIdAndVlanNameFromVlan', vlanController.getIdAndVlanNameFromVlan),
]

#: 主机监控操作api
urlpatterns += [
    #: 一键安装主机
    path('monitorInfo/createHost', monitorInfoController.createHost),
    # 获取资源信息
    path('monitorInfo/getAllHostInfoByPage', monitorInfoController.getAllHostInfoByPage),
    #资源大盘
    path('monitorDash/getMonitorItem', monitorDashController.getMonitorItem),

]


#: apiInfo操作api
urlpatterns += [
    #: 根据apiId查询api信息
    path('apiInfo/getAllFromApiInfoByApiId', apiInfoController.getAllFromApiInfoByApiId),
    #: 添加api信息
    path('apiInfo/setFromApiInfo', apiInfoController.setFromApiInfo),
    #: 根据apiId更新api信息
    path('apiInfo/updAllFromApiInfoByApiId', apiInfoController.updAllFromApiInfoByApiId),
    #: 根据apiId删除指定api信息
    path('apiInfo/delFromApiInfoByApiId', apiInfoController.delFromApiInfoByApiId),
    #: apiInfo分页查询带模糊查询功能
    path('apiInfo/getListFromApiInfoByPage', apiInfoController.getListFromApiInfoByPage),
]


#: roleInfo操作api
urlpatterns += [
    #: 根据apiId查询角色信息
    path('roleInfo/getAllFromRoleInfoByRoleId', roleInfoController.getAllFromRoleInfoByRoleId),
    #: 根据roleId查询角色信息与角色权限详情
    path('roleInfo/getAllFromRoleInfoAndApiInfoByRoleId', roleInfoController.getAllFromRoleInfoAndApiInfoByRoleId),
    #: 根据apiId查询角色信息
    path('roleInfo/getAllFromRoleInfoAndApiInfoByRoleId', roleInfoController.getAllFromRoleInfoAndApiInfoByRoleId),
    #: 添加api信息
    path('roleInfo/setFromRoleInfo', roleInfoController.setFromRoleInfo),
    #: 根据apiId更新角色信息
    path('roleInfo/updAllFromRoleInfoByRoleId', roleInfoController.updAllFromRoleInfoByRoleId),
    #: 根据apiId删除指定角色信息
    path('roleInfo/delFromRoleInfoByRoleId', roleInfoController.delFromRoleInfoByRoleId),
    #: apiInfo分页查询带模糊查询功能
    path('roleInfo/getListFromRoleInfoByPage', roleInfoController.getListFromRoleInfoByPage),
    #: 查询全部角色id与角色名
    path('roleInfo/getRoleIdAndRoleNameFromRoleInfo', roleInfoController.getRoleIdAndRoleNameFromRoleInfo),
    #: 根据roleId查询角色信息与角色拥有的权限详情与未拥有的权限详情
    path('roleInfo/getListFromRoleInfoAndApiInfoByRoleId', roleInfoController.getListFromRoleInfoAndApiInfoByRoleId),
    #: 添加角色权限
    path('roleInfo/addApiListFromRoleIdByRoleId', roleInfoController.addApiListFromRoleIdByRoleId),
    #: 删除角色权限
    path('roleInfo/delApiListFromRoleIdByRoleId', roleInfoController.delApiListFromRoleIdByRoleId),
]


#: 用户组操作api
urlpatterns += [
    #: 根据groupId查询查询用户组信息
    path('userGroup/getAllFromUserGroupByGroupId', userGroupController.getAllFromUserGroupByGroupId),
    #: 添加用户分组信息
    path('userGroup/setFromUserGroup', userGroupController.setFromUserGroup),
    #: 根据groupId更新用户信息
    path('userGroup/updAllFromUserGroupByGroupId', userGroupController.updAllFromUserGroupByGroupId),
    #: 根据groupId删除角色信息
    path('userGroup/delFromUserGroupByGroupId', userGroupController.delFromUserGroupByGroupId),
    #: 用户组分页查询带模糊查询功能
    path('userGroup/getListFromUserGroupByPage', userGroupController.getListFromUserGroupByPage),
    #: 获取所有用户组与用户组Id
    path('userGroup/getGroupIdAndGroupNameFromUserGroup', userGroupController.getGroupIdAndGroupNameFromUserGroup),
]


#: 项目信息操作API
urlpatterns += [
    #: 查看分页项目信息
    path('projectInfo/getAllFromProjectInfoByPage', projectInfoController.getAllFromProjectInfoByPage),
    #: 添加项目信息
    path('projectInfo/setFromProjectInfo', projectInfoController.setFromProjectInfo),
    #: 更新项目信息
    path('projectInfo/updFromProjectInfoByProjectId', projectInfoController.updFromProjectInfoByProjectId),
    #: 删除项目信息
    path('projectInfo/delFromProjectInfoByProjectId', projectInfoController.delFromProjectInfoByProjectId),
    #: 查看指定项目信息
    path('projectInfo/getAllFromProjectInfoByProjectId', projectInfoController.getAllFromProjectInfoByProjectId),
    #: 获取全部项目id与项目名
    path('projectInfo/getProjectNameFromProjectInfo', projectInfoController.getProjectNameFromProjectInfo),
    #: 查询所有指定的gitId的项目
    path('projectInfo/getAllFromProjectNameFromGitId', projectInfoController.getAllFromProjectNameFromGitId),
]


#: 项目配置文件操作API
urlpatterns += [
    #: 分页查询项目配置文件信息，包含项目以及配置文件名模糊匹配
    path('projectSetting/getAllFromProjectSettingByPage', projectSettingController.getAllFromProjectSettingByPage),
    #: 添加项目配置文件
    path('projectSetting/addFromProjectSettingByProjectIdAndAmbientId', projectSettingController.addFromProjectSettingByProjectIdAndAmbientId),
    #: 编辑配置文件 #内容#
    path('projectSetting/editFromProjectSettingByProjectId', projectSettingController.editFromProjectSettingByProjectId),
    #: 查看指定文件 #内容#
    path('projectSetting/getContentFromProjectSettingByProjectId',projectSettingController.getContentFromProjectSettingByProjectId),
    #: 查看指定配置  #文件信息#
    path('projectSetting/getAllFromProjectSettingByProjectId',projectSettingController.getAllFromProjectSettingByProjectId),
    #: 修改指定配置 #文件信息#
    path('projectSetting/updFromProjectSettingByProjectId',projectSettingController.updFromProjectSettingByProjectId),
    #: 删除配置文件
    path('projectSetting/delFromProjectSettingByProjectId',projectSettingController.delFromProjectSettingByProjectId),
]


#: git信息操作API
urlpatterns += [
    #: 添加git信息
    path('gitInfo/addFromGitInfo', gitInfoController.addFromGitInfo),
    #: 删除git信息
    path('gitInfo/delFromGitInfoByGitId', gitInfoController.delFromGitInfoByGitId),
    #: 更新git信息
    path('gitInfo/updAllFromGitInfoByGitId', gitInfoController.updAllFromGitInfoByGitId),
    #: 查询指定git信息
    path('gitInfo/getAllFromGitInfoByGitId', gitInfoController.getAllFromGitInfoByGitId),
    #: 查询所有git名称，前端使用
    path('gitInfo/getGitNameFromGitInfo', gitInfoController.getGitNameFromGitInfo),
    #: 分页查询,带模糊查询
    path('gitInfo/getAllFromGitInfoByPage', gitInfoController.getAllFromGitInfoByPage),
    #: 根据项目id，获取所有git分支名
    path('gitInfo/getBranchsFromGitByProjectId', gitInfoController.getBranchsFromGitByProjectId),
]


#: 发布工单信息操作API
urlpatterns += [
    #: 查询指定orderId的工单信息
    path('releaseOrder/getAllFromReleaseOrderByOrderId', releaseOrderController.getAllFromReleaseOrderByOrderId),
    #: 添加发布工单信息
    path('releaseOrder/setFromReleaseOrder', releaseOrderController.setFromReleaseOrder),
    #: 发布工单分页查询，带模糊查询
    path('releaseOrder/getListFromReleaseOrderByPage', releaseOrderController.getListFromReleaseOrderByPage),
    #: 删除发布工单信息
    path('releaseOrder/delFromReleaseOrderByOrderId', releaseOrderController.delFromReleaseOrderByOrderId),
    #: 指定orderId, 修改工单内容
    path('releaseOrder/updContentFromReleaseOrdeByOrderId', releaseOrderController.updContentFromReleaseOrdeByOrderId),
    #: 指定orderId,修改工单授权
    path('releaseOrder/updAuthorizerFromReleaseOrdeByOrderId', releaseOrderController.updAuthorizerFromReleaseOrdeByOrderId),
    #: 指定orderId,修改工单状态
    path('releaseOrder/updStatusFromReleaseOrderByOrderId', releaseOrderController.updStatusFromReleaseOrderByOrderId),
]