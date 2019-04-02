### cmdb  #: 资源管控

    1.views  #: 视图
        1.controller  #: 编写api请求层代码，保证数据传入，如输出规范
        2.dao  #: 连接orm数据操作
        3.models  #: 表结构
        4.urls #: api地址

### devops  #: 主项目配置中心
   
### sdk_api #: 各项目api接入中心

# utils   #：工具类

    1.DataEncoder 解决orm时间格式转换json格式
    2.JsonResponse 统计api输出json格式化
    3.UserSession session会话登录验证

### 部署方法
1.项目部署请修改settings中DATABASES连接的数据库地址

```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'devops',
            'USER': 'root',
            'PASSWORD': 'admin123',
            'HOST': '172.28.5.190',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4'
            }
        }
    }
 ```


2.请修改saltAPI类中saltapi地址

```
    #: 类变量定义
    def __init__(self):
        self.__url = 'https://172.28.5.190:8000'
        self.__user = 'saltapi'
        self.__password = 'saltapi'
```        

3.pip安装依赖组件

    pip install Django==2.1.3
    pip install Jinja2==2.10
    pip install urllib3==1.24.1
    pip install PyMySQL==0.9.2
    
4.数据库同步

    python manage.py makemigrations cmdb
    python manage.py migrate
    如果同步失败，请删除cmdb中migrations与__pycache__文件夹中的文件
    
5.启动项目

    python manage.py runserver 0.0.0.0:8080
