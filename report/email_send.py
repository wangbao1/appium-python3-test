# encoding: utf-8
'''
@author: lileilei
@file: email_send.py
@time: 2017/4/26 21:02
'''
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib, time, os


# 简单的格式化一个邮件地址
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def create_report_sendemali(from_addr, password, mail_to):
    msg = MIMEMultipart()
    msg['Subject'] = Header('博客测试报告', 'utf-8').encode()
    msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % mail_to)
    msg['Date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    msg.attach(MIMEText('这是 Python 发送的测试邮件……', 'plain', 'utf-8'))
    report_obj = open(r'xueshang.html', 'rb')
    mail_body_value = report_obj.read()
    # 创建附件，并添加到msg
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(mail_body_value)
    encoders.encode_base64(part)
    # 获取文件的文件名
    part.add_header('Content-Disposition', 'attachment; filename=xueshang.html')
    msg.attach(part)
    report_obj.close()

    server = smtplib.SMTP_SSL("smtp.163.com", 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, mail_to, msg.as_string())
    server.quit()

if __name__ == "__main__":
    create_report_sendemali('18510574788@163.com', 'Mf2468101', '583469256@qq.com')
