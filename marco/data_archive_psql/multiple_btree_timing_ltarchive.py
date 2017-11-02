#!/usr/bin/python

'''
    File name: multiple_btree_timing_ltarchive.py
    Prepared by: MCL
    Date created: 16/8/2017
    Date last modified: 2/11/2017
    Python Version: 2.7

    This script compares the run time of PostgreSQL queries with a positional
    and a instrumental selection, 4 cases are compared:
    (1) Database with only spatial index on positions
    (2) Database with only B-Tree index on instruments
    (3) Database with both indexes
    (4) Database without any index
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
n_repeat_direct = 5

# Create zero arrays for the number of results and execution times
time_pgsphere_1_filter_case_1 = np.zeros(n_repeat)
n_results_pgsphere_1_filter_case_1 = np.zeros(n_repeat)
time_pgsphere_2_filter_case_1 = np.zeros(n_repeat)
n_results_pgsphere_2_filter_case_1 = np.zeros(n_repeat)
time_pgsphere_3_filter_case_1 = np.zeros(n_repeat)
n_results_pgsphere_3_filter_case_1 = np.zeros(n_repeat)
time_pgsphere_4_filter_case_1 = np.zeros(n_repeat)
n_results_pgsphere_4_filter_case_1 = np.zeros(n_repeat)
time_pgsphere_5_filter_case_1 = np.zeros(n_repeat)
n_results_pgsphere_5_filter_case_1 = np.zeros(n_repeat)
time_pgsphere_6_filter_case_1 = np.zeros(n_repeat)
n_results_pgsphere_6_filter_case_1 = np.zeros(n_repeat)

time_pgsphere_1_filter_case_2 = np.zeros(n_repeat)
n_results_pgsphere_1_filter_case_2 = np.zeros(n_repeat)
time_pgsphere_2_filter_case_2 = np.zeros(n_repeat)
n_results_pgsphere_2_filter_case_2 = np.zeros(n_repeat)
time_pgsphere_3_filter_case_2 = np.zeros(n_repeat)
n_results_pgsphere_3_filter_case_2 = np.zeros(n_repeat)
time_pgsphere_4_filter_case_2 = np.zeros(n_repeat)
n_results_pgsphere_4_filter_case_2 = np.zeros(n_repeat)
time_pgsphere_5_filter_case_2 = np.zeros(n_repeat)
n_results_pgsphere_5_filter_case_2 = np.zeros(n_repeat)
time_pgsphere_6_filter_case_2 = np.zeros(n_repeat)
n_results_pgsphere_6_filter_case_2 = np.zeros(n_repeat)

time_pgsphere_1_filter_case_3 = np.zeros(n_repeat)
n_results_pgsphere_1_filter_case_3 = np.zeros(n_repeat)
time_pgsphere_2_filter_case_3 = np.zeros(n_repeat)
n_results_pgsphere_2_filter_case_3 = np.zeros(n_repeat)
time_pgsphere_3_filter_case_3 = np.zeros(n_repeat)
n_results_pgsphere_3_filter_case_3 = np.zeros(n_repeat)
time_pgsphere_4_filter_case_3 = np.zeros(n_repeat)
n_results_pgsphere_4_filter_case_3 = np.zeros(n_repeat)
time_pgsphere_5_filter_case_3 = np.zeros(n_repeat)
n_results_pgsphere_5_filter_case_3 = np.zeros(n_repeat)
time_pgsphere_6_filter_case_3 = np.zeros(n_repeat)
n_results_pgsphere_6_filter_case_3 = np.zeros(n_repeat)

time_pgsphere_1_filter_case_4 = np.zeros(n_repeat)
n_results_pgsphere_1_filter_case_4 = np.zeros(n_repeat)
time_pgsphere_2_filter_case_4 = np.zeros(n_repeat)
n_results_pgsphere_2_filter_case_4 = np.zeros(n_repeat)
time_pgsphere_3_filter_case_4 = np.zeros(n_repeat)
n_results_pgsphere_3_filter_case_4 = np.zeros(n_repeat)
time_pgsphere_4_filter_case_4 = np.zeros(n_repeat)
n_results_pgsphere_4_filter_case_4 = np.zeros(n_repeat)
time_pgsphere_5_filter_case_4 = np.zeros(n_repeat)
n_results_pgsphere_5_filter_case_4 = np.zeros(n_repeat)
time_pgsphere_6_filter_case_4 = np.zeros(n_repeat)
n_results_pgsphere_6_filter_case_4 = np.zeros(n_repeat)

time_pgsphere_1_filter_case_5 = np.zeros(n_repeat)
n_results_pgsphere_1_filter_case_5 = np.zeros(n_repeat)
time_pgsphere_2_filter_case_5 = np.zeros(n_repeat)
n_results_pgsphere_2_filter_case_5 = np.zeros(n_repeat)
time_pgsphere_3_filter_case_5 = np.zeros(n_repeat)
n_results_pgsphere_3_filter_case_5 = np.zeros(n_repeat)
time_pgsphere_4_filter_case_5 = np.zeros(n_repeat)
n_results_pgsphere_4_filter_case_5 = np.zeros(n_repeat)
time_pgsphere_5_filter_case_5 = np.zeros(n_repeat)
n_results_pgsphere_5_filter_case_5 = np.zeros(n_repeat)
time_pgsphere_6_filter_case_5 = np.zeros(n_repeat)
n_results_pgsphere_6_filter_case_5 = np.zeros(n_repeat)

time_direct_1_filter = np.zeros(n_repeat_direct)
n_results_direct_1_filter = np.zeros(n_repeat_direct)
time_direct_2_filter = np.zeros(n_repeat_direct)
n_results_direct_2_filter = np.zeros(n_repeat_direct)
time_direct_3_filter = np.zeros(n_repeat_direct)
n_results_direct_3_filter = np.zeros(n_repeat_direct)
time_direct_4_filter = np.zeros(n_repeat_direct)
n_results_direct_4_filter = np.zeros(n_repeat_direct)
time_direct_5_filter = np.zeros(n_repeat_direct)
n_results_direct_5_filter = np.zeros(n_repeat_direct)
time_direct_6_filter = np.zeros(n_repeat_direct)
n_results_direct_6_filter = np.zeros(n_repeat_direct)

time_1 = np.zeros(n_repeat)
time_2 = np.zeros(n_repeat)
time_3 = np.zeros(n_repeat)
time_4 = np.zeros(n_repeat)
time_5 = np.zeros(n_repeat)
time_6 = np.zeros(n_repeat)

# Baseline

query_1_distinct = "SELECT COUNT(DISTINCT \"INSTRUME\") FROM allkeys;"
query_2_distinct = "SELECT COUNT(DISTINCT \"TAGID\") FROM allkeys;"
query_3_distinct = "SELECT COUNT(DISTINCT \"USERID\") FROM allkeys;"
query_4_distinct = "SELECT COUNT(DISTINCT \"PROPID\") FROM allkeys;"
query_5_distinct = "SELECT COUNT(DISTINCT \"OBSID\") FROM allkeys;"
query_6_distinct = "SELECT COUNT(DISTINCT \"GROUPID\") FROM allkeys;"

conn = psycopg2.connect(
    database="ltarchive",
    user="dbuser",
    password="dbuser",
    host="150.204.240.113",
    port="6543")

cur = conn.cursor()
cur.execute(query_1_distinct)
n_results_1 = int(cur.fetchall()[0][0])
cur.close()
cur = conn.cursor()
cur.execute(query_2_distinct)
n_results_2 = int(cur.fetchall()[0][0])
cur.close()
cur = conn.cursor()
cur.execute(query_3_distinct)
n_results_3 = int(cur.fetchall()[0][0])
cur.close()
cur = conn.cursor()
cur.execute(query_4_distinct)
n_results_4 = int(cur.fetchall()[0][0])
cur.close()
cur = conn.cursor()
cur.execute(query_5_distinct)
n_results_5 = int(cur.fetchall()[0][0])
cur.close()
cur = conn.cursor()
cur.execute(query_6_distinct)
n_results_6 = int(cur.fetchall()[0][0])
cur.close()

conn.close()

for i in range(n_repeat):
    query_1 = "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
        "WHERE \"INSTRUME\"=\'IO:O\';"
    query_2 = "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
        "WHERE \"TAGID\"=\'LTOps\';"
    query_3 = "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
        "WHERE \"USERID\"=\'Operations\';"
    query_4 = "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
        "WHERE \"PROPID\"=\'MiscOpsTestA\';"
    query_5 = "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
        "WHERE \"OBSID\"=\'MULTIPLE_EXPOSURE\';"
    query_6 = "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
        "WHERE \"GROUPID\"=\'IOO_frodo_magicpixel\';"

    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")

    bla, time_1[i] = pq.run_query(conn, query_1)
    bla, time_2[i] = pq.run_query(conn, query_2)
    bla, time_3[i] = pq.run_query(conn, query_3)
    bla, time_4[i] = pq.run_query(conn, query_4)
    bla, time_5[i] = pq.run_query(conn, query_5)
    bla, time_6[i] = pq.run_query(conn, query_6)

    print "(Direct) Time elapsed for 1 filter : " + str(time_1[i])
    print "(Direct) Time elapsed for 2 filter : " + str(time_2[i])
    print "(Direct) Time elapsed for 3 filter : " + str(time_3[i])
    print "(Direct) Time elapsed for 4 filter : " + str(time_4[i])
    print "(Direct) Time elapsed for 5 filter : " + str(time_5[i])
    print "(Direct) Time elapsed for 6 filter : " + str(time_6[i])

    conn.close()

# No index
for i in range(n_repeat_direct):
    query_1_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE \"INSTRUME\"=\'IO:O\';"
    query_2_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE \"INSTRUME\"=\'IO:O\'" +\
        " AND \"OBSID\"=\'MULTIPLE_EXPOSURE\';"
    query_3_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE \"INSTRUME\"=\'IO:O\'" +\
        " AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\';"
    query_4_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE \"INSTRUME\"=\'IO:O\'" +\
        " AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\';"
    query_5_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE \"INSTRUME\"=\'IO:O\'" +\
        " AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"USERID\"=\'Operations\';"
    query_6_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE \"INSTRUME\"=\'IO:O\'" +\
        " AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"USERID\"=\'Operations\' AND " +\
        "\"TAGID\"=\'LTOps\';"

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

    print "(Direct) Time elapsed for 1 filter : " + str(time_direct_1_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_1_filter[i])
    print "(Direct) Time elapsed for 2 filter : " + str(time_direct_2_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_2_filter[i])
    print "(Direct) Time elapsed for 3 filter : " + str(time_direct_3_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_3_filter[i])
    print "(Direct) Time elapsed for 4 filter : " + str(time_direct_4_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_4_filter[i])
    print "(Direct) Time elapsed for 5 filter : " + str(time_direct_5_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_5_filter[i])
    print "(Direct) Time elapsed for 6 filter : " + str(time_direct_6_filter[i]) +\
        ' No. of matches = ' + str(n_results_direct_6_filter[i])

    conn.close()


# Case 1
# Repeating the queries n_repeat times
for i in range(n_repeat):
    print "run " + str(i+1) + " of " + str(n_repeat)

    query_1_filter_case_1 =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\';"
    query_2_filter_case_1 =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"TAGID\"=\'LTOps\';"
    query_3_filter_case_1 =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"TAGID\"=\'LTOps\' AND " +\
        "\"USERID\"=\'Operations\';"
    query_4_filter_case_1 =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"TAGID\"=\'LTOps\' AND " +\
        "\"USERID\"=\'Operations\' AND \"INSTRUME\"=\'IO:O\';"
    query_5_filter_case_1 =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"TAGID\"=\'LTOps\' AND " +\
        "\"USERID\"=\'Operations\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\';"
    query_6_filter_case_1 =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"TAGID\"=\'LTOps\' AND " +\
        "\"USERID\"=\'Operations\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\';"

    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  

    # Run the queries and save the results in arrays
    n_results_pgsphere_1_filter_case_1[i], time_pgsphere_1_filter_case_1[i] =\
        pq.run_query(conn, query_1_filter_case_1)
    n_results_pgsphere_2_filter_case_1[i], time_pgsphere_2_filter_case_1[i] =\
        pq.run_query(conn, query_2_filter_case_1)
    n_results_pgsphere_3_filter_case_1[i], time_pgsphere_3_filter_case_1[i] =\
        pq.run_query(conn, query_3_filter_case_1)
    n_results_pgsphere_4_filter_case_1[i], time_pgsphere_4_filter_case_1[i] =\
        pq.run_query(conn, query_4_filter_case_1)
    n_results_pgsphere_5_filter_case_1[i], time_pgsphere_5_filter_case_1[i] =\
        pq.run_query(conn, query_5_filter_case_1)
    n_results_pgsphere_6_filter_case_1[i], time_pgsphere_6_filter_case_1[i] =\
        pq.run_query(conn, query_6_filter_case_1)

    # Print results
    print "(pgSphere) Time elapsed for pgSphere 1 filter : " +\
        str(time_pgsphere_1_filter_case_1[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_1_filter_case_1[i])
    print "(pgSphere) Time elapsed for pgSphere 2 filter : " +\
        str(time_pgsphere_2_filter_case_1[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_2_filter_case_1[i])
    print "(pgSphere) Time elapsed for pgSphere 3 filter : " +\
        str(time_pgsphere_3_filter_case_1[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_3_filter_case_1[i])
    print "(pgSphere) Time elapsed for pgSphere 4 filter : " +\
        str(time_pgsphere_4_filter_case_1[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_4_filter_case_1[i])
    print "(pgSphere) Time elapsed for pgSphere 5 filter : " +\
        str(time_pgsphere_5_filter_case_1[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_5_filter_case_1[i])
    print "(pgSphere) Time elapsed for pgSphere 6 filter : " +\
        str(time_pgsphere_6_filter_case_1[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_6_filter_case_1[i])

    # Terminate connection to the database
    conn.close()


# Case 2
for i in range(n_repeat):
    query_1_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\';"
    query_2_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\';"
    query_3_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"INSTRUME\"=\'IO:O\';"
    query_4_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"USERID\"=\'Operations\';"
    query_5_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"USERID\"=\'Operations\' AND \"TAGID\"=\'LTOps\';"
    query_6_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"USERID\"=\'Operations\' AND \"TAGID\"=\'LTOps\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\';"

    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  

    # Run the queries and save the results in arrays
    n_results_pgsphere_1_filter_case_2[i], time_pgsphere_1_filter_case_2[i] =\
        pq.run_query(conn, query_1_filter)
    n_results_pgsphere_2_filter_case_2[i], time_pgsphere_2_filter_case_2[i] =\
        pq.run_query(conn, query_2_filter)
    n_results_pgsphere_3_filter_case_2[i], time_pgsphere_3_filter_case_2[i] =\
        pq.run_query(conn, query_3_filter)
    n_results_pgsphere_4_filter_case_2[i], time_pgsphere_4_filter_case_2[i] =\
        pq.run_query(conn, query_4_filter)
    n_results_pgsphere_5_filter_case_2[i], time_pgsphere_5_filter_case_2[i] =\
        pq.run_query(conn, query_5_filter)
    n_results_pgsphere_6_filter_case_2[i], time_pgsphere_6_filter_case_2[i] =\
        pq.run_query(conn, query_6_filter)

    # Print results
    print "(pgSphere) Time elapsed for pgSphere 1 filter : " +\
        str(time_pgsphere_1_filter_case_2[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_1_filter_case_2[i])
    print "(pgSphere) Time elapsed for pgSphere 2 filter : " +\
        str(time_pgsphere_2_filter_case_2[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_2_filter_case_2[i])
    print "(pgSphere) Time elapsed for pgSphere 3 filter : " +\
        str(time_pgsphere_3_filter_case_2[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_3_filter_case_2[i])
    print "(pgSphere) Time elapsed for pgSphere 4 filter : " +\
        str(time_pgsphere_4_filter_case_2[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_4_filter_case_2[i])
    print "(pgSphere) Time elapsed for pgSphere 5 filter : " +\
        str(time_pgsphere_5_filter_case_2[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_5_filter_case_2[i])
    print "(pgSphere) Time elapsed for pgSphere 6 filter : " +\
        str(time_pgsphere_6_filter_case_2[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_6_filter_case_2[i])

    # Terminate connection to the database
    conn.close()


# Case 3
for i in range(n_repeat):
    query_1_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"INSTRUME\"=\'IO:O\';"
    query_2_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"INSTRUME\"=\'IO:O\' AND \"OBSID\"=\'MULTIPLE_EXPOSURE\';"
    query_3_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"INSTRUME\"=\'IO:O\' AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\';"
    query_4_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"INSTRUME\"=\'IO:O\' AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\';"
    query_5_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"INSTRUME\"=\'IO:O\' AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"USERID\"=\'Operations\';"
    query_6_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"INSTRUME\"=\'IO:O\' AND \"OBSID\"=\'MULTIPLE_EXPOSURE\' AND " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"USERID\"=\'Operations\' AND " +\
        "\"TAGID\"=\'LTOps\';"

    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543"
        )

    n_results_pgsphere_1_filter_case_3[i], time_pgsphere_1_filter_case_3[i] =\
        pq.run_query(conn, query_1_filter)
    n_results_pgsphere_2_filter_case_3[i], time_pgsphere_2_filter_case_3[i] =\
        pq.run_query(conn, query_2_filter)
    n_results_pgsphere_3_filter_case_3[i], time_pgsphere_3_filter_case_3[i] =\
        pq.run_query(conn, query_3_filter)
    n_results_pgsphere_4_filter_case_3[i], time_pgsphere_4_filter_case_3[i] =\
        pq.run_query(conn, query_4_filter)
    n_results_pgsphere_5_filter_case_3[i], time_pgsphere_5_filter_case_3[i] =\
        pq.run_query(conn, query_5_filter)
    n_results_pgsphere_6_filter_case_3[i], time_pgsphere_6_filter_case_3[i] =\
        pq.run_query(conn, query_6_filter)

    print "(pgSphere) Time elapsed for pgSphere 1 filter : " +\
        str(time_pgsphere_1_filter_case_3[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_1_filter_case_3[i])
    print "(pgSphere) Time elapsed for pgSphere 2 filter : " +\
        str(time_pgsphere_2_filter_case_3[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_2_filter_case_3[i])
    print "(pgSphere) Time elapsed for pgSphere 3 filter : " +\
        str(time_pgsphere_3_filter_case_3[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_3_filter_case_3[i])
    print "(pgSphere) Time elapsed for pgSphere 4 filter : " +\
        str(time_pgsphere_4_filter_case_3[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_4_filter_case_3[i])
    print "(pgSphere) Time elapsed for pgSphere 5 filter : " +\
        str(time_pgsphere_5_filter_case_3[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_5_filter_case_3[i])
    print "(pgSphere) Time elapsed for pgSphere 6 filter : " +\
        str(time_pgsphere_6_filter_case_3[i]) + ' No. of matches = ' +\
       str(n_results_pgsphere_6_filter_case_3[i])

    conn.close()


# Case 4
for i in range(n_repeat):
    query_1_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\';"
    query_2_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\';"
    query_3_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\';"
    query_4_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\';"
    query_5_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"USERID\"=\'Operations\';"
    query_6_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\' AND \"USERID\"=\'Operations\' AND " +\
        "\"TAGID\"=\'LTOps\';"

    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543"
        )

    n_results_pgsphere_1_filter_case_4[i], time_pgsphere_1_filter_case_4[i] =\
        pq.run_query(conn, query_1_filter)
    n_results_pgsphere_2_filter_case_4[i], time_pgsphere_2_filter_case_4[i] =\
        pq.run_query(conn, query_2_filter)
    n_results_pgsphere_3_filter_case_4[i], time_pgsphere_3_filter_case_4[i] =\
        pq.run_query(conn, query_3_filter)
    n_results_pgsphere_4_filter_case_4[i], time_pgsphere_4_filter_case_4[i] =\
        pq.run_query(conn, query_4_filter)
    n_results_pgsphere_5_filter_case_4[i], time_pgsphere_5_filter_case_4[i] =\
        pq.run_query(conn, query_5_filter)
    n_results_pgsphere_6_filter_case_4[i], time_pgsphere_6_filter_case_4[i] =\
        pq.run_query(conn, query_6_filter)

    print "(pgSphere) Time elapsed for pgSphere 1 filter : " +\
        str(time_pgsphere_1_filter_case_4[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_1_filter_case_4[i])
    print "(pgSphere) Time elapsed for pgSphere 2 filter : " +\
        str(time_pgsphere_2_filter_case_4[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_2_filter_case_4[i])
    print "(pgSphere) Time elapsed for pgSphere 3 filter : " +\
        str(time_pgsphere_3_filter_case_4[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_3_filter_case_4[i])
    print "(pgSphere) Time elapsed for pgSphere 4 filter : " +\
        str(time_pgsphere_4_filter_case_4[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_4_filter_case_4[i])
    print "(pgSphere) Time elapsed for pgSphere 5 filter : " +\
        str(time_pgsphere_5_filter_case_4[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_5_filter_case_4[i])
    print "(pgSphere) Time elapsed for pgSphere 6 filter : " +\
        str(time_pgsphere_6_filter_case_4[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_6_filter_case_4[i])

    conn.close()



# Case 5
for i in range(n_repeat):
    query_1_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\';"
    query_2_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\';"
    query_3_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\';"
    query_4_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\' " +\
        "AND \"USERID\"=\'Operations\';"
    query_5_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\' " +\
        "AND \"USERID\"=\'Operations\' AND \"TAGID\"=\'LTOps\';"
    query_6_filter =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing WHERE " +\
        "\"GROUPID\"=\'IOO_frodo_magicpixel\' AND " +\
        "\"OBSID\"=\'MULTIPLE_EXPOSURE\' AND \"INSTRUME\"=\'IO:O\' " +\
        "AND \"USERID\"=\'Operations\' AND \"TAGID\"=\'LTOps\' AND " +\
        "\"PROPID\"=\'MiscOpsTestA\';"

    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543"
        )

    n_results_pgsphere_1_filter_case_5[i], time_pgsphere_1_filter_case_5[i] =\
        pq.run_query(conn, query_1_filter)
    n_results_pgsphere_2_filter_case_5[i], time_pgsphere_2_filter_case_5[i] =\
        pq.run_query(conn, query_2_filter)
    n_results_pgsphere_3_filter_case_5[i], time_pgsphere_3_filter_case_5[i] =\
        pq.run_query(conn, query_3_filter)
    n_results_pgsphere_4_filter_case_5[i], time_pgsphere_4_filter_case_5[i] =\
        pq.run_query(conn, query_4_filter)
    n_results_pgsphere_5_filter_case_5[i], time_pgsphere_5_filter_case_5[i] =\
        pq.run_query(conn, query_5_filter)
    n_results_pgsphere_6_filter_case_5[i], time_pgsphere_6_filter_case_5[i] =\
        pq.run_query(conn, query_6_filter)

    print "(pgSphere) Time elapsed for pgSphere 1 filter : " +\
        str(time_pgsphere_1_filter_case_5[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_1_filter_case_5[i])
    print "(pgSphere) Time elapsed for pgSphere 2 filter : " +\
        str(time_pgsphere_2_filter_case_5[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_2_filter_case_5[i])
    print "(pgSphere) Time elapsed for pgSphere 3 filter : " +\
        str(time_pgsphere_3_filter_case_5[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_3_filter_case_5[i])
    print "(pgSphere) Time elapsed for pgSphere 4 filter : " +\
        str(time_pgsphere_4_filter_case_5[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_4_filter_case_5[i])
    print "(pgSphere) Time elapsed for pgSphere 5 filter : " +\
        str(time_pgsphere_5_filter_case_5[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_5_filter_case_5[i])
    print "(pgSphere) Time elapsed for pgSphere 6 filter : " +\
        str(time_pgsphere_6_filter_case_5[i]) + ' No. of matches = ' +\
        str(n_results_pgsphere_6_filter_case_5[i])
    conn.close()


median_time_without_index = np.array((
    np.median(time_direct_1_filter),
    np.median(time_direct_2_filter),
    np.median(time_direct_3_filter),
    np.median(time_direct_4_filter),
    np.median(time_direct_5_filter),
    np.median(time_direct_6_filter)))

median_time_with_index_case_1 = np.array((
    np.median(time_pgsphere_1_filter_case_1),
    np.median(time_pgsphere_2_filter_case_1),
    np.median(time_pgsphere_3_filter_case_1),
    np.median(time_pgsphere_4_filter_case_1),
    np.median(time_pgsphere_5_filter_case_1),
    np.median(time_pgsphere_6_filter_case_1)))

median_time_with_index_case_2 = np.array((
    np.median(time_pgsphere_1_filter_case_2),
    np.median(time_pgsphere_2_filter_case_2),
    np.median(time_pgsphere_3_filter_case_2),
    np.median(time_pgsphere_4_filter_case_2),
    np.median(time_pgsphere_5_filter_case_2),
    np.median(time_pgsphere_6_filter_case_2)))

median_time_with_index_case_3 = np.array((
    np.median(time_pgsphere_1_filter_case_3),
    np.median(time_pgsphere_2_filter_case_3),
    np.median(time_pgsphere_3_filter_case_3),
    np.median(time_pgsphere_4_filter_case_3),
    np.median(time_pgsphere_5_filter_case_3),
    np.median(time_pgsphere_6_filter_case_3)))

median_time_with_index_case_4 = np.array((
    np.median(time_pgsphere_1_filter_case_4),
    np.median(time_pgsphere_2_filter_case_4),
    np.median(time_pgsphere_3_filter_case_4),
    np.median(time_pgsphere_4_filter_case_4),
    np.median(time_pgsphere_5_filter_case_4),
    np.median(time_pgsphere_6_filter_case_4)))

median_time_with_index_case_5 = np.array((
    np.median(time_pgsphere_1_filter_case_5),
    np.median(time_pgsphere_2_filter_case_5),
    np.median(time_pgsphere_3_filter_case_5),
    np.median(time_pgsphere_4_filter_case_5),
    np.median(time_pgsphere_5_filter_case_5),
    np.median(time_pgsphere_6_filter_case_5)))

fig1 = plt.figure(1)
fig1.clf()
ax1 = fig1.add_subplot(111)
ax1.plot(np.arange(1,7),
         median_time_with_index_case_1,
         color='C3',
         label='Case 1'
         )
ax1.plot(np.arange(1,7),
         median_time_with_index_case_2,
         color='C4',
         label='Case 2'
         )
ax1.plot(np.arange(1,7),
         median_time_with_index_case_3,
         color='C0',
         label='Case 3'
         )
ax1.plot(np.arange(1,7),
         median_time_with_index_case_4,
         color='C1',
         label='Case 4'
         )
ax1.plot(np.arange(1,7),
         median_time_with_index_case_5,
         color='C2',
         label='Case 5'
         )
ax1.plot(np.arange(1,7),
         median_time_without_index,
         color='C5',
         label='No index'
         )

ax1.grid()
ax1.set_xlim(1.,6.)
ax1.set_ylim(0.0001,10)
ax1.set_yscale('log')
ax1.set_xlabel('Number of filters')
ax1.set_ylabel('Time taken / seconds')
ax1.legend(loc='center left')
ax1.set_title('PostgreSQL search with multiple B-tree Index')
plt.savefig(output_path + 'psql_Newton_ltarchive_multiple_Btree_timing.png')


median_time_baseline = np.array((
    np.median(time_1),
    np.median(time_2),
    np.median(time_3),
    np.median(time_4),
    np.median(time_5),
    np.median(time_6)))

print "The baseline for the 6 filters are " + str(median_time_baseline)


fig2 = plt.figure(2)
fig2.clf()
ax2 = fig2.add_subplot(111)
ax2.scatter(n_results_1, np.median(time_1), color='C1', label='INSTRUME')
ax2.scatter(n_results_2, np.median(time_2), color='C2', label='TAGID')
ax2.scatter(n_results_3, np.median(time_3), color='C3', label='USERID')
ax2.scatter(n_results_4, np.median(time_4), color='C4', label='PROPID')
ax2.scatter(n_results_5, np.median(time_5), color='C5', label='OBSID')
ax2.scatter(n_results_6, np.median(time_6), color='C6', label='GROUPID')
ax2.grid()
ax2.set_xlabel('Number of distinct entries')
ax2.set_ylabel('Time taken / seconds')
ax2.set_xscale('log')
ax2.legend()
ax2.set_title('PostgreSQL search with multiple B-tree Index')
plt.savefig(output_path + 'psql_Newton_ltarchive_Btree_baseline_timing.png')
