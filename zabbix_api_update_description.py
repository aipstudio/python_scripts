#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
import psycopg2
import os
from pyzabbix import ZabbixAPI

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')


def get_ou_pg():
    conn = psycopg2.connect(dbname=config.get('PG', 'db'),
                            user=config.get('PG', 'user'),
                            password=config.get('PG', 'password'),
                            host=config.get('PG', 'host'),
                            port='5432')
    with conn:
        with conn.cursor() as cur:
            sql = '''select ''|| 'ou' || p.id , p.fullname from basis.t_partner p
                     where (p.partner_e_mail like 'af%%@%' or p.partner_e_mail like 'fk%%@%')
                     order by p.id;
                     ''' #and p.id = 17860
            cur.execute(sql)
            records = cur.fetchall()
    conn.close()  #на всякий случай
    return (records)


def main():
    pg_ous = get_ou_pg()
    z_srv = config.get('ZABBIX', 'server')
    z = ZabbixAPI(config.get('ZABBIX', 'host'))
    z.login(user=config.get('ZABBIX', 'user'),
            password=config.get('ZABBIX', 'password'))
    hosts = z.host.get(
        groupids=34,
        hostids=20625,
        output=['hostid', 'name', 'description'], sortfield='name')

    for host in hosts:
        for pg_ou in pg_ous:
            if host['name'].lower() == pg_ou[0]:
                if host['description'] == '':
                    # z.do_request(
                    #     'host.update', {
                    #         'hostid': host['hostid'],
                    #         'name': host['name'],
                    #         'description': pg_ou[1]
                    #     })
                    print("%-6s %-10s %-40s" %
                          (host['hostid'], host['name'], pg_ou[1]))
                    os.system('zabbix_sender -z '+z_srv+' -s '+host['name']+' -k address_trap -o "'+pg_ou[1].replace('"','').encode('utf-8').decode("cp1251", "replace")+'"')
                    break


if __name__ == '__main__':
    main()
