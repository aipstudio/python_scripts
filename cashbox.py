#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import hmac
import hashlib
import base64
import datetime
from time import sleep

def main():
    url = 'https://cashbox.ru/webapi/v1/user/account/balance'
    result = req(url)
    print('Денег на счете = ', result['balance'])
    url = 'https://cashbox.ru/webapi/v1/task/326354'
    result = req(url)
    print('Денег в задаче = ', result['publishing']['paidTimes'] - result['publishing']['resultsCount'])
    url = 'https://cashbox.ru/webapi/v1/freetask/326354/reports/2'
    result = req(url)
    i = 0
    for id in result:
        url_check = f'https://cashbox.ru/webapi/v1/freetaskreport/{id}/confirm'
        i += 1
        req(url_check)
        #print('Отчет подтвержден = ', url_check)
    print('Подтверждено = ', i)


def req(url):
    PublicKey = b''
    SecretKey = b''
    dt = str(int(datetime.datetime.now().timestamp())) + '000'
    #md5 = base64.b64encode(hashlib.md5(SecretKey).digest())
    plaintStr = f'{PublicKey.decode("utf-8")}:GET:{url}:{dt}:'
    signature = base64.b64encode(
        hmac.new(SecretKey, plaintStr.encode('UTF-8'), hashlib.sha512).digest())
    h = {'Timestamp': dt,
         'Authorization': f'CashboxAuth {PublicKey.decode("UTF-8")}:{signature.decode("UTF-8")}', 'Content-Type': 'application/json', 'Connection': 'close'}
    r = requests.get(url, headers=h)
    #print(r.text)
    sleep(1)
    if url.find('confirm') == -1:
        return(r.json())
    else:
        return(r.text)


if __name__ == '__main__':
    main()

# GET:
#Timestamp: 1588925300544
# Authorization: CashboxAuth 'ваш PublicKey':n3RDovb0Ft4iN8wo6MEjsldaI17q7HrdUBwzSyK7hRI/UpcVBEckW6qlnNZg48cbz+crst8BbROXnWCGJmkOOA==

# POST:
#Timestamp: 1588925365555
# Authorization: CashboxAuth 'ваш PublicKey':O4t+V6/6c2gXlsUke7LF0N6OBgzF20I3v9J+59VBORDEz+hH/iYU+FMr4wyvBJjnVlufn8xuncArFT5hR31+og==
# Content-Type: application/json
