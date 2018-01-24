import os
import inspect
import time
import numpy as np
import mysql.connector
import gc
import matplotlib
from mysql_functions import MysqlQuery

try:
    matplotlib.use('macosx')
except:
    pass

from matplotlib.pyplot import *
ion()

mq = MysqlQuery()

# Get output path if provided, default at ~/Desktop
try:
    output_path = argv[1]
except:
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    output_path = os.path.dirname(os.path.abspath(filename)) + '/output/'

conn = mysql.connector.connect(
    user='root',
    password='ng@tr00t',
    database='sktobs'
    )
cur = conn.cursor()
query = ("SELECT `usnoref` FROM (" +\
"SELECT @row := @row +1 AS rownum, 'separation', `usnoref` " +\
"FROM (SELECT @row :=0) r, objdat ) ranked " +\
"WHERE rownum % 10000 = 1 ;")

cur.execute(query)
temp = cur.fetchall()
cur.close()
cur = None
conn.close()


temp = np.array(temp).astype('string').flatten()
n_normal = np.zeros(len(temp))
time_normal = np.zeros(len(temp))
n_partitioned = np.zeros(len(temp))
time_partitioned = np.zeros(len(temp))

for i, objectname in enumerate(temp):
    query_normal = ("SELECT * FROM obsdat WHERE `usnoref`=" + objectname + ";")
    query_partitioned = ("SELECT * FROM obsdat100split WHERE `usnoref`=" + objectname + ";")
    conn = mysql.connector.connect(
        user='root',
        password='ng@tr00t',
        database='sktobs'
        )
    # normal
    n_normal[i], time_normal[i] = mq.run_query(conn, query_normal)
    # partitioned
    n_partitioned[i], time_partitioned[i] = mq.run_query(conn, query_partitioned)
    conn.close()



figure(1)
clf()
scatter(jd.astype('float'), rcat.astype('float'), s=1)
ylim(8,11)
grid()
