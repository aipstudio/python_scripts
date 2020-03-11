#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime 
import pymysql
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')


def main():
    con = pymysql.connect(config.get('OTRS', 'host'), 'otrs_conn',
                          config.get('OTRS', 'password'), 'otrs')
    f = open('tickets.txt', 'w', encoding="utf-8")
    f.flush
    with con:
        cur = con.cursor()
        #dt = ('2020-02-22 - 2020-02-23', '2020-02-15 - 2020-02-16')
        dt = []
        d = datetime.date(2019, 9, 28)
        td = datetime.date.today()
        while d <= td:
            d = d + datetime.timedelta(days=7)
            dd = d + datetime.timedelta(days=1)
            dt.append(f'{d} - {dd}')

        for dt_ in dt:
            dt_s = dt_[:10]
            dt_e = dt_[13:]
            sql = f'''
                select '{dt_s} - {dt_e}' as 'Period', t1.c as 'all', t2.c as 'PharnNet', t3.c as 'Retail', t4.c as 'Mail'
                from 
                (SELECT count(*) as 'c', '{dt_s} - {dt_e}' as 'DT', 'All' as 'In'
                FROM ticket t 
                where t.create_time BETWEEN '{dt_s} 00:00:00' AND '{dt_e} 23:59:59'
                #and (t.title like 'Проблема не связанная с кассой' or t.title like 'Не печатает ККМ' 
                #or t.title like 'Расхождение денежных сумм' or t.title like 'Другая проблема');
                #and t.customer_id = 'pharm.net@aprelit.xyz'
                ) t1,
                (
                SELECT count(*) as 'c', '{dt_s} - {dt_e}' as 'DT', 'PharnNet' as ''
                FROM ticket t 
                where t.create_time BETWEEN '{dt_s} 00:00:00' AND '{dt_e} 23:59:59'
                #and (t.title like 'Проблема не связанная с кассой' or t.title like 'Не печатает ККМ' 
                #or t.title like 'Расхождение денежных сумм' or t.title like 'Другая проблема');
                and t.customer_id = 'pharm.net@aprelit.xyz'
                ) t2,
                (
                SELECT count(*) as 'c', '{dt_s} - {dt_e}' as 'DT', 'Retail' as ''
                FROM ticket t 
                where t.create_time BETWEEN '{dt_s} 00:00:00' AND '{dt_e} 23:59:59'
                and (t.title like 'Проблема не связанная с кассой' or t.title like 'Не печатает ККМ' 
                or t.title like 'Расхождение денежных сумм' or t.title like 'Другая проблема')
                #and t.customer_id = 'pharm.net@aprelit.xyz'
                ) t3,
                (
                SELECT count(*) as 'c', '{dt_s} - {dt_e}' as 'DT', 'Mail' as ''
                FROM ticket t 
                where t.create_time BETWEEN '{dt_s} 00:00:00' AND '{dt_e} 23:59:59'
                and t.title not like 'Проблема не связанная с кассой' and t.title not like 'Не печатает ККМ' 
                and t.title not like 'Расхождение денежных сумм' and t.title not like 'Другая проблема'
                and t.customer_id != 'pharm.net@aprelit.xyz'
                ) t4
            '''
            cur.execute(sql)
            rows = cur.fetchall()

            for row in rows:
                print(row)
                f.write(f'{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n')
    f.close()


if __name__ == '__main__':
    main()