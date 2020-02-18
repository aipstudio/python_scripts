#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
import math
from pyzabbix import ZabbixAPI
result = q1 = q2 = q3 = q4 = q5 = ''
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')


def main():
    global result, q1, q2, q3, q4, q5, q6
    z = ZabbixAPI(config.get('ZABBIX', 'host'))
    z.login(user=config.get('ZABBIX', 'user'),
            password=config.get('ZABBIX', 'password'))
    f = open('result.txt', 'w', encoding="utf-8")
    f.flush
    hosts = z.host.get(groupids=34, output=['hostid', 'name'])
    for host in hosts:
        items = z.item.get(hostids=host['hostid'],
                           filter={
                               'name': [
                                   'HW CPU Name', 'HW Baseboard',
                                   'Total memory', 'System information',
                                   'Oracle - Size Dir',
                                   'Oracle scripts - free space warning',
                                   'Oracle scripts - scheduler no work job'
                               ]
                           },
                           output=['itemid', 'name', 'lastvalue'])
        q1 = q2 = q3 = q4 = q5 = q6 = ''
        for item in items:
            if item['name'] == 'HW CPU Name':
                q1 = item['lastvalue'] + ' | '
            if item['name'] == 'HW Baseboard':
                q2 = item['lastvalue'] + ' | '
            if item['name'] == 'Total memory':
                q3 = str(round(int(item['lastvalue']) / 1024 / 1024 / 1024,
                               1)) + ' Gb | '
            if item['name'] == 'System information':
                q4 = item['lastvalue'] + ' | '
            if item['name'] == 'Oracle - Size Dir':
                q5 = str(
                    round(float(item['lastvalue']) / 1024 / 1024 / 1024,
                          1)) + ' Gb | '
            if item['name'] == 'Oracle scripts - scheduler no work job':
                # if item['name'] == 'Oracle scripts - free space warning':
                q6 = item['lastvalue'].replace("\r", " ").replace("\n",
                                                                  " ") + ' | '
            result = host['name'] + ' | ' + q1 + q2 + q3 + q4 + q5 + q6 + "\n"
        f.write(result)
    f.close()


if __name__ == '__main__':
    main()
