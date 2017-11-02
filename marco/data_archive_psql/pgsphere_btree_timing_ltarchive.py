#!/usr/bin/python

'''
    File name: pgsphere_btree_timing_ltarchive.py
    Prepared by: MCL
    Date created: 14/8/2017
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

# Cone search parameters
min_radius = 2.5
max_radius = np.log10(30. * 3600.)  # (arcsecs)
n_interval = 100
n_repeat = 10
n_interval_direct = 5
n_repeat_direct = 5

# Set the search radius (degrees)
radii_pgsphere =\
    10.**np.linspace(min_radius, max_radius, n_interval) / 3600.

# Create zero arrays for the number of results and execution times
time_pgsphere_only_gc = np.zeros((n_repeat, n_interval))
n_results_pgsphere_only_gc = np.zeros((n_repeat, n_interval))
time_btree_only_gc = np.zeros((n_repeat, n_interval))
n_results_btree_only_gc = np.zeros((n_repeat, n_interval))
time_pgsphere_btree_gc = np.zeros((n_repeat, n_interval))
n_results_pgsphere_btree_gc = np.zeros((n_repeat, n_interval))
time_pgsphere_only_gnp = np.zeros((n_repeat, n_interval))
n_results_pgsphere_only_gnp = np.zeros((n_repeat, n_interval))
time_btree_only_gnp = np.zeros((n_repeat, n_interval))
n_results_btree_only_gnp = np.zeros((n_repeat, n_interval))
time_pgsphere_btree_gnp = np.zeros((n_repeat, n_interval))
n_results_pgsphere_btree_gnp = np.zeros((n_repeat, n_interval))

# Repeating the queries n_repeat times
for j in range(n_repeat):

    # Loop through the list of radii
    for i, radius in enumerate(radii_pgsphere):
        print "run " + str(j+1) + " of " + str(n_repeat) + " and " +\
            str(i+1) + " of " + len(radii_pgsphere)

        # Prepare the PostgreSQL queries
        query_pgsphere_only_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_gc) + "), RADIANS(" +\
            str(dec_gc) + ")), RADIANS(" + str(radius) +\
            "))~coords AND \"INSTRUME\"=\'IO:O\';"
        query_btree_only_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "vincenty(" + str(dec_gc) + ", " + str(ra_gc) +\
            ", dec_degree, ra_degree) <= " + str(radius) +\
            " AND \"INSTRUME\"=\'IO:O\';"
        query_pgsphere_btree_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
            "WHERE scircle(spoint(radians(" + str(ra_gc) +\
            "), RADIANS(" + str(dec_gc) + ")), RADIANS(" +\
            str(radius) + "))~coords AND \"INSTRUME\"=\'IO:O\';"
        query_pgsphere_only_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(RADIANS(" + str(ra_gnp) + "), RADIANS(" +\
            str(dec_gnp) + ")), RADIANS(" + str(radius) +\
            "))~coords AND \"INSTRUME\"=\'IO:O\';"
        query_btree_only_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "vincenty(" + str(dec_gnp) + ", " + str(ra_gnp) +\
            ", dec_degree, ra_degree) <= " + str(radius) +\
            " AND \"INSTRUME\"=\'IO:O\';"
        query_pgsphere_btree_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
            "WHERE scircle(spoint(radians(" + str(ra_gnp) +\
            "), RADIANS(" + str(dec_gnp) + ")), RADIANS(" +\
            str(radius) +\
            "))~coords AND \"INSTRUME\"=\'IO:O\';"

        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543"
            )

        # Run the queries and save the results in arrays
        n_results_pgsphere_only_gc[j][i], time_pgsphere_only_gc[j][i] =\
            pq.run_query(conn, query_pgsphere_only_gc)
        n_results_btree_only_gc[j][i], time_btree_only_gc[j][i] =\
            pq.run_query(conn, query_btree_only_gc)
        n_results_pgsphere_btree_gc[j][i], time_pgsphere_btree_gc[j][i] =\
            pq.run_query(conn, query_pgsphere_btree_gc)
        n_results_pgsphere_only_gnp[j][i], time_pgsphere_only_gnp[j][i] =\
            pq.run_query(conn, query_pgsphere_only_gnp)
        n_results_btree_only_gnp[j][i], time_btree_only_gnp[j][i] =\
            pq.run_query(conn, query_btree_only_gnp)
        n_results_pgsphere_btree_gnp[j][i], time_pgsphere_btree_gnp[j][i] =\
            pq.run_query(conn, query_pgsphere_btree_gnp)

        # Print results
        print "(pgSphere GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_only_gc[j][i]) + ' No. of matches = ' +\
            str(n_results_pgsphere_only_gc[j][i])
        print "(B-Tree GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_btree_only_gc[j][i]) + ' No. of matches = ' +\
            str(n_results_btree_only_gc[j][i])
        print "(pgSphere + B-Tree GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_btree_gc[j][i]) + ' No. of matches = ' +\
            str(n_results_pgsphere_btree_gc[j][i])
        print "(pgSphere GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_only_gnp[j][i]) + ' No. of matches = ' +\
            str(n_results_pgsphere_only_gnp[j][i])
        print "(B-Tree GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_btree_only_gnp[j][i]) + ' No. of matches = ' +\
            str(n_results_btree_only_gnp[j][i])
        print "(pgSphere + B-Tree GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_btree_gnp[j][i]) + ' No. of matches = ' +\
            str(n_results_pgsphere_btree_gnp[j][i])

        # Terminate connection to the database
        conn.close()


# Set the search radius (arcsec)
radii_direct = 10.**np.linspace(2.5, max_radius, n_interval_direct)

# Create zero arrays for the number of results and execution times
time_direct_gc = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gc = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_gnp = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gnp = np.zeros((n_repeat_direct, n_interval_direct))

# Repeating the queries n_repeat_direct times
for j in range(n_repeat_direct):
    print "run " + str(j+1) + " of " + str(n_repeat_direct)

    # Loop through the list of radii
    for i, radius in enumerate(radii_direct):

        # Prepare the PostgreSQL queries
        query_direct_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE vincenty(" +\
            str(dec_gnp) + ", " + str(ra_gnp) +\
            ", dec_degree, ra_degree) <= " + str(radius / 3600.) +\
            " AND \"INSTRUME\"=\'IO:O\';"
        query_direct_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE vincenty(" +\
            str(dec_gc) + ", " + str(ra_gc) +\
            ", dec_degree, ra_degree) <= " + str(radius / 3600.) +\
            " AND \"INSTRUME\"=\'IO:O\';"

        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")

        # Run the queries and save the results in arrays
        n_results_direct_gnp[j][i], time_direct_gnp[j][i] =\
            pq.run_query(conn, query_direct_gnp)
        n_results_direct_gc[j][i], time_direct_gc[j][i] =\
            pq.run_query(conn, query_direct_gc)

        # Print results
        print "(Direct GC) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gc[j][i]) +\
            ' No. of matches = ' + str(n_results_direct_gc[j][i])
        print "(Direct GNP) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gnp[j][i]) +\
            ' No. of matches = ' + str(n_results_direct_gnp[j][i])

        # Terminate connection to the database
        conn.close()


# Create a log-log plot
fig1 = plt.figure(1)
fig1.clf()
ax1 = fig1.add_subplot(111)
ax2 = ax1.twinx()
# GC
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_only_gc, axis=0),
         color='C0',
         label='(GC) pgSphere')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_btree_only_gc, axis=0),
         color='C1',
         label='(GC) B-Tree')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_btree_gc, axis=0),
         color='C2',
         label='(GC) pgSphere + B-Tree')
ax1.plot(radii_direct,
         np.median(time_direct_gc, axis=0),
         color='C3',
         label='(GC) Direct')
# GNP
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_only_gnp, axis=0),
         color='C0',
         ls=':',
         label='(GNP) pgSphere')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_btree_only_gnp, axis=0),
         color='C1',
         ls=':',
         label='(GNP) B-Tree')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_btree_gnp, axis=0),
         color='C2',
         ls=':',
         label='(GNP) pgSphere + B-Tree')
ax1.plot(radii_direct,
         np.median(time_direct_gnp, axis=0),
         color='C3',
         ls=':',
         label='(GNP) Direct')
# Number count
ax2.plot(radii_pgsphere * 3600.,
         np.median(n_results_pgsphere_only_gc, axis=0),
         color='C4',
         label='(GC)')
ax2.plot(radii_pgsphere * 3600.,
         np.median(n_results_pgsphere_only_gnp, axis=0),
         color='C4',
         ls=':',
         label='(GNP)')

ax1.grid()
ax1.set_xlim(10.**min_radius, 10.**max_radius)
ax1.set_ylim(0.0001, 50.)
ax2.set_ylim(0.1, 50000.)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_xlabel('Search radius / arcsec')
ax1.set_ylabel('Time taken / seconds')
ax2.set_ylabel('Number of results')
ax1.legend(loc='upper left')
ax2.legend(loc='lower right')
ax1.set_title('PostgreSQL search with pgSphere and INSTRUME B-Tree')
plt.savefig(output_path + "psql_Newton_ltarchive_pgSphere_BTree_instrume.png")




# Consider GROUPID that exist in the database but not without the search
# radius


# Create zero arrays for the number of results and execution times
time_pgsphere_only_gc_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_only_gc_groupid = np.zeros((n_repeat, n_interval))
time_btree_only_gc_groupid = np.zeros((n_repeat, n_interval))
n_results_btree_only_gc_groupid = np.zeros((n_repeat, n_interval))
time_pgsphere_btree_gc_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_btree_gc_groupid = np.zeros((n_repeat, n_interval))
time_pgsphere_only_gnp_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_only_gnp_groupid = np.zeros((n_repeat, n_interval))
time_btree_only_gnp_groupid = np.zeros((n_repeat, n_interval))
n_results_btree_only_gnp_groupid = np.zeros((n_repeat, n_interval))
time_pgsphere_btree_gnp_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_btree_gnp_groupid = np.zeros((n_repeat, n_interval))

# Repeating the queries n_repeat times
for j in range(n_repeat):
    # Loop through the list of radii
    for i, radius in enumerate(radii_pgsphere):
        print "run " + str(j+1) + " of " + str(n_repeat) + " and " +\
            str(i+1) + " of " + str(len(radii_pgsphere))
        # Prepare the PostgreSQL queries
        query_pgsphere_only_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_gc) + "), RADIANS(" +\
            str(dec_gc) + ")), RADIANS(" + str(radius) +\
            "))~coords AND \"GROUPID\"=\'WD1145+017\';"
        query_btree_only_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "vincenty(" + str(dec_gc) + ", " + str(ra_gc) +\
            ", dec_degree, ra_degree) <= " + str(radius) +\
            " AND \"GROUPID\"=\'WD1145+017\';"
        query_pgsphere_btree_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
            "WHERE scircle(spoint(radians(" + str(ra_gc) +\
            "), RADIANS(" + str(dec_gc) + ")), RADIANS(" +\
            str(radius) + "))~coords AND \"GROUPID\"=\'WD1145+017\';"
        query_pgsphere_only_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(RADIANS(" + str(ra_gnp) + "), RADIANS(" +\
            str(dec_gnp) + ")), RADIANS(" + str(radius) +\
            "))~coords AND \"GROUPID\"=\'WD1145+017\';"
        query_btree_only_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "vincenty(" + str(dec_gnp) + ", " + str(ra_gnp) +\
            ", dec_degree, ra_degree) <= " + str(radius) +\
            " AND \"GROUPID\"=\'WD1145+017\';"
        query_pgsphere_btree_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
            "WHERE scircle(spoint(radians(" + str(ra_gnp) +\
            "), RADIANS(" + str(dec_gnp) + ")), RADIANS(" +\
            str(radius) +\
            "))~coords AND \"GROUPID\"=\'WD1145+017\';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543"
            )
        # Run the queries and save the results in arrays
        n_results_pgsphere_only_gc_groupid[j][i],\
            time_pgsphere_only_gc_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_only_gc_groupid)
        n_results_btree_only_gc_groupid[j][i],\
            time_btree_only_gc_groupid[j][i] =\
            pq.run_query(conn, query_btree_only_gc_groupid)
        n_results_pgsphere_btree_gc_groupid[j][i],\
            time_pgsphere_btree_gc_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_btree_gc_groupid)
        n_results_pgsphere_only_gnp_groupid[j][i], time_pgsphere_only_gnp_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_only_gnp_groupid)
        n_results_btree_only_gnp_groupid[j][i],\
            time_btree_only_gnp_groupid[j][i] =\
            pq.run_query(conn, query_btree_only_gnp_groupid)
        n_results_pgsphere_btree_gnp_groupid[j][i],\
            time_pgsphere_btree_gnp_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_btree_gnp_groupid)
        # Print results
        print "(pgSphere GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_only_gc_groupid[j][i]) + ' No. of matches = ' +\
            str(n_results_pgsphere_only_gc_groupid[j][i])
        print "(B-Tree GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_btree_only_gc_groupid[j][i]) + ' No. of matches = ' +\
            str(n_results_btree_only_gc_groupid[j][i])
        print "(pgSphere + B-Tree GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_btree_gc_groupid[j][i]) +\
            ' No. of matches = ' +\
            str(n_results_pgsphere_btree_gc_groupid[j][i])
        print "(pgSphere GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_only_gnp_groupid[j][i]) +\
            ' No. of matches = ' +\
            str(n_results_pgsphere_only_gnp_groupid[j][i])
        print "(B-Tree GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_btree_only_gnp_groupid[j][i]) + ' No. of matches = ' +\
            str(n_results_btree_only_gnp_groupid[j][i])
        print "(pgSphere + B-Tree GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_btree_gnp_groupid[j][i]) +\
            ' No. of matches = ' +\
            str(n_results_pgsphere_btree_gnp_groupid[j][i])
        # Terminate connection to the database
        conn.close()


# Set the search radius (arcsec)
radii_direct = 10.**np.linspace(2.5, max_radius, n_interval_direct)

# Create zero arrays for the number of results and execution times
time_direct_gc_groupid = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gc_groupid = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_gnp_groupid = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gnp_groupid = np.zeros((n_repeat_direct, n_interval_direct))

# Repeating the queries n_repeat_direct times
for j in range(n_repeat_direct):
    print "run " + str(j+1) + " of " + str(n_repeat_direct)
    # Loop through the list of radii
    for i, radius in enumerate(radii_direct):
        # Prepare the PostgreSQL queries
        query_direct_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE vincenty(" +\
            str(dec_gnp) + ", " + str(ra_gnp) +\
            ", dec_degree, ra_degree) <= " + str(radius / 3600.) +\
            " AND \"GROUPID\"=\'WD1145+017\';"
        query_direct_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE vincenty(" +\
            str(dec_gc) + ", " + str(ra_gc) +\
            ", dec_degree, ra_degree) <= " + str(radius / 3600.) +\
            " AND \"GROUPID\"=\'WD1145+017\';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")
        # Run the queries and save the results in arrays
        n_results_direct_gnp_groupid[j][i], time_direct_gnp_groupid[j][i] =\
            pq.run_query(conn, query_direct_gnp_groupid)
        n_results_direct_gc_groupid[j][i], time_direct_gc_groupid[j][i] =\
            pq.run_query(conn, query_direct_gc_groupid)
        # Print results
        print "(Direct GC) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gc_groupid[j][i]) +\
            ' No. of matches = ' + str(n_results_direct_gc_groupid[j][i])
        print "(Direct GNP) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gnp_groupid[j][i]) +\
            ' No. of matches = ' + str(n_results_direct_gnp_groupid[j][i])
        # Terminate connection to the database
        conn.close()


# Create a log-log plot
fig1 = plt.figure(1)
fig1.clf()
ax1 = fig1.add_subplot(111)
ax2 = ax1.twinx()
# GC
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_only_gc_groupid, axis=0),
         color='C0',
         label='(GC) pgSphere')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_btree_only_gc_groupid, axis=0),
         color='C1',
         label='(GC) B-Tree')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_btree_gc_groupid, axis=0),
         color='C2',
         label='(GC) pgSphere + B-Tree')
ax1.plot(radii_direct,
         np.median(time_direct_gc_groupid, axis=0),
         color='C3',
         label='(GC) Direct')
# GNP
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_only_gnp_groupid, axis=0),
         color='C0',
         ls=':',
         label='(GNP) pgSphere')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_btree_only_gnp_groupid, axis=0),
         color='C1',
         ls=':',
         label='(GNP) B-Tree')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_btree_gnp_groupid, axis=0),
         color='C2',
         ls=':',
         label='(GNP) pgSphere + B-Tree')
ax1.plot(radii_direct,
         np.median(time_direct_gnp_groupid, axis=0),
         color='C3',
         ls=':',
         label='(GNP) Direct')

ax1.grid()
ax1.set_xlim(10.**min_radius, 10.**max_radius)
ax1.set_ylim(0.0001, 50.)
ax2.set_ylim(0.1, 50000.)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_xlabel('Search radius / arcsec')
ax1.set_ylabel('Time taken / seconds')
ax2.set_ylabel('Number of results')
ax1.legend(loc='upper left')
ax2.legend(loc='center right')
ax1.set_title('PostgreSQL search with pgSphere and GROUPID B-Tree')
plt.savefig(output_path + "psql_Newton_ltarchive_pgSphere_BTree_groupid.png")




# Consider GROUPID that does not exist in the database


# Create zero arrays for the number of results and execution times
time_pgsphere_only_gc_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_only_gc_groupid = np.zeros((n_repeat, n_interval))
time_btree_only_gc_groupid = np.zeros((n_repeat, n_interval))
n_results_btree_only_gc_groupid = np.zeros((n_repeat, n_interval))
time_pgsphere_btree_gc_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_btree_gc_groupid = np.zeros((n_repeat, n_interval))
time_pgsphere_only_gnp_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_only_gnp_groupid = np.zeros((n_repeat, n_interval))
time_btree_only_gnp_groupid = np.zeros((n_repeat, n_interval))
n_results_btree_only_gnp_groupid = np.zeros((n_repeat, n_interval))
time_pgsphere_btree_gnp_groupid = np.zeros((n_repeat, n_interval))
n_results_pgsphere_btree_gnp_groupid = np.zeros((n_repeat, n_interval))

# Repeating the queries n_repeat times
for j in range(n_repeat):
    # Loop through the list of radii
    for i, radius in enumerate(radii_pgsphere):
        print "run " + str(j+1) + " of " + str(n_repeat) + " and " +\
            str(i+1) + " of " + str(len(radii_pgsphere))
        # Prepare the PostgreSQL queries
        query_pgsphere_only_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_gc) + "), RADIANS(" +\
            str(dec_gc) + ")), RADIANS(" + str(radius) +\
            "))~coords AND \"GROUPID\"=\'DOES_NOT_EXIST\';"
        query_btree_only_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "vincenty(" + str(dec_gc) + ", " + str(ra_gc) +\
            ", dec_degree, ra_degree) <= " + str(radius) +\
            " AND \"GROUPID\"=\'DOES_NOT_EXIST\';"
        query_pgsphere_btree_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
            "WHERE scircle(spoint(radians(" + str(ra_gc) +\
            "), RADIANS(" + str(dec_gc) + ")), RADIANS(" +\
            str(radius) + "))~coords AND \"GROUPID\"=\'DOES_NOT_EXIST\';"
        query_pgsphere_only_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(RADIANS(" + str(ra_gnp) + "), RADIANS(" +\
            str(dec_gnp) + ")), RADIANS(" + str(radius) +\
            "))~coords AND \"GROUPID\"=\'DOES_NOT_EXIST\';"
        query_btree_only_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_testing WHERE " +\
            "vincenty(" + str(dec_gnp) + ", " + str(ra_gnp) +\
            ", dec_degree, ra_degree) <= " + str(radius) +\
            " AND \"GROUPID\"=\'DOES_NOT_EXIST\';"
        query_pgsphere_btree_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere_testing " +\
            "WHERE scircle(spoint(radians(" + str(ra_gnp) +\
            "), RADIANS(" + str(dec_gnp) + ")), RADIANS(" +\
            str(radius) +\
            "))~coords AND \"GROUPID\"=\'DOES_NOT_EXIST\';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543"
            )
        # Run the queries and save the results in arrays
        n_results_pgsphere_only_gc_groupid[j][i],\
            time_pgsphere_only_gc_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_only_gc_groupid)
        n_results_btree_only_gc_groupid[j][i],\
            time_btree_only_gc_groupid[j][i] =\
            pq.run_query(conn, query_btree_only_gc_groupid)
        n_results_pgsphere_btree_gc_groupid[j][i],\
            time_pgsphere_btree_gc_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_btree_gc_groupid)
        n_results_pgsphere_only_gnp_groupid[j][i], time_pgsphere_only_gnp_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_only_gnp_groupid)
        n_results_btree_only_gnp_groupid[j][i],\
            time_btree_only_gnp_groupid[j][i] =\
            pq.run_query(conn, query_btree_only_gnp_groupid)
        n_results_pgsphere_btree_gnp_groupid[j][i],\
            time_pgsphere_btree_gnp_groupid[j][i] =\
            pq.run_query(conn, query_pgsphere_btree_gnp_groupid)
        # Print results
        print "(pgSphere GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_only_gc_groupid[j][i]) + ' No. of matches = ' +\
            str(n_results_pgsphere_only_gc_groupid[j][i])
        print "(B-Tree GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_btree_only_gc_groupid[j][i]) + ' No. of matches = ' +\
            str(n_results_btree_only_gc_groupid[j][i])
        print "(pgSphere + B-Tree GC) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_btree_gc_groupid[j][i]) +\
            ' No. of matches = ' +\
            str(n_results_pgsphere_btree_gc_groupid[j][i])
        print "(pgSphere GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_only_gnp_groupid[j][i]) +\
            ' No. of matches = ' +\
            str(n_results_pgsphere_only_gnp_groupid[j][i])
        print "(B-Tree GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_btree_only_gnp_groupid[j][i]) + ' No. of matches = ' +\
            str(n_results_btree_only_gnp_groupid[j][i])
        print "(pgSphere + B-Tree GNP) Time elapsed for search radius " +\
            str(radius * 3600.) + " arcsec : " +\
            str(time_pgsphere_btree_gnp_groupid[j][i]) +\
            ' No. of matches = ' +\
            str(n_results_pgsphere_btree_gnp_groupid[j][i])
        # Terminate connection to the database
        conn.close()


# Set the search radius (arcsec)
radii_direct = 10.**np.linspace(2.5, max_radius, n_interval_direct)

# Create zero arrays for the number of results and execution times
time_direct_gc_groupid = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gc_groupid = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_gnp_groupid = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gnp_groupid = np.zeros((n_repeat_direct, n_interval_direct))

# Repeating the queries n_repeat_direct times
for j in range(n_repeat_direct):
    print "run " + str(j+1) + " of " + str(n_repeat_direct)
    # Loop through the list of radii
    for i, radius in enumerate(radii_direct):
        # Prepare the PostgreSQL queries
        query_direct_gnp_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE vincenty(" +\
            str(dec_gnp) + ", " + str(ra_gnp) +\
            ", dec_degree, ra_degree) <= " + str(radius / 3600.) +\
            " AND \"GROUPID\"=\'IOO_frodo_magicpixel\';"
        query_direct_gc_groupid =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys WHERE vincenty(" +\
            str(dec_gc) + ", " + str(ra_gc) +\
            ", dec_degree, ra_degree) <= " + str(radius / 3600.) +\
            " AND \"GROUPID\"=\'IOO_frodo_magicpixel\';"
        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543")
        # Run the queries and save the results in arrays
        n_results_direct_gnp_groupid[j][i], time_direct_gnp_groupid[j][i] =\
            pq.run_query(conn, query_direct_gnp_groupid)
        n_results_direct_gc_groupid[j][i], time_direct_gc_groupid[j][i] =\
            pq.run_query(conn, query_direct_gc_groupid)
        # Print results
        print "(Direct GC) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gc_groupid[j][i]) +\
            ' No. of matches = ' + str(n_results_direct_gc_groupid[j][i])
        print "(Direct GNP) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gnp_groupid[j][i]) +\
            ' No. of matches = ' + str(n_results_direct_gnp_groupid[j][i])
        # Terminate connection to the database
        conn.close()


# Create a log-log plot
fig1 = plt.figure(1)
fig1.clf()
ax1 = fig1.add_subplot(111)
ax2 = ax1.twinx()
# GC
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_only_gc_groupid, axis=0),
         color='C0',
         label='(GC) pgSphere')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_btree_only_gc_groupid, axis=0),
         color='C1',
         label='(GC) B-Tree')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_btree_gc_groupid, axis=0),
         color='C2',
         label='(GC) pgSphere + B-Tree')
ax1.plot(radii_direct,
         np.median(time_direct_gc_groupid, axis=0),
         color='C3',
         label='(GC) Direct')
# GNP
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_only_gnp_groupid, axis=0),
         color='C0',
         ls=':',
         label='(GNP) pgSphere')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_btree_only_gnp_groupid, axis=0),
         color='C1',
         ls=':',
         label='(GNP) B-Tree')
ax1.plot(radii_pgsphere * 3600.,
         np.median(time_pgsphere_btree_gnp_groupid, axis=0),
         color='C2',
         ls=':',
         label='(GNP) pgSphere + B-Tree')
ax1.plot(radii_direct,
         np.median(time_direct_gnp_groupid, axis=0),
         color='C3',
         ls=':',
         label='(GNP) Direct')


ax1.grid()
ax1.set_xlim(10.**min_radius, 10.**max_radius)
ax1.set_ylim(0.0001, 50.)
ax2.set_ylim(0.1, 50000.)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_xlabel('Search radius / arcsec')
ax1.set_ylabel('Time taken / seconds')
ax2.set_ylabel('Number of results')
ax1.legend(loc='upper left')
ax2.legend(loc='center right')
ax1.set_title('PostgreSQL search with pgSphere and B-Tree with no match')
plt.savefig(output_path + "psql_Newton_ltarchive_pgSphere_BTree_return_none.png")
