import os
import inspect
import time
import numpy as np
import mysql.connector
import gc
import matplotlib
from mysql_functions import MysqlQuery
import random

#try:
#    matplotlib.use('macosx')
#except:
#    pass

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
#query = ("SELECT `usnoref` FROM (" +\
#"SELECT @row := @row +1 AS rownum, 'separation', `usnoref` " +\
#"FROM (SELECT @row :=0) r, objdat WHERE `entries`>10) ranked " +\
#"WHERE rownum % 1000 = 1;")

query = ("SELECT `usnoref` FROM objdat WHERE `entries`>100;")

cur.execute(query)
object_list = cur.fetchall()
cur.close()
cur = None
conn.close()


object_list = np.array(object_list).astype('string').flatten()
n_normal = np.zeros(10000*5)
n_partitioned = np.zeros(10000*5)

conn = mysql.connector.connect(
    user='root',
    password='ng@tr00t',
    database='sktobs'
    )

for j in range(5):
    random.shuffle(object_list)
    for i, objectname in enumerate(object_list[10000:]):
        print i, objectname
        query_normal = ("SELECT RA FROM obsdat WHERE `usnoref`='" + str(objectname) + "';")
        query_partitioned = ("SELECT RA FROM obsdat100split WHERE `usnoref`='" + str(objectname) + "';")
        # normal
        cur = conn.cursor()
        cur.execute(query_normal)
        n_normal[i+j*10000] = np.shape(cur.fetchall())[0]
        cur.close()
        # partitioned
        cur = conn.cursor()
        cur.execute(query_partitioned)
        n_partitioned[i+j*10000] = np.shape(cur.fetchall())[0]
        cur.close()

conn.close()


# Get the query time, has to be done in the same session as the queries above
# `SQL_TEXT`, `TIMER_WAIT`/1000000000000
query_time = ("SELECT * FROM `events_statements_history_long` WHERE `CURRENT_SCHEMA`='sktobs' AND `EVENT_NAME`='statement/sql/select';")
conn = mysql.connector.connect(
    user='root',
    password='ng@tr00t',
    database='performance_schema'
    )
# normal
cur = conn.cursor()
cur.execute(query_time)
events_statements_history_long = cur.fetchall()
cur.close()
conn.close()
events_statements_history_long = np.array(events_statements_history_long)

np.save('events_statements_history_long.npy', events_statements_history_long)
np.save('n_normal.npy', n_normal)
np.save('n_partitioned.npy', n_partitioned)

time_elapsed = events_statements_history_long[:,7].astype('float')/1E12
time_elapsed_normal = time_elapsed[::2]
time_elapsed_partitioned = time_elapsed[1::2]

figure(1)
clf()
scatter(time_elapsed_normal, time_elapsed_partitioned, s=1)
xlabel('Single table')
ylabel('100-partition table')
grid()

figure(2)
clf()
hist(time_elapsed_normal/time_elapsed_partitioned, bins=200,range=(0,200))
grid()
