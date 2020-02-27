#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
import psycopg2
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
                     where (p.partner_e_mail like 'af%%@%' or p.partner_e_mail like 'fk%%@%') and p.id = 17860''' #and p.id = 17860
            cur.execute(sql)
            records = cur.fetchall()
    conn.close()  #на всякий случай
    return (records)


def main():
    pg_ous = get_ou_pg()

    z = ZabbixAPI(config.get('ZABBIX', 'host'))
    z.login(user=config.get('ZABBIX', 'user'),
            password=config.get('ZABBIX', 'password'))
    hosts = z.host.get(
        groupids=34,
        #        hostids=14269,
        output=['hostid', 'name', 'description'])

    for host in hosts:
        for pg_ou in pg_ous:
            if host['name'] == pg_ou[0]:
                z.do_request(
                    'host.update', {
                        'hostid': host['hostid'],
                        'name': host['name'],
                        'description': pg_ou[1]
                    })
                print("%-6s %-10s %-40s" %
                      (host['hostid'], host['name'], pg_ou[1]))
                break


if __name__ == '__main__':
    main()