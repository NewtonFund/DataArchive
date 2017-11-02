#!/usr/bin/python

'''
    File name: btree_gin_timing_ltarchive.py
    Prepared by: MCL
    Date created: 19/10/2017
    Date last modified: 2/11/2017
    Python Version: 2.7

    This script compares the run time of PostgreSQL queries with a positional
    and a instrumental selection, 4 cases are compared:
    (1) Database with B-Tree index
    (2) Database with hash indexes
    (3) Database without any indexes
'''

import os
import inspect
import sys
import numpy as np
import psycopg2
import matplotlib
from psql_functions import PsqlQuery
try:
    matplotlib.use('TkAgg')
except:
    pass

from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
# plt.ion()

pq = PsqlQuery()

# Get output path if provided, default at ~/Desktop
try:
    output_path = argv[1]
except:
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    output_path = os.path.dirname(os.path.abspath(filename)) + '/output/'


# Equatorial coordinates of the Galactic Centre
ra_gc = 266.41683
dec_gc = -29.00781

# Equatorial coordinates of the Galactic North Pole
ra_gnp = 192.85951
dec_gnp = 27.12834

# Number of repeats
n_repeat = 10

# Create zero arrays for the number of results and execution times
time_direct_1_filter = np.zeros(n_repeat)
time_direct_2_filter = np.zeros(n_repeat)
time_direct_3_filter = np.zeros(n_repeat)
time_direct_4_filter = np.zeros(n_repeat)
time_direct_5_filter = np.zeros(n_repeat)
time_direct_6_filter = np.zeros(n_repeat)
n_results_direct_1_filter = np.zeros(n_repeat)
n_results_direct_2_filter = np.zeros(n_repeat)
n_results_direct_3_filter = np.zeros(n_repeat)
n_results_direct_4_filter = np.zeros(n_repeat)
n_results_direct_5_filter = np.zeros(n_repeat)
n_results_direct_6_filter = np.zeros(n_repeat)

# Getting the list of unique OBSID
conn = psycopg2.connect(
    database="ltarchive",
    user="dbuser",
    password="dbuser",
    host="150.204.240.113",
    port="6543")
cur = conn.cursor()
cur.execute("SELECT DISTINCT \"OBSID\" FROM allkeys_testing;")
obsid_list = np.array(cur.fetchall())
cur.close()
conn.close()

# Getting the list of unique USERID
conn = psycopg2.connect(
    database="ltarchive",
    user="dbuser",
    password="dbuser",
    host="150.204.240.113",
    port="6543")
cur = conn.cursor()
cur.execute("SELECT DISTINCT \"USERID\" FROM allkeys_testing;")
userid_list = np.array(cur.fetchall())
cur.close()
conn.close()

# Getting the list of unique TAGID
conn = psycopg2.connect(
    database="ltarchive",
    user="dbuser",
    password="dbuser",
    host="150.204.240.113",
    port="6543")
cur = conn.cursor()
cur.execute("SELECT DISTINCT \"TAGID\" FROM allkeys_testing;")
tagid_list = np.array(cur.fetchall())
cur.close()
conn.close()

# Getting the list of unique GROUPID
conn = psycopg2.connect(
    database="ltarchive",
    user="dbuser",
    password="dbuser",
    host="150.204.240.113",
    port="6543")
cur = conn.cursor()
cur.execute("SELECT DISTINCT \"GROUPID\" FROM allkeys_testing;")
groupid_list = np.array(cur.fetchall())
cur.close()
conn.close()

# Getting the list of unique PROPID
conn = psycopg2.connect(
    database="ltarchive",
    user="dbuser",
    password="dbuser",
    host="150.204.240.113",
    port="6543")
cur = conn.cursor()
cur.execute("SELECT DISTINCT \"PROPID\" FROM allkeys_testing;")
propid_list = np.array(cur.fetchall())
cur.close()
conn.close()

# Getting the list of unique INSTRUME
conn = psycopg2.connect(
    database="ltarchive",
    user="dbuser",
    password="dbuser",
    host="150.204.240.113",
    port="6543")
cur = conn.cursor()
cur.execute("SELECT DISTINCT \"INSTRUME\" FROM allkeys_testing;")
instrume_list = np.array(cur.fetchall())
cur.close()
conn.close()

