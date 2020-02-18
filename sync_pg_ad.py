#!/usr/bin/python
# -*- coding: utf-8 -*-
# pip install ldap3 psycopg2
import ldap3
import psycopg2
import configparser
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')


def get_users_pg():
    conn = psycopg2.connect(dbname=config.get('PG', 'db'), user=config.get(
        'PG', 'user'), password=config.get('PG', 'password'), host=config.get('PG', 'host'), port='5432')
    cursor = conn.cursor()
    sql = '''select u.id, u.sname||' '||u.name||' '||u.pname AS "FIO", u.user_login AS "login" , u.email, u.department_id AS "kod_otdela", d.name AS "OTDEL", u.status,
    case when u.status & 2 = 2 then 'WORKS' else 'LOCK' end AS "status_job"
    from basis.T_User u join basis.t_department d on d.id = u.department_id
    where u.email != '' and u.status & 2 >= 2 --u.department_id = 15; '''
    cursor.execute(sql)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return(records)

def get_users_ldap():
    server = ldap3.Server(config.get('AD', 'host'), get_info=ldap3.ALL)
    c = ldap3.Connection(server, config.get('AD', 'user'),
                         config.get('AD', 'password'))
    c.bind()
    pg_users = get_users_pg()
    pg_u_groups = ['АХС (AHS)', 'Бухгалтерия', 'Коммерческий отдел', 'Мебельный цех', 'Оптовый склад (OPT)', 'ОСБ', 'Отдел закупок', 'Отдел маркетинга (MRK)',
                   'Отдел обучения', 'Отдел персонала (PERS)', 'Отдел подбора персонала (PODP)', 'Отдел разработки программного обеспечения (PROG)', 'Отдел системного администрирования (IT)',
                   'Отдел собственной торговой марки', 'Рождественская Набережная', 'Руководство', 'Супервайзеры', 'Финансово-экономический отдел (FIN)', 'Юридический отдел (YUR)']
    for pg_u_group in pg_u_groups:
        c.search(f'OU={pg_u_group},OU=Пользователи,DC=apteka,DC=aprel',
                 '(objectclass=person)', attributes=['cn', 'sAMAccountName', 'mail'])
        for user_ldap in c.entries:
            if user_ldap['mail'] == None:
                for pg_user in pg_users:
                    if pg_user[2] == user_ldap['sAMAccountName']:
                        print("%-25s %-40s %-40s %-40s %-40s" % (str(user_ldap['sAMAccountName']), str(
                            user_ldap['cn']), str(user_ldap['mail']), str(pg_user[3]), pg_u_group))
                        # print(user_ldap.entry_dn)
                        #c.modify (user_ldap.entry_dn, {'mail': [(MODIFY_REPLACE, [str(user_pg[3])])]})
    #c.search('OU=Отдел системного администрирования (IT),OU=Пользователи,DC=apteka,DC=aprel', '(&(objectclass=person)(sAMAccountName=prozhoga_ay))', attributes=['cn', 'sAMAccountName', 'mail'])
    #c.search('OU=АХС (AHS),OU=Пользователи,DC=apteka,DC=aprel', '(objectclass=person)', attributes=['cn', 'sAMAccountName', 'mail'])

    c.unbind()
    c.closed


def main():
    get_users_ldap()


if __name__ == '__main__':
    main()
