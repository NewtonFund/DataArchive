'''
Run natively on Newton
'''

import os

import mysql.connector
import numpy as np

usnoref_list_path = '/home/dbuser/Documents/skcamt_usnored_list.npy'

if os.path.exists(usnored_list_path):
    usnoref_list = np.load(usnored_list_path)
else:
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
    np.save(usnored_list_path, usnoref_list)


conn = mysql.connector.connect(user="root", password="ng@tr00t", database='sktobs')

for i in range(list_length)[::-1]:
    usnoref = usnoref_list[i][0]
    query = ("CREATE TABLE IF NOT EXISTS skt.`" + usnoref + "` AS SELECT * FROM obsdat WHERE usnoref=\"" + usnoref + "\";")
    try:
        cur = conn.cursor()
        for result in cur.execute(query, multi=True):
            pass
    except:
        conn = mysql.connector.connect(user="root", password="ng@tr00t", database='sktobs')
        cur = conn.cursor()
        for result in cur.execute(query, multi=True):
            pass
    print str((i+1)) + " of " + str(list_length) + " tables created."

