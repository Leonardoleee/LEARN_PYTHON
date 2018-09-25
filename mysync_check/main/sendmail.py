#!/usr/bin/env python
# coding=utf-8

import os, sys
import time
from collections import OrderedDict
import datetime
import logging
from email.header import Header
from smtplib import SMTP_SSL
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



logger = logging.getLogger('syncinfo')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('sync.log')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


time_stamp = time.strftime("%Y-%m-%d", time.localtime())
def send_mail():
    #163邮箱smtp服务器
	host_server = 'smtp.163.com'
	#sender_163为发件人的163号码
	sender_163 = '18506582337@163.com'
	#pwd为163邮箱的授权码
	pwd = '0okmnhy6'
	#发件人的邮箱
	sender_163_mail = '18506582337@163.com'
	#收件人邮箱
	receiver = 'lilaibang@wanmagroup.com, huangyipeng@wanmagroup.com'
	# 邮件的正文内容
	mail_content = "mysql sync info"
	# 邮件标题
	mail_title = 'mysql同步信息'
	#接收邮件列表,是list,不是字符串 
	mail_to  = ['lilaibang@wanmagroup.com', 'huangyipeng@wanmagroup.com']     

	# 邮件正文内容
	# msg = MIMEMultipart()
	msg = MIMEMultipart('related')
	msg["Subject"] = Header(mail_title, 'utf-8')
	msg["From"] = sender_163_mail
	# 收件人，必须是一个字符串
	msg["To"] = ','.join(mail_to)         

	msgAlternative = MIMEMultipart('alternative')
	msg.attach(msgAlternative)

	# 邮件正文内容
	mail_body = """
	<p> - 数据库同步状态检查 - </p>
	"""

	#msg.attach(MIMEText(mail_body, 'html', 'utf-8'))
	msgText = (MIMEText(mail_body, 'html', 'utf-8'))
	msgAlternative.attach(msgText)

	# 指定图片为当前目录
	# fp = open('./pic/utilization.png', 'rb')
        # msgImage = MIMEImage(fp.read())
	# fp.close()

	# 定义图片 ID，在 HTML 文本中引用
	# msgImage.add_header('Content-ID', '<send_image>')
	#msg.attach(msgImage)

	# 构造附件1，传送当前目录下的 attach.txt 文件
	att1 = MIMEText(open("/home/app/script/mysync_check/sync_info_" + time_stamp + ".html", 'rb').read(), 'base64', 'utf-8')
	att1["Content-Type"] = 'application/octet-stream'
	# 这里的filename可以任意写，写什么名字，邮件中显示什么名字
	att1["Content-Disposition"] = 'attachment; filename="sync_status.html"'
	msg.attach(att1)

	# ssl登录
	smtp = SMTP_SSL(host_server)
	# set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
	smtp.set_debuglevel(0)
	smtp.ehlo(host_server)
	smtp.login(sender_163, pwd)

	smtp.sendmail(sender_163_mail, mail_to, msg.as_string())
	smtp.quit()


