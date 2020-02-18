import psycopg2
conn = psycopg2.connect(dbname='production',
                        user='pr',
                        password='1',
                        host='192.168.88.40',
                        port='6432')
cursor = conn.cursor()
#cursor.execute('SELECT * FROM pg_catalog.pg_user;')
cursor.execute('SELECT * FROM basis.t_user')
records = cursor.fetchall()
for row in records:
    print(row)
cursor.close()
conn.close()
