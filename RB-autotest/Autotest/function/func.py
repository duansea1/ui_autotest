
from email.mime.text import MIMEText
from email.header import Header
import smtplib
from function import conf



def send_mail(subject,content,to_users):
    '''
    @param to_users: 多个收件人，以;分隔开'''
    #username=conf.get_local_value('exchangemail', 'username')
    useremail=conf.get_local_value('exchangemail', 'useremail')
    password=conf.get_local_value('exchangemail', 'password')

    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = useremail
    msg['To'] = ','.join(to_users)
    #msg['Cc'] = cc_user
    
    server = smtplib.SMTP()
    server.connect("smtp.exmail.qq.com")
#     server.connect("10.6.8.20")
    server.starttls()  
    server.login(useremail,password)  
    
    senders=server.sendmail(useremail, to_users, msg.as_string())
    print(senders)
    server.quit()
    return True