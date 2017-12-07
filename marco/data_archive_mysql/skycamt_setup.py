'''
Run natively on Newton
'''

import mysql.connector
import numpy as np

query_unique_usnoref = ("SELECT DISTINCT(usnoref) FROM objdat;")
conn = mysql.connector.connect(
    user = "root",
    password = "ng@tr00t",
    database = 'sktobs'
    )
cur = conn.cursor()
cur.execute(query_unique_usnoref)
usnoref_list = np.array(cur.fetchall())
cur.close()
cur = None

usnoref_list = usnoref_list.astype('str')
list_length = len(usnoref_list)

conn = mysql.connector.connect(user="root", password="ng@tr00t", database='sktobs')

for i in range(list_length):
    print str((i+1)) + " of " + str(list_length) + " tables created."
    usnoref1 = usnoref_list[i][0]
    query1 = ("CREATE TABLE IF NOT EXISTS skt.`" + usnoref1 + "` AS SELECT * FROM obsdat WHERE usnoref=\"" + usnoref1 + "\";")
    try:
        cur = conn.cursor()
        for result in cur.execute(query1):
            pass
    except:
        conn = mysql.connector.connect(user="root", password="ng@tr00t", database='sktobs')
        cur = conn.cursor()
        for result in cur.execute(query1):
            pass

