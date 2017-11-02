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
import random
from psql_functions import PsqlQuery
try:
    matplotlib.use('TkAgg')
except:
    pass

from matplotlib.gridspec import GridSpec
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
n_repeat = 10000

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






# GIN index
n_results_gin_partial = np.zeros(n_repeat)
time_gin_partial = np.zeros(n_repeat)

# B-tree index
n_results_btree_partial = np.zeros(n_repeat)
time_btree_partial = np.zeros(n_repeat)

# Hash index
n_results_hash_partial = np.zeros(n_repeat)
time_hash_partial = np.zeros(n_repeat)

for i in range(n_repeat):
    print "Run " + str(i+1) + " of " + str(n_repeat)
    # Pick two columns
    column1_gin = "\"PROPID_tsvector\""
    phrase1 = None
    while (phrase1 == None) or (phrase1 == ''):
        phrase1 = np.random.choice(np.ndarray.flatten(propid_list), 1)[0]
    phrase1 = phrase1[:3]
    # constructing the query statement
    query_gin =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
        column1_gin + " @@ to_tsquery('" + phrase1 + ":*');"
    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  
    # Run the queries and save the results in arrays
    n_temp_gin, time_temp_gin = pq.run_query(conn, query_gin)
    n_results_gin_partial[i], time_gin_partial[i] = n_temp_gin, time_temp_gin
    conn.close()


for i in range(n_repeat):
    print "Run " + str(i+1) + " of " + str(n_repeat)
    # Pick two columns
    column1 = "\"PROPID\""
    phrase1 = None
    while (phrase1 == None) or (phrase1 == ''):
        phrase1 = np.random.choice(np.ndarray.flatten(propid_list), 1)[0]
    phrase1 = phrase1[:3]
    # constructing the query statement
    query_btree =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
        column1 + " LIKE '" + phrase1 + "%';"
    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  
    # Run the queries and save the results in arrays
    n_temp_btree, time_temp_btree = pq.run_query(conn, query_btree)
    n_results_btree_partial[i], time_btree_partial[i] = n_temp_btree, time_temp_btree
    conn.close()


for i in range(n_repeat):
    print "Run " + str(i+1) + " of " + str(n_repeat)
    # Pick two columns
    column1 = "\"PROPID\""
    phrase1 = None
    while (phrase1 == None) or (phrase1 == ''):
        phrase1 = np.random.choice(np.ndarray.flatten(propid_list), 1)[0]
    phrase1 = phrase1[:3]
    # constructing the query statement
    query_hash =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
        column1 + " LIKE '" + phrase1 + "%';"
    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  
    # Run the queries and save the results in arrays
    n_temp_hash, time_temp_hash = pq.run_query(conn, query_hash)
    n_results_hash_partial[i], time_hash_partial[i] = n_temp_hash, time_temp_hash
    conn.close()


fig3 = plt.figure(3,figsize=(10,6))
fig3.clf()
gridspec = GridSpec(1, 3)
gridspec.update(left=0.12,right=0.95,top=0.98,bottom=0.1,wspace=0)

ax1 = fig3.add_subplot(gridspec[0,0])
ax2 = fig3.add_subplot(gridspec[0,1])
ax3 = fig3.add_subplot(gridspec[0,2])

ax1.scatter(np.log10(n_results_hash_partial), np.log10(time_hash_partial), s=2)
ax2.scatter(np.log10(n_results_btree_partial), np.log10(time_btree_partial), s=2)
ax3.scatter(np.log10(n_results_gin_partial), np.log10(time_gin_partial), s=2)


ax2.set_xlabel('Number of matches')

ax1.set_ylabel('Query Time / s')

ax1.grid()
ax2.grid()
ax3.grid()

ax1.set_xlim(0,6)
ax2.set_xlim(0,6)
ax3.set_xlim(0,6)

ax1.set_ylim(-4,2)
ax2.set_ylim(-4,2)
ax3.set_ylim(-4,2)

