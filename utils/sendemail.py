import smtplib
import os
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from devops.settings import Email


# 发送邮件类
class SendEmail:
    #: 邮件配置初始化
    def __init__(self):
        self.mailHost = Email['email_host']  # 设置服务器
        self.mailUser = Email['email_user']  # 用户名
        self.mailPass = Email['email_password']  # 口令
        self.mailPostfix = Email['email_postfix']  # 发件箱的后缀

    #: subject: 邮件主题
    #: addressee: 收件人  列表类型
    #: data: 网页渲染的数据
    #: html: 网页
    def sendMail(self, subject, addressee, data, html):
        path = os.path.dirname(os.path.abspath(__file__))
        env = Environment(autoescape=False, loader=FileSystemLoader(os.path.join(path, '../templates')), trim_blocks=False)
        template = env.get_template(html)
        content = template.render(data=data)
        msg = MIMEText(content, _subtype='html', _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = "CMDB系统邮件<" + self.mailUser + ">"
        msg['To'] = ";".join(addressee)
        sendEmail = smtplib.SMTP()
        try:
            sendEmail.connect(self.mailHost)  # 连接smtp服务器
            sendEmail.login(self.mailUser, self.mailPass)  # 登陆服务器
            sendEmail.sendmail(self.mailUser, addressee, msg.as_string())  # 发送邮件
            return True
        except Exception as e:
            return e
        finally:
            sendEmail.close()
