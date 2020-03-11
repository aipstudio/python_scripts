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
    f = open('tickets_hours.txt', 'w', encoding="utf-8")
    f.flush
    f.write('Время/дата|8T|8A|9T|9A|10T|10A|11T|11A|12T|12A|13T|13A|14T|14A|15T|15A|16T|16A|17T|17A|18T|18A|19T|19A\n')
    with con:
        cur = con.cursor()
        dt = []
        d = datetime.datetime(2019, 12, 1, 7, 0, 0)
        #td = datetime.datetime.today()
        td = datetime.datetime(2020, 1, 1, 23, 0, 0)
        while d < td:
            if d.weekday() < 5:
                dd = d + datetime.timedelta(hours=13)
                dt.append(f'{d} - {dd}')
            d = d + datetime.timedelta(days=1)

        for dt_ in dt:
            dt_s = dt_[:20]
            dt_e = dt_[22:]
            sql = f'''
                select t1.h, t1.ct, t2.ca
                from 
                (SELECT HOUR (t.create_time) as 'h',  count(*) as 'ct'
                FROM ticket t
                where t.create_time BETWEEN '{dt_s}' AND '{dt_e}'
                GROUP by HOUR (t.create_time) 
                ) t1, 
                (SELECT HOUR (a.create_time) as 'h',  count(*) as 'ca'
                FROM article a
                where a.create_time BETWEEN '{dt_s}' AND '{dt_e}' and a.create_by !=1
                GROUP by HOUR (a.create_time) ) t2
                where t1.h = t2.h
            '''
            cur.execute(sql)
            rows = cur.fetchall()
            res = ''
            
            for row in rows:
                res = f'{res} | {row[1]} | {row[2]}'
            print(f'{dt_[:10]}{res}')
            f.write(f'{dt_[:10]}{res}\n')
    f.close()

if __name__ == '__main__':
    main()
