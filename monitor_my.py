#!/usr/bin/python
# -*- coding: utf-8 -*-
import configparser
import json
import socket
import datetime
import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
from pyzabbix import ZabbixAPI

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')
otrs_ip = config.get('OTRS', 'host')
otrs_pass = config.get('OTRS', 'password')

users = {}
new_tickets_today = 0
close_tickets_today = 0
open_tickets = 0

def get_otrs_users():
    con = pymysql.connect(otrs_ip, 'otrs_conn',
                          otrs_pass, 'otrs')
    with con:
        cur = con.cursor()
        sql = f'''
            select u.id , u.login , u.first_name 
            from users u , group_user gu 
            where u.id = gu.user_id 
            and gu.group_id = 25 and u.valid_id = 1
            '''
        cur.execute(sql)
        rows = cur.fetchall()
        for num, row in enumerate (rows):
            users[num] = {'user': row[1], 'id': row[0], 'name': row[2],'opened': '', 'closed': '', 'ach_opened': '', 'ach_closed': ''}

def get_from_DB( id):
    connection = pymysql.connect(
        host=otrs_ip,
        user='otrs_conn',
        password=otrs_pass,
        db='otrs',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    opened, closed, ach_opened, ach_closed = 0, 0, 0, 0
# список открытых заявок
    with closing(connection) as connection:
        with connection.cursor() as cursor:
            query = f"""
                select u.first_name, t.user_id , count(*) as open 
                from otrs.ticket t
                join otrs.users u on t.user_id = u.id
                where t.ticket_state_id in (1,4) -- 1 - new 4 - open 2 - closed
                and  t.user_id in 
                ({id}) -- 57 тех подд, 1 я-admin
                group by t.user_id
                order by 3 desc;
            """
            cursor.execute(query)
            for row in cursor:
                opened = row['open']
# список закрытых заявок
            query = f"""
                select u.first_name, t.user_id , count(*) as closed
                from otrs.ticket t
                join otrs.users u on t.user_id = u.id
                where t.ticket_state_id in (2) -- 1 - new 4 - open 2 - closed
                and t.user_id in 
                ({id}) 
                and date(t.change_time) = date(now())-- 57 тех подд, 1 я-admin
                group by t.user_id
                order by 3 desc;
            """
            cursor.execute(query)
            for row in cursor:
                closed = row['closed']

# список открытых ахтунгов
            query = f"""
                select u.first_name, t.user_id , count(*) as closed
                from otrs.ticket t
                join otrs.users u on t.user_id = u.id
                where t.ticket_state_id in (1,4) -- 1 - new 4 - open 2 - closed
                and t.ticket_priority_id = 5 
                and  t.user_id in 
                ({id}) 
                group by t.user_id
                order by 3 desc;
            """
            cursor.execute(query)
            for row in cursor:
                    # print(row)
                ach_opened = row['closed']
# список закрытых ахтунгов
            query = f"""
                select u.first_name, t.user_id , count(*) as closed
                from otrs.ticket t
                join otrs.users u on t.user_id = u.id
                where t.ticket_state_id in (2) -- 1 - new 4 - open 2 - closed
                and t.ticket_priority_id = 5 
                and  t.user_id in 
                ({id}) 
                and date(t.change_time) = date(now())
                group by t.user_id
                order by 3 desc;
            """
            cursor.execute(query)
            for row in cursor:
                ach_closed = row['closed']
###################
    return opened, closed, ach_opened, ach_closed

def db_to_users():
    global close_tickets_today, open_tickets
    for user in users:
        #print(users[user]['user'])
        user_id = users[user]['id']
        op, cl, ao, ac = get_from_DB(user_id)
        users[user]['opened'] = op
        users[user]['closed'] = cl
        users[user]['ach_opened'] = ao
        users[user]['ach_closed'] = ac
        close_tickets_today = close_tickets_today + cl + ac
        open_tickets = open_tickets + op
        #print(users[user])

def count_new_from_db():
    global new_tickets_today
    connection = pymysql.connect(
        host=otrs_ip,
        user='otrs_conn',
        password=otrs_pass,
        db='otrs',
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    with closing(connection) as connection:
        with connection.cursor() as cursor:
            query = f"""
                select count(*) as new from otrs.ticket t
                where date(t.create_time) = date(now());
            """
            cursor.execute(query)
            for row in cursor:
                # print(row)
                new_tickets_today = row['new']
    

def send_elk():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('elasticsearch',5046))
    s.settimeout(0.1)
    for i in range(len(users)):
        j = '{"ticket_type":"ticket_agent","name":"' + str(users[i]['name']) + '","id":' + str(users[i]['id']) + ',"opened":' + str(users[i]['opened']) + ',"closed":' + str(users[i]['closed']) + ', "ach_opened":' + str(users[i]['ach_opened']) + ', "ach_closed":' + str(users[i]['ach_closed']) + '}\n'
        s.sendall(bytes(j, 'utf8'))
        try:
            j=s.recv(2048)        
        except socket.timeout:
            pass
    s.close()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('elasticsearch',5046))
    s.settimeout(0.1)
    j = '{"ticket_type":"ticket_all","all_create":' + str(new_tickets_today) + ',"all_close":' + str(close_tickets_today) + ',"all_open":' + str(open_tickets) + '}\n'
    s.sendall(bytes(j, 'utf8'))
    try:
        j=s.recv(2048)        
    except socket.timeout:
        pass
    s.close()

def main():
    count_new_from_db()
    get_otrs_users()
    db_to_users()
    send_elk()

if __name__ == '__main__':
    main()
