#!/usr/bin/python
# coding:utf-8  

 
import smtplib 
import string 


HOST = "smtp.raisecom.com" #定义smtp主机 
SUBJECT = "Test email from Python" #定义邮件主题 
TO = "hushouqiang@raisecom.com" #定义邮件收件人 
FROM = "hushouqiang@raisecom.com" #定义邮件发件人 
text = "Python rules them all 胡守强!" #邮件内容 
BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        text
        ),"\r\n") #组装 sendmail 方法的邮件主体内容, 各段以"\r\n" 进行 分隔 
    
server = smtplib.SMTP() #创建 一个 SMTP() 对象 
server.connect( HOST,"25") #通过 connect 方法连接smtp主机 
#server.starttls() #启动安全传输模式 
server.login("004668","Lan2017sum") #邮箱账号登录校验 
#print BODY
server.sendmail( FROM, [TO], BODY) #邮件发送 
server.quit() #断开smtp连接 