# No index
for i in range(n_repeat):
    print "run " + str(i+1) + " of " + str(n_repeat)
    query_1_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\';"
    query_2_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE " +\
        "\"TAGID\"=\'LTOps\';"
    query_3_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE " +\
        "\"USERID\"=\'Operations\';"
    query_4_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE " +\
        "\"INSTRUME\"=\'IO:O\';"
    query_5_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE " +\
        "\"PROPID\"=\'MiscOpsTestA\';"
    query_6_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\';"
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")
    n_results_direct_1_filter[i], time_direct_1_filter[i] =\
        pq.run_query(conn, query_1_filter)
    n_results_direct_2_filter[i], time_direct_2_filter[i] =\
        pq.run_query(conn, query_2_filter)
    n_results_direct_3_filter[i], time_direct_3_filter[i] =\
        pq.run_query(conn, query_3_filter)
    n_results_direct_4_filter[i], time_direct_4_filter[i] =\
        pq.run_query(conn, query_4_filter)
    n_results_direct_5_filter[i], time_direct_5_filter[i] =\
        pq.run_query(conn, query_5_filter)
    n_results_direct_6_filter[i], time_direct_6_filter[i] =\
        pq.run_query(conn, query_6_filter)
    print "(Direct) Time elapsed for filter 1 : " + str(time_direct_1_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_1_filter[i])
    print "(Direct) Time elapsed for filter 2 : " + str(time_direct_2_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_2_filter[i])
    print "(Direct) Time elapsed for filter 3 : " + str(time_direct_3_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_3_filter[i])
    print "(Direct) Time elapsed for filter 4 : " + str(time_direct_4_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_4_filter[i])
    print "(Direct) Time elapsed for filter 5 : " + str(time_direct_5_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_5_filter[i])
    print "(Direct) Time elapsed for filter 6 : " + str(time_direct_6_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_6_filter[i])
    conn.close()



# GIN index

n_results_gin_obsid = np.zeros((len(obsid_list), n_repeat))
time_gin_obsid = np.zeros((len(obsid_list), n_repeat))
n_results_gin_groupid = np.zeros((len(groupid_list), n_repeat))
time_gin_groupid = np.zeros((len(groupid_list), n_repeat))
n_results_gin_tagid = np.zeros((len(tagid_list), n_repeat))
time_gin_tagid = np.zeros((len(tagid_list), n_repeat))
n_results_gin_userid = np.zeros((len(userid_list), n_repeat))
time_gin_userid = np.zeros((len(userid_list), n_repeat))
n_results_gin_propid = np.zeros((len(propid_list), n_repeat))
time_gin_propid = np.zeros((len(propid_list), n_repeat))
n_results_gin_instrume = np.zeros((len(instrume_list), n_repeat))
time_gin_instrume = np.zeros((len(instrume_list), n_repeat))

