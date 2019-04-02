# -*- coding:utf-8 -*-
from django.db import models
import django.utils.timezone as timezone


#: 主机信息表
class HostInfo(models.Model):
    host_id = models.AutoField(primary_key=True, unique=True, verbose_name='主机id')
    salt_id = models.CharField(max_length=50, unique=True, null=False, verbose_name='salt名')
    host_name = models.CharField(max_length=50, verbose_name='主机名')
    alies_name = models.CharField(max_length=50, verbose_name='主机别名')
    vlan = models.ForeignKey(to="Vlan", to_field="id", related_name='vlan_id',
                                on_delete=models.CASCADE, null=True, verbose_name='vlan')
    ambient = models.ForeignKey(to="Ambient", to_field="id", related_name='ambient_id',
                                on_delete=models.CASCADE, null=True, verbose_name='环境')
    memory = models.IntegerField(null=True, verbose_name='内存')
    swap = models.IntegerField(null=True, verbose_name='交换分区')
    os_fullname = models.CharField(null=True, max_length=50, verbose_name='系统版本名')
    os_release = models.CharField(null=True, max_length=50, verbose_name='系统版本号')
    kernel_release = models.CharField(max_length=50, verbose_name='内核版本')
    cpu_model = models.CharField(max_length=50, verbose_name='cpu信息')
    cpus_number = models.IntegerField(null=True, verbose_name='cpu核数')
    host_type = models.CharField(max_length=50, verbose_name='主机类型')
    ssh_port = models.IntegerField(null=True, verbose_name='远程端口')
    state = models.IntegerField(default=0, verbose_name='主机状态')
    project_list = models.CharField(max_length=50, null=True, verbose_name='主机类型')
    delete = models.IntegerField(default=0, verbose_name='是否收集')
    remarks = models.CharField(max_length=200, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.salt_id

    class Meta:
        db_table = 'host_info'


#: 环境表
class Ambient(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    ambient_name = models.CharField(max_length=50, verbose_name='环境名')
    remarks = models.CharField(max_length=200, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.ambient_name

    class Meta:
        db_table = 'ambient'


#: 主机磁盘表
class DiskInfo(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    host = models.ForeignKey(to="HostInfo", to_field="host_id", related_name='disk_host',
                                on_delete=models.CASCADE, verbose_name='主机id')
    disk_name = models.CharField(null=True, max_length=50, verbose_name='磁盘名')
    size_gb = models.CharField(null=True, max_length=50, verbose_name='容量/GB')
    size_bytes = models.CharField(null=True, max_length=50, verbose_name='容量/bytes')
    state = models.IntegerField(default=0, verbose_name='状态1: 磁盘已不存在,状态0：磁盘使用中')

    def __str__(self):
        return self.disk_name

    class Meta:
        db_table = 'disk_info'


#: 主机网卡表
class Network(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    host = models.ForeignKey(to="HostInfo", to_field="host_id", related_name='network_host',
                                on_delete=models.CASCADE, verbose_name='主机id')
    network_name = models.CharField(max_length=50, verbose_name='网卡名')
    ip_address = models.CharField(max_length=50, verbose_name='ip地址')
    state = models.IntegerField(default=0, verbose_name='状态1: 网卡已不存在,状态0：网卡使用中')

    def __str__(self):
        return self.network_name

    class Meta:
        db_table = 'network'


#: vlan网段表
class Vlan(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    vlan_name = models.CharField(max_length=50, unique=True, verbose_name='vlan名')
    gateway = models.CharField(max_length=50, verbose_name='网关')
    network = models.CharField(max_length=50, verbose_name='子网')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.vlan_name

    class Meta:
        db_table = 'vlan'


#: 任务信息表
class TaskList(models.Model):
    task_id = models.AutoField(primary_key=True, unique=True, verbose_name='任务id')
    task_name = models.CharField(max_length=100, null=False, verbose_name='任务标题')
    task_state = models.IntegerField(default=0, verbose_name='任务状态')
    task_info = models.CharField(max_length=500, verbose_name='任务详情')
    create = models.ForeignKey(to="UserInfo", to_field="user_id", related_name='create_id',
                               on_delete=models.CASCADE, verbose_name='创建人')
    execute = models.ForeignKey(to="UserInfo", to_field="user_id", related_name='execute_id',
                                null=True, on_delete=models.CASCADE, verbose_name='处理人')
    authorizer = models.ForeignKey(to="UserInfo", to_field="user_id", related_name='authorizer_id', null=True,
                                   on_delete=models.CASCADE, verbose_name='授权人')
    remarks = models.CharField(max_length=500, null=True, verbose_name='任务备注')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    modify_date = models.DateTimeField(null=True, verbose_name='完成时间')

    def __str__(self):
        return self.task_name

    class Meta:
        db_table = 'task_list'


#: 任务日志信息表
class TaskLogList(models.Model):
    log_id = models.AutoField(primary_key=True, unique=True, verbose_name='日志id')
    task_id = models.IntegerField(null=False, verbose_name='任务id')
    execute = models.IntegerField(null=False, verbose_name='操作人')
    log_info = models.CharField(max_length=200, verbose_name='日志详情')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.log_id

    class Meta:
        db_table = 'task_log_list'


#: 用户信息表
class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True, verbose_name='用户id')
    group = models.ForeignKey(to="UserGroup", to_field="group_id", null=True,
                              on_delete=models.CASCADE, verbose_name='用户组Id')
    user_name = models.CharField(max_length=50, default='小样记得取名', verbose_name='用户名')
    password = models.CharField(max_length=100, null=False, verbose_name='密码')
    phone = models.CharField(max_length=50, verbose_name='手机号码')
    email = models.CharField(max_length=50, verbose_name='邮箱')
    state = models.IntegerField(default=1, verbose_name='用户状态')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'user_info'


#: 用户组表
class UserGroup(models.Model):
    group_id = models.AutoField(primary_key=True, unique=True, verbose_name='用户组id')
    role = models.ForeignKey(to="RoleInfo", to_field="role_id", null=True,
                              on_delete=models.CASCADE, verbose_name='角色Id')
    group_name = models.CharField(max_length=100, verbose_name='用户组名')
    remarks = models.CharField(max_length=500, null=True, verbose_name='备注')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'user_group'


#: 权限角色表
class RoleInfo(models.Model):
    role_id = models.AutoField(primary_key=True, unique=True, verbose_name='角色Id')
    role_name = models.CharField(max_length=100, verbose_name='角色名')
    api_list = models.CharField(max_length=500, null=True, verbose_name='api id json')
    remarks = models.CharField(max_length=500, null=True, verbose_name='备注')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'role_info'


#: api信息表
class ApiInfo(models.Model):
    api_id = models.AutoField(primary_key=True, unique=True, verbose_name='apiId')
    api_url = models.CharField(max_length=300, verbose_name='api url地址')
    api_name = models.CharField(max_length=300, null=True, verbose_name='api url名')
    remarks = models.CharField(max_length=500, null=True, verbose_name='备注')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    def __str__(self):
        return self.api_url

    class Meta:
        db_table = 'api_info'


#: 项目详情表
class ProjectInfo(models.Model):
    project_id = models.AutoField(primary_key=True, unique=True, verbose_name='项目Id')
    project_name = models.CharField(max_length=100, unique=True, verbose_name='项目名')
    project_path = models.CharField(max_length=300, null=True, verbose_name='项目路径')
    package_path = models.CharField(max_length=300, null=True, verbose_name='项目包路径')
    project_port = models.IntegerField(null=True, verbose_name='项目端口')
    project_type = models.IntegerField(null=True, verbose_name='项目类型')
    git = models.ForeignKey(to="GitInfo", to_field="git_id", null=True,
                               on_delete=models.CASCADE, verbose_name='gitId')
    github_url = models.CharField(max_length=200, null=True, verbose_name='github仓库地址')
    maven_path = models.CharField(max_length=200, null=True, verbose_name='maven获取包地址')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='更新时间')
    remarks = models.CharField(max_length=200, null=True, verbose_name='备注')

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'project_info'


#: 项目配置文件表
class ProjectSetting(models.Model):
    setting_id = models.AutoField(primary_key=True, unique=True, verbose_name='配置文件Id')
    project = models.ForeignKey(to="ProjectInfo", to_field="project_id", null=True,
                                   on_delete=models.CASCADE, verbose_name='项目Id')
    ambient = models.ForeignKey(to="Ambient", to_field="id", null=True,
                                   on_delete=models.CASCADE, verbose_name='环境Id')
    file_name = models.CharField(max_length=100, verbose_name='配置文件名')
    remote_path = models.CharField(max_length=200, verbose_name='配置文件远端路径')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='更新时间')
    remarks = models.CharField(max_length=200, null=True, verbose_name='备注')

    def __str__(self):
        return self.file_name

    class Meta:
        db_table = 'project_setting'
        unique_together = ["project", "ambient", "file_name"]


#: git账号信息表
class GitInfo(models.Model):
    git_id = models.AutoField(primary_key=True, unique=True, verbose_name='gitId')
    git_name = models.CharField(max_length=100, unique=True, verbose_name='git用户')
    git_key = models.CharField(max_length=100, null=True, verbose_name='git私钥')
    git_pass = models.CharField(max_length=150, null=True, verbose_name='git密码')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='更新时间')
    remarks = models.CharField(max_length=200, null=True, verbose_name='备注')

    def __str__(self):
        return self.git_name

    class Meta:
        db_table = 'git_info'


#: 发布工单信息表
class ReleaseOrder(models.Model):
    order_id = models.AutoField(primary_key=True, unique=True, verbose_name='发布工单Id')
    order_title = models.CharField(max_length=150, verbose_name='工单标题')
    order_content = models.CharField(max_length=300, verbose_name='工单内容')
    author = models.ForeignKey(to="UserInfo", to_field="user_id", related_name='author',
                               on_delete=models.CASCADE, verbose_name='工单创建人')
    executor = models.ForeignKey(to="UserInfo", to_field="user_id", related_name='executor',
                                 on_delete=models.CASCADE, verbose_name='任务执行人')
    product = models.ForeignKey(to="UserInfo", to_field="user_id", related_name='product',
                                on_delete=models.CASCADE, verbose_name='产品审核人')
    artisan = models.ForeignKey(to="UserInfo", to_field="user_id", related_name='artisan',
                                on_delete=models.CASCADE, verbose_name='技术审核人')
    ambient = models.ForeignKey(to="Ambient", to_field="id", related_name='ambient',
                                on_delete=models.CASCADE, verbose_name='环境Id')
    authorizer = models.CharField(max_length=50, default='''{"artisan": 1, "product": 1}''', verbose_name='授权状态')
    status = models.IntegerField(default=1, verbose_name='工单状态')
    ftp_path = models.CharField(max_length=100, null=True, verbose_name='ftp路径')
    remarks = models.CharField(max_length=300, null=True, verbose_name='备注')
    release_time = models.DateTimeField(verbose_name='发布时间')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='更新时间')

    def __str__(self):
        return self.order_title

    class Meta:
        db_table = 'release_order'


#: 监控item表
class Monitor(models.Model):
    id = models.AutoField(primary_key=True, unique=True, verbose_name='id')
    host = models.ForeignKey(to="HostInfo", to_field="host_id", related_name='monitor_host',
                                on_delete=models.CASCADE, verbose_name='主机id')
    cpu_use = models.CharField(max_length=50, verbose_name='CPU使用率')
    mem_use = models.CharField(max_length=50, verbose_name='内存使用率')
    load5 = models.CharField(max_length=50, verbose_name='5分钟内load值')

    class Meta:
        db_table = 'monitor_info'


#: 步骤模板
class StepTemp(models.Model):
    step_id = models.AutoField(primary_key=True, unique=True, verbose_name='步骤Id')
    step_name = models.CharField(max_length=100, verbose_name='步骤名')
    script_path = models.CharField(max_length=150, verbose_name='脚本路径')
    execute_count = models.IntegerField(default=1, verbose_name='执行次数,默认执行一次')
    execute_time = models.IntegerField(default=0, verbose_name='执行间隔时间,0代表没有间隔时间')
    update_time = models.DateTimeField(default=timezone.now, verbose_name='修改时间')
    remarks = models.CharField(max_length=200, null=True, verbose_name='备注')

    def __str__(self):
        return self.step_name

    class Meta:
        db_table = 'step_temp'


#: 步骤参数模板
class StepParameterTemp(models.Model):
    param_id = models.AutoField(primary_key=True, unique=True, verbose_name='参数Id')
    step = models.ForeignKey(to="StepTemp", to_field="step_id", related_name='step',
                             on_delete=models.CASCADE, verbose_name='步骤ID')
    param_name = models.CharField(max_length=100, verbose_name='参数中文解释')
    param_command = models.CharField(max_length=50, verbose_name='参数命令')
    is_null = models.CharField(max_length=50, default='false', verbose_name='是否为空,默认不能为空')

