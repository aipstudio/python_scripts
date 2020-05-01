#!/usr/bin/python
# -*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mail(p1):  # отправка уведомлений почтой
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    email_login = config.get('mail', 'username')
    email_pass = config.get('mail', 'password')
    email_to = config.get('mail', 'email_to')
    msg = MIMEMultipart()
    msg['From'] = email_login
    msg['To'] = email_to
    msg['Subject'] = "Warning Mining"
    body = p1
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    server.login(email_login, email_pass)
    text = msg.as_string()
    server.sendmail(email_login, email_to, text)
    server.quit()


    

if __name__ == '__main__':
    main()
