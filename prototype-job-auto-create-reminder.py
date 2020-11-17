#coding=utf-8 
import commands
import smtplib  
from email.mime.text import MIMEText 

#应用场景是每次有新的迭代，产品会在SVN指定文件夹下添加有规则的文件夹名，来存放产品原型
#每次需要新建一个Jenkins job来帮忙自动构建产品文档，生成一个HTML链接供所有人使用，省得使用SVN
#新版本来了，有时候会不能及时去新建这个job，所以需要邮件自动提醒

#specify email info
mailto_list=["abc@qq.com"] 
mail_host="smtp.163.com"
mail_user="robotium2016@163.com"
mail_pass="uiauxxx"
mail_postfix="163.com"

#method for sending mail
def send_mail(to_list,sub,content):  
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
output = commands.getoutput("svn info https://192.168.70.78/svn/Doc/Saas多学项目/V2.3.0 |grep 'non-existentd'")
#length 0 means folder exist, otherwise means folder not exist
if len(output) == 0:
    if send_mail(mailto_list,"产品原型自动化构建job创建提醒！！！","新版本开始，记得去Jenkins新建原型构建的job哦，么么哒！"):
        print "邮件发送成功"
    else:
        print "邮件发送失败"