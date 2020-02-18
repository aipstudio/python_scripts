import imaplib,configparser

def check_mail():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8-sig')
    email_login = config.get('mail', 'username')
    email_pass = config.get('mail', 'password')
    email_to = config.get('mail', 'email_to')
    server = imaplib.IMAP4_SSL ('imap.yandex.ru', 993)
    server.login(email_login, email_pass)
    server.select("inbox")
    status, messages = server.search(None, '(UNSEEN)')
    r = messages[0].split()
    server.logout()
    return (len(r))

print(check_mail())
