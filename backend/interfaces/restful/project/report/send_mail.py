# Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, mail_client):
        # 邮箱服务器地址
        self.mailServer = mail_client['mail_server']
        # 邮箱服务器端口
        self.port = mail_client['port']
        # 邮箱用户名
        self.user = mail_client['username']
        # 邮箱密码
        self.pwd = mail_client['password']
        self.conn = None

    def send_mail(self, mail_from, mail_to, msg):
        # 构造邮箱对象
        self.conn = smtplib.SMTP()
        # 连接网易邮箱服务器
        self.conn.connect(self.mailServer, self.port)
        # 打印出和SMTP服务器交互的所有信息
        self.conn.set_debuglevel(1)
        # 登录网易邮箱
        self.conn.login(self.user, self.pwd)
        # 发送邮件
        self.conn.sendmail(mail_from, mail_to, msg.as_string())
        # 回收资源
        self.conn.close()

    def send_text(self, config):
        msg = MIMEMultipart()
        # 构造MIMETextweb文本对象
        context = MIMEText(config['mail_text'], 'plain', 'utf-8')
        msg.attach(context)
        # 配置发送方
        me = formataddr((Header('接口测试报告', 'utf-8').encode(), config['mail_from']))
        msg['From'] = me
        # 配置接收方
        msg['To'] = ",".join(config['mail_to'])
        # 配置主题
        msg['Subject'] = Header(config['mail_subject'], 'utf-8').encode()
        att1 = MIMEText(config["render_content"], 'plain', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment;filename=' + config["report_name"]

        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字，filename[-6:]指的是之前附件地址的后6位
        msg.attach(att1)
        # 发送邮件
        self.send_mail(me, config['mail_to'], msg)


class MailSend:
    def __init__(self, config):
        self.config = config
        # 1、初始化网易邮箱
        self.mail_didngding = {'mail_server': 'smtp.mxhichina.com',
                               'port': 25,
                               'username': self.config["mail_from"],
                               'password': self.config["password"]}  # 使用网易邮箱的第三方需要授权码作为口令

    def send(self):
        mail = Mail(self.mail_didngding)
        # 2、初始化邮件发送配置
        mail_config = {
            'mail_subject': "WaykiChain API Test",
            'mail_from': self.config["mail_from"],
            'mail_to': self.config["mail_to"],
            'mail_text': self.config["description"],
            'report_name': self.config["report_name"],
            'render_content': self.config["render_content"],
        }
        # 3、发送邮件
        mail.send_text(mail_config)


if __name__ == '__main__':
    config = {
        "mail_from": 'linxin.jiang@waykichainhk.com',
        "password": 'Tiger@Waykichain',
        "mail_to": ['linxin.jiang@waykichainhk.com'],
        "render_content": "7777",
        "report_name": "swagger.html",
        "description": "接口测试报告"
    }
    mail = MailSend(config)
    mail.send()
