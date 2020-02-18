#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

def main():
    z = ZabbixAPI(config.get('ZABBIX', 'host'),user=config.get('ZABBIX', 'user'),password=config.get('ZABBIX', 'password'))
    hosts = z.host.get(groupids=34,output=['hostid','name']) #, hostids=13887
    for host in hosts:
        a = z.hostinterface.get(hostids=host['hostid'])
        if a[0]['ip'].find('10.55.10.') != -1 and a[0]['ip'] != '10.55.10.184' :
            print(a[0]['ip'])
            #z.host.delete(host['hostid'])

if __name__ == '__main__':
    main()