ax1.set_yticklabels([r'$10^{-4}$',r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^{0}$',r'$10^{1}$',r'$10^{2}$'])
ax2.set_yticklabels([''])
ax3.set_yticklabels([''])

ax1.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$'])
ax2.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$'])
ax3.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$',r'$10^{6}$'])

plt.savefig(output_path + 'query_time_hash_btree_gin_partial_compared.png')




# GIN index
n_results_gin_partial_2 = np.zeros(n_repeat)
time_gin_partial_2 = np.zeros(n_repeat)

# B-tree index
n_results_btree_partial_2 = np.zeros(n_repeat)
time_btree_partial_2 = np.zeros(n_repeat)

# Hash index
n_results_hash_partial_2 = np.zeros(n_repeat)
time_hash_partial_2 = np.zeros(n_repeat)

for i in range(n_repeat):
    print "Run " + str(i+1) + " of " + str(n_repeat)
    # Pick two columns
    phrase1 = None
    while (phrase1 == None) or (phrase1 == ''):
        phrase1 = np.random.choice(np.ndarray.flatten(propid_list), 1)[0]
    phrase1 = phrase1[:3]
    phrase2 = None
    while (phrase2 == None) or (phrase2 == ''):
        phrase2 = np.random.choice(np.ndarray.flatten(instrume_list), 1)[0]
    column1_gin = "\"PROPID_tsvector\""
    column2 = "\"INSTRUME\""
    # constructing the query statement
    query_gin =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_gin WHERE " +\
        column1_gin + " @@ to_tsquery('" + phrase1 + ":*') AND " +\
        column2 + " = '" + phrase2 + "';"
    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  
    # Run the queries and save the results in arrays
    n_temp_gin, time_temp_gin = pq.run_query(conn, query_gin)
    n_results_gin_partial_2[i], time_gin_partial_2[i] = n_temp_gin, time_temp_gin
    conn.close()



for i in range(n_repeat):
    print "Run " + str(i+1) + " of " + str(n_repeat)
    # Pick two columns
    phrase1 = None
    while (phrase1 == None) or (phrase1 == ''):
        phrase1 = np.random.choice(np.ndarray.flatten(propid_list), 1)[0]
    phrase1 = phrase1[:3]
    phrase2 = None
    while (phrase2 == None) or (phrase2 == ''):
        phrase2 = np.random.choice(np.ndarray.flatten(instrume_list), 1)[0]
    column1 = "\"PROPID\""
    column2 = "\"INSTRUME\""
    # constructing the query statement
    query_btree =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
        column1 + " LIKE '" + phrase1 + "%' AND " +\
        column2 + " = '" + phrase2 + "';"
    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  
    # Run the queries and save the results in arrays
    n_temp_btree, time_temp_btree = pq.run_query(conn, query_btree)
    n_results_btree_partial_2[i], time_btree_partial_2[i] = n_temp_btree, time_temp_btree
    conn.close()


for i in range(n_repeat):
    print "Run " + str(i+1) + " of " + str(n_repeat)
    # Pick two columns
    phrase1 = None
    while (phrase1 == None) or (phrase1 == ''):
        phrase1 = np.random.choice(np.ndarray.flatten(propid_list), 1)[0]
    phrase1 = phrase1[:3]
    phrase2 = None
    while (phrase2 == None) or (phrase2 == ''):
        phrase2 = np.random.choice(np.ndarray.flatten(instrume_list), 1)[0]
    column1 = "\"PROPID\""
    column2 = "\"INSTRUME\""
    # constructing the query statement
    query_hash =\
        "EXPLAIN ANALYSE SELECT * FROM allkeys_testing_hash WHERE " +\
        column1 + " LIKE '" + phrase1 + "%' AND " +\
        column2 + " = '" + phrase2 + "';"
    # Connect to the database
    conn = psycopg2.connect(
        database="ltarchive",
        user="dbuser",
        password="dbuser",
        host="150.204.240.113",
        port="6543")  
    # Run the queries and save the results in arrays
    n_temp_hash, time_temp_hash = pq.run_query(conn, query_hash)
    n_results_hash_partial_2[i], time_hash_partial_2[i] = n_temp_hash, time_temp_hash
    conn.close()


fig4 = plt.figure(4,figsize=(10,6))
fig4.clf()
gridspec = GridSpec(1, 3)
gridspec.update(left=0.12,right=0.95,top=0.98,bottom=0.1,wspace=0)

ax1 = fig4.add_subplot(gridspec[0,0])
ax2 = fig4.add_subplot(gridspec[0,1])
ax3 = fig4.add_subplot(gridspec[0,2])

ax1.scatter(np.log10(n_results_hash_partial_2), np.log10(time_hash_partial_2), s=2)
ax2.scatter(np.log10(n_results_btree_partial_2), np.log10(time_btree_partial_2), s=2)
ax3.scatter(np.log10(n_results_gin_partial_2), np.log10(time_gin_partial_2), s=2)

ax2.set_xlabel('Number of matches')
ax1.set_ylabel('Query Time / s')

ax1.grid()
ax2.grid()
ax3.grid()

ax1.set_xlim(0,6)
ax2.set_xlim(0,6)
ax3.set_xlim(0,6)

ax1.set_ylim(-4.0,2)
ax2.set_ylim(-4.0,2)
ax3.set_ylim(-4.0,2)

ax1.set_yticklabels([r'$10^{-4}$', r'$10^{-3}$',r'$10^{-2}$',r'$10^{-1}$',r'$10^{0}$',r'$10^{1}$',r'$10^{2}$'])
ax2.set_yticklabels([''])
ax3.set_yticklabels([''])

ax1.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$'])
ax2.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$'])
ax3.set_xticklabels([r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$',r'$10^{5}$',r'$10^{6}$'])

ax1.plot(np.log10(hash_sample), np.log10(itp.splev(hash_sample, hash_itp)))
ax2.plot(np.log10(btree_sample), np.log10(itp.splev(btree_sample, btree_itp)))
ax3.plot(np.log10(gin_sample), np.log10(itp.splev(gin_sample, gin_itp)))

plt.savefig(output_path + 'query_time_hash_btree_gin_double_filters_partial_compared.png')



