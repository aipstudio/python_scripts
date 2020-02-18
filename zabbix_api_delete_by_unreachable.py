#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyzabbix import ZabbixAPI
import datetime
from datetime import timedelta
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

def main():
    i = 0 
    z = ZabbixAPI(config.get('ZABBIX', 'host'),user=config.get('ZABBIX', 'user'),password=config.get('ZABBIX', 'password'))
# z.login(user="zabbix_api", password="AYfIMePZ7xzQ")   
    for trigger in z.trigger.get(output=['triggerid', 'description', 'priority','lastchange'], groupids=34, filter={"value":1},sortfield='lastchange'):
        if trigger['description'] == 'Zabbix agent on {HOST.NAME} is unreachable':
            trigmsg = z.trigger.get(triggerids= trigger['triggerid'], selectHosts= 'extend')
            lastchange = datetime.datetime.fromtimestamp(int(trigger['lastchange']))
            dt = datetime.datetime.now()
            if lastchange < dt - timedelta(days=3):
                for tm in trigmsg:
                    for l in tm['hosts']:
                        i = i + 1
                        print (l['name'], l['hostid'])
                        #z.host.delete(int(l['hostid']))
    print ("All remove hosts: " + str(i))

if __name__ == '__main__':
    main()