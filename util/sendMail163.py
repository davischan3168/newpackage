import smtplib
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart
import os
import time
import sys
ISOTIMEFORMAT='%Y%m%d'

def sentemail_attachment(host = 'smtp.163.com',port = 465 ,\
                             sender = 'chenzuliang@163.com',
                             pwd = 'chen&801019',
                             receiver ='racheal123_54@kindle.cn',
                             filename='30个不同学术观点的理论展示(1).txt'):
    caodate=str(time.strftime(ISOTIMEFORMAT, time.localtime()))
    body = '<h1>'+caodate+'</h1><p>zhongfs</p>' 
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html') 
    # 设置正文为符合邮件格式的HTML内容
    if filename==None:
        msg['subject'] = '打卡通知' 
        # 设置邮件标题
        msg['from'] = sender  
        # 设置发送人
        msg['to'] = receiver  
        # 设置接收人
        try:
            s = smtplib.SMTP_SSL(host, port)  
            # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
            s.login(sender, pwd)  
            # 登陆邮箱
            s.sendmail(sender, receiver, msg.as_string())
            # 发送邮件！
            print ('Done.sent email success')
        except smtplib.SMTPException:
            print ('Error.sent email fail')

    elif os.path.isfile(filename):        
        message = MIMEMultipart() 
        message['subject'] = caodate+'下载附件通知' 
        # 设置邮件标题
        message['from'] = sender  
        # 设置发送人
        message['to'] = receiver
        # 设置接收人 
        message.attach(msg)
        # 构造附件1，传送当前目录下的 test.txt 文件
        att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1.add_header("Content-Disposition","attachment",filename='%s'%filename)
        message.attach(att1)
        try:
            s = smtplib.SMTP_SSL(host, port)
            s.login(sender, pwd)
            s.sendmail(sender, receiver, message.as_string())
            print ('Done.sent email success')
        except smtplib.SMTPException:
	        print ('Error.sent email fail')
    else:
        print('Something wrong with %s'%filename)
    return


        
if __name__ == '__main__':
    path=sys.argv[1]
    if os.path.splitext(path)[1].lower() in ['.docx','.html']:
        npath=os.path.splitext(path)[0]+'.mobi'
        os.system('ebook-convert %s %s'%(path,npath))
        sentemail_attachment(filename=npath)