for i in range(n_repeat):
    print "run " + str(i+1) + " of " + str(n_repeat)
    # OBSID
    for j, obsid in enumerate(obsid_list):
        print str(j) + " of " + str(len(obsid_list))
        if (obsid[0] == None):
            continue
        obsid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
            "\"OBSID\" = '" + str(obsid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_gin_obsid[j][i], time_gin_obsid[j][i] =\
            pq.run_query(conn, obsid_query)
        conn.close()
    # GROUPID
    for j, groupid in enumerate(groupid_list):
        print str(j) + " of " + str(len(groupid_list))
        if (groupid[0] == None):
            continue
        groupid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
            "\"GROUPID\" = '" + str(groupid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_gin_groupid[j][i], time_gin_groupid[j][i] =\
            pq.run_query(conn, groupid_query)
        conn.close()
    # TAGID
    for j, tagid in enumerate(tagid_list):
        print str(j) + " of " + str(len(tagid_list))
        if (tagid[0] == None):
            continue
        tagid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
            "\"TAGID\" = '" + str(obsid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_gin_tagid[j][i], time_gin_tagid[j][i] =\
            pq.run_query(conn, tagid_query)
        conn.close()
    # USERID
    for j, userid in enumerate(userid_list):
        print str(j) + " of " + str(len(userid_list))
        if (userid[0] == None):
            continue
        userid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
            "\"USERID\" = '" + str(userid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_gin_userid[j][i], time_gin_userid[j][i] =\
            pq.run_query(conn, userid_query)
        conn.close()
    # PROPID
    for j, propid in enumerate(propid_list):
        print str(j) + " of " + str(len(propid_list))
        if (propid[0] == None):
            continue
        propid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
            "\"PROPID\" = '" + str(propid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_gin_propid[j][i], time_gin_propid[j][i] =\
            pq.run_query(conn, propid_query)
        conn.close()
    # INSTRUME
    for j, instrume in enumerate(instrume_list):
        print str(j) + " of " + str(len(instrume_list))
        if (instrume[0] == None):
            continue
        instrume_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
            "\"INSTRUME\" = '" + str(instrume[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_gin_instrume[j][i], time_gin_instrume[j][i] =\
            pq.run_query(conn, instrume_query)
        conn.close()




# B-Tree

n_results_btree_obsid = np.zeros((len(obsid_list), n_repeat))
time_btree_obsid = np.zeros((len(obsid_list), n_repeat))
n_results_btree_groupid = np.zeros((len(groupid_list), n_repeat))
time_btree_groupid = np.zeros((len(groupid_list), n_repeat))
n_results_btree_tagid = np.zeros((len(tagid_list), n_repeat))
time_btree_tagid = np.zeros((len(tagid_list), n_repeat))
n_results_btree_userid = np.zeros((len(userid_list), n_repeat))
time_btree_userid = np.zeros((len(userid_list), n_repeat))
n_results_btree_propid = np.zeros((len(propid_list), n_repeat))
time_btree_propid = np.zeros((len(propid_list), n_repeat))
n_results_btree_instrume = np.zeros((len(instrume_list), n_repeat))
time_btree_instrume = np.zeros((len(instrume_list), n_repeat))

for i in range(n_repeat):
    print "run " + str(i+1) + " of " + str(n_repeat)
    # OBSID
    for j, obsid in enumerate(obsid_list):
        print str(j) + " of " + str(len(obsid_list))
        if (obsid[0] == None):
            continue
        obsid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "\"OBSID\" = '" + str(obsid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_btree_obsid[j][i], time_btree_obsid[j][i] =\
            pq.run_query(conn, obsid_query)
        conn.close()
    # GROUPID
    for j, groupid in enumerate(groupid_list):
        print str(j) + " of " + str(len(groupid_list))
        if (groupid[0] == None):
            continue
        groupid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "\"GROUPID\" = '" + str(groupid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_btree_groupid[j][i], time_btree_groupid[j][i] =\
            pq.run_query(conn, groupid_query)
        conn.close()
    # TAGID
    for j, tagid in enumerate(tagid_list):
        print str(j) + " of " + str(len(tagid_list))
        if (tagid[0] == None):
            continue
        tagid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "\"TAGID\" = '" + str(obsid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_btree_tagid[j][i], time_btree_tagid[j][i] =\
            pq.run_query(conn, tagid_query)
        conn.close()
    # USERID
    for j, userid in enumerate(userid_list):
        print str(j) + " of " + str(len(userid_list))
        if (userid[0] == None):
            continue
        userid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "\"USERID\" = '" + str(userid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_btree_userid[j][i], time_btree_userid[j][i] =\
            pq.run_query(conn, userid_query)
        conn.close()
    # PROPID
    for j, propid in enumerate(propid_list):
        print str(j) + " of " + str(len(propid_list))
        if (propid[0] == None):
            continue
        propid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "\"PROPID\" = '" + str(propid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_btree_propid[j][i], time_btree_propid[j][i] =\
            pq.run_query(conn, propid_query)
        conn.close()
    # INSTRUME
    for j, instrume in enumerate(instrume_list):
        print str(j) + " of " + str(len(instrume_list))
        if (instrume[0] == None):
            continue
        instrume_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "\"INSTRUME\" = '" + str(instrume[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_btree_instrume[j][i], time_btree_instrume[j][i] =\
            pq.run_query(conn, instrume_query)
        conn.close()


# Hash 

n_results_hash_obsid = np.zeros((len(obsid_list), n_repeat))
time_hash_obsid = np.zeros((len(obsid_list), n_repeat))
n_results_hash_groupid = np.zeros((len(groupid_list), n_repeat))
time_hash_groupid = np.zeros((len(groupid_list), n_repeat))
n_results_hash_tagid = np.zeros((len(tagid_list), n_repeat))
time_hash_tagid = np.zeros((len(tagid_list), n_repeat))
n_results_hash_userid = np.zeros((len(userid_list), n_repeat))
time_hash_userid = np.zeros((len(userid_list), n_repeat))
n_results_hash_propid = np.zeros((len(propid_list), n_repeat))
time_hash_propid = np.zeros((len(propid_list), n_repeat))
n_results_hash_instrume = np.zeros((len(instrume_list), n_repeat))
time_hash_instrume = np.zeros((len(instrume_list), n_repeat))

for i in range(n_repeat):
    print "run " + str(i+1) + " of " + str(n_repeat)
    # OBSID
    for j, obsid in enumerate(obsid_list):
        print str(j) + " of " + str(len(obsid_list))
        if (obsid[0] == None):
            continue
        obsid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
            "\"OBSID\" = '" + str(obsid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_hash_obsid[j][i], time_hash_obsid[j][i] =\
            pq.run_query(conn, obsid_query)
        conn.close()
    # GROUPID
    for j, groupid in enumerate(groupid_list):
        print str(j) + " of " + str(len(groupid_list))
        if (groupid[0] == None):
            continue
        groupid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
            "\"GROUPID\" = '" + str(groupid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_hash_groupid[j][i], time_hash_groupid[j][i] =\
            pq.run_query(conn, groupid_query)
        conn.close()
    # TAGID
    for j, tagid in enumerate(tagid_list):
        print str(j) + " of " + str(len(tagid_list))
        if (tagid[0] == None):
            continue
        tagid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
            "\"TAGID\" = '" + str(obsid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_hash_tagid[j][i], time_hash_tagid[j][i] =\
            pq.run_query(conn, tagid_query)
        conn.close()
    # USERID
    for j, userid in enumerate(userid_list):
        print str(j) + " of " + str(len(userid_list))
        if (userid[0] == None):
            continue
        userid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
            "\"USERID\" = '" + str(userid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_hash_userid[j][i], time_hash_userid[j][i] =\
            pq.run_query(conn, userid_query)
        conn.close()
    # PROPID
    for j, propid in enumerate(propid_list):
        print str(j) + " of " + str(len(propid_list))
        if (propid[0] == None):
            continue
        propid_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
            "\"PROPID\" = '" + str(propid[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_hash_propid[j][i], time_hash_propid[j][i] =\
            pq.run_query(conn, propid_query)
        conn.close()
    # INSTRUME
    for j, instrume in enumerate(instrume_list):
        print str(j) + " of " + str(len(instrume_list))
        if (instrume[0] == None):
            continue
        instrume_query =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
            "\"INSTRUME\" = '" + str(instrume[0]) + "';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")  
        # Run the queries and save the results in arrays
        n_results_hash_instrume[j][i], time_hash_instrume[j][i] =\
            pq.run_query(conn, instrume_query)
        conn.close()







fig1 = plt.figure(1, figsize=(10,6))
fig1.clf()
gridspec = GridSpec(1, 3)
gridspec.update(left=0.12,right=0.95,top=0.98,bottom=0.1,wspace=0)

ax1 = fig1.add_subplot(gridspec[0,0])
ax2 = fig1.add_subplot(gridspec[0,1])
ax3 = fig1.add_subplot(gridspec[0,2])


ax1.scatter(
    np.log10(np.median(n_results_hash_obsid,axis=1)),
    np.log10(np.median(time_hash_obsid,axis=1)),
    s=2,
    label='OBSID'
    )
ax1.scatter(
    np.log10(np.median(n_results_hash_groupid,axis=1)),
    np.log10(np.median(time_hash_groupid,axis=1)),
    s=2,
    label='GROUPID'
    )
ax1.scatter(
    np.log10(np.median(n_results_hash_tagid,axis=1)),
    np.log10(np.median(time_hash_tagid,axis=1)),
    s=2,
    label='TAGID'
    )
ax1.scatter(
    np.log10(np.median(n_results_hash_userid,axis=1)),
    np.log10(np.median(time_hash_userid,axis=1)),
    s=2,
    label='USERID'
    )
ax1.scatter(
    np.log10(np.median(n_results_hash_propid,axis=1)),
    np.log10(np.median(time_hash_propid,axis=1)),
    s=2,
    label='PROPID'
    )
ax1.scatter(
    np.log10(np.median(n_results_hash_instrume,axis=1)),
    np.log10(np.median(time_hash_instrume,axis=1)),
    s=2,
    label='INSTRUME'
    )
x_median_hash = np.concatenate((
    np.median(n_results_hash_obsid, axis=1),
    np.median(n_results_hash_groupid, axis=1),
    np.median(n_results_hash_tagid, axis=1),
    np.median(n_results_hash_userid, axis=1),
    np.median(n_results_hash_propid, axis=1),
    np.median(n_results_hash_instrume, axis=1)
    ))
y_median_hash = np.concatenate((
    np.median(time_hash_obsid, axis=1),
    np.median(time_hash_groupid, axis=1),
    np.median(time_hash_tagid, axis=1),
    np.median(time_hash_userid, axis=1),
    np.median(time_hash_propid, axis=1),
    np.median(time_hash_instrume, axis=1)
    ))
x_median_hash = x_median_hash[x_median_hash>0.]
y_median_hash = y_median_hash[y_median_hash>0.]
ax1.set_xlabel('Number of matches')
ax1.set_ylabel('Query Time / s')
ax1.grid()
xmin_hash = 0.0
xmax_hash = np.ceil(np.max(np.log10(x_median_hash)))
ymin_hash = np.floor(np.min(np.log10(y_median_hash)))+0.5
ymax_hash = np.ceil(np.max(np.log10(y_median_hash)))
xticks_hash = np.array((1,10,100,1000,10000,100000,1000000,10000000))
yticks_hash = np.arange(ymin_hash-0.5, ymax_hash,1.0)
ax1.set_xlim(xmin_hash,xmax_hash)
ax1.set_ylim(ymin_hash,ymax_hash)
ax1.set_xticks(np.log10(xticks_hash))
ax1.set_yticks(yticks_hash[1:])
ax1.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$',r'$10^{6}$'])
ax1.set_yticklabels([r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^{0}$',r'$10^{1}$'])

ax2.scatter(
    np.log10(np.median(n_results_btree_obsid,axis=1)),
    np.log10(np.median(time_btree_obsid,axis=1)),
    s=2,
    label='OBSID'
    )
ax2.scatter(
    np.log10(np.median(n_results_btree_groupid,axis=1)),
    np.log10(np.median(time_btree_groupid,axis=1)),
    s=2,
    label='GROUPID'
    )
ax2.scatter(
    np.log10(np.median(n_results_btree_tagid,axis=1)),
    np.log10(np.median(time_btree_tagid,axis=1)),
    s=2,
    label='TAGID'
    )
ax2.scatter(
    np.log10(np.median(n_results_btree_userid,axis=1)),
    np.log10(np.median(time_btree_userid,axis=1)),
    s=2,
    label='USERID'
    )
ax2.scatter(
    np.log10(np.median(n_results_btree_propid,axis=1)),
    np.log10(np.median(time_btree_propid,axis=1)),
    s=2,
    label='PROPID'
    )
ax2.scatter(
    np.log10(np.median(n_results_btree_instrume,axis=1)),
    np.log10(np.median(time_btree_instrume,axis=1)),
    s=2,
    label='INSTRUME'
    )
x_median_btree = np.concatenate((
    np.median(n_results_btree_obsid, axis=1),
    np.median(n_results_btree_groupid, axis=1),
    np.median(n_results_btree_tagid, axis=1),
    np.median(n_results_btree_userid, axis=1),
    np.median(n_results_btree_propid, axis=1),
    np.median(n_results_btree_instrume, axis=1)
    ))
y_median_btree = np.concatenate((
    np.median(time_btree_obsid, axis=1),
    np.median(time_btree_groupid, axis=1),
    np.median(time_btree_tagid, axis=1),
    np.median(time_btree_userid, axis=1),
    np.median(time_btree_propid, axis=1),
    np.median(time_btree_instrume, axis=1)
    ))
x_median_btree = x_median_btree[x_median_btree>0.]
y_median_btree = y_median_btree[y_median_btree>0.]
#ax2.set_ylabel('Query Time / s')
ax2.set_xlabel('Number of matches')
ax2.grid()
xmin_btree = 0.0
xmax_btree = np.ceil(np.max(np.log10(x_median_btree)))
ymin_btree = np.floor(np.min(np.log10(y_median_btree)))+0.5
ymax_btree = np.ceil(np.max(np.log10(y_median_btree)))
xticks_btree = np.arange(0, 8)
yticks_btree = np.arange(ymin_btree-0.5, ymax_btree,1.0)
ax2.set_xlim(xmin_btree,xmax_btree)
ax2.set_ylim(ymin_btree,ymax_btree)
ax2.set_xticks(xticks_btree)
ax2.set_yticks(yticks_btree[1:])
ax2.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$',r'$10^{6}$'])
ax2.set_yticklabels([''])

ax3.scatter(
    np.log10(np.median(n_results_gin_obsid,axis=1)),
    np.log10(np.median(time_gin_obsid,axis=1)),
    s=2,
    label='OBSID'
    )
ax3.scatter(
    np.log10(np.median(n_results_gin_groupid,axis=1)),
    np.log10(np.median(time_gin_groupid,axis=1)),
    s=2,
    label='GROUPID'
    )
ax3.scatter(
    np.log10(np.median(n_results_gin_tagid,axis=1)),
    np.log10(np.median(time_gin_tagid,axis=1)),
    s=2,
    label='TAGID'
    )
ax3.scatter(
    np.log10(np.median(n_results_gin_userid,axis=1)),
    np.log10(np.median(time_gin_userid,axis=1)),
    s=2,
    label='USERID'
    )
ax3.scatter(
    np.log10(np.median(n_results_gin_propid,axis=1)),
    np.log10(np.median(time_gin_propid,axis=1)),
    s=2,
    label='PROPID'
    )
ax3.scatter(
    np.log10(np.median(n_results_gin_instrume,axis=1)),
    np.log10(np.median(time_gin_instrume,axis=1)),
    s=2,
    label='INSTRUME'
    )
x_median_gin = np.concatenate((
    np.median(n_results_gin_obsid, axis=1),
    np.median(n_results_gin_groupid, axis=1),
    np.median(n_results_gin_tagid, axis=1),
    np.median(n_results_gin_userid, axis=1),
    np.median(n_results_gin_propid, axis=1),
    np.median(n_results_gin_instrume, axis=1)
    ))
y_median_gin = np.concatenate((
    np.median(time_gin_obsid, axis=1),
    np.median(time_gin_groupid, axis=1),
    np.median(time_gin_tagid, axis=1),
    np.median(time_gin_userid, axis=1),
    np.median(time_gin_propid, axis=1),
    np.median(time_gin_instrume, axis=1)
    ))
x_median_gin = x_median_gin[x_median_gin>0.]
y_median_gin = y_median_gin[y_median_gin>0.]
ax3.set_xlabel('Number of matches')
ax3.grid()
xmin_gin = 0.0
xmax_gin = np.ceil(np.max(np.log10(x_median_gin)))
ymin_gin = np.floor(np.min(np.log10(y_median_gin)))+0.5
ymax_gin = np.ceil(np.max(np.log10(y_median_gin)))
xticks_gin = np.arange(0,8)
yticks_gin = np.arange(ymin_gin-0.5, ymax_gin+1.0,1.0)
ax3.set_xlim(xmin_gin,xmax_gin)
ax3.set_ylim(ymin_gin,ymax_gin)
ax3.set_xticks(xticks_gin)
ax3.set_yticks(yticks_gin[1:])
ax3.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$',r'$10^{6}$',r'$10^{7}$'])
ax3.set_yticklabels([''])
ax3.legend()

ax1.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_1_filter)),np.log10(np.median(time_direct_1_filter))])
ax1.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_6_filter)),np.log10(np.median(time_direct_6_filter))])
ax1.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_2_filter)),np.log10(np.median(time_direct_2_filter))])
ax1.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_3_filter)),np.log10(np.median(time_direct_3_filter))])
ax1.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_5_filter)),np.log10(np.median(time_direct_5_filter))])
ax1.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_4_filter)),np.log10(np.median(time_direct_4_filter))])

ax2.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_1_filter)),np.log10(np.median(time_direct_1_filter))])
ax2.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_6_filter)),np.log10(np.median(time_direct_6_filter))])
ax2.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_2_filter)),np.log10(np.median(time_direct_2_filter))])
ax2.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_3_filter)),np.log10(np.median(time_direct_3_filter))])
ax2.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_5_filter)),np.log10(np.median(time_direct_5_filter))])
ax2.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_4_filter)),np.log10(np.median(time_direct_4_filter))])

ax3.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_1_filter)),np.log10(np.median(time_direct_1_filter))])
ax3.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_6_filter)),np.log10(np.median(time_direct_6_filter))])
ax3.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_2_filter)),np.log10(np.median(time_direct_2_filter))])
ax3.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_3_filter)),np.log10(np.median(time_direct_3_filter))])
ax3.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_5_filter)),np.log10(np.median(time_direct_5_filter))])
ax3.plot([xmin_hash,xmax_hash],[np.log10(np.median(time_direct_4_filter)),np.log10(np.median(time_direct_4_filter))])

plt.savefig(output_path + 'query_time_hash_btree_gin_compared.png')
