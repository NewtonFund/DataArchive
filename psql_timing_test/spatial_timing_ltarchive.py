#!/usr/bin/python

'''
    File name: spatial_timing_ltarchive.py
    Prepared by: MCL
    Date created: 9/8/2017
    Date last modified: 16/8/2017
    Python Version: 2.7

    This script compares the run time of PostgreSQL queries by position,
    3 cases are compared:
    (1) Database with Q3C index
    (2) Database with pgSphere index
    (3) Database without index
'''

import os
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
    output_path = os.path.expanduser('~') + "/Desktop/"

# Equatorial coordinates of the Galactic Centre
ra_gc = 266.41683
dec_gc = -29.00781

# Equatorial coordinates of the Galactic North Pole
ra_gnp = 192.85951
dec_gnp = 27.12834

# Cone search parameters
min_radius = 0.
max_radius = np.log10(30. * 3600.)  # (arcsecs)
n_interval = 100
n_repeat = 10
n_interval_direct = 5
n_repeat_direct = 5

# Set the search radius (degrees)
radii_q3c = 10.**np.linspace(min_radius, max_radius, n_interval)
radii_pgsphere = 10.**np.linspace(min_radius, max_radius, n_interval)
radii_direct = 10.**np.linspace(min_radius, max_radius, n_interval_direct)

# Create zero arrays for the number of results and execution times
time_q3c_gc = np.zeros((n_repeat, n_interval))
n_results_q3c_gc = np.zeros((n_repeat, n_interval))
time_q3c_gnp = np.zeros((n_repeat, n_interval))
n_results_q3c_gnp = np.zeros((n_repeat, n_interval))

time_pgsphere_gc = np.zeros((n_repeat, n_interval))
n_results_pgsphere_gc = np.zeros((n_repeat, n_interval))
time_pgsphere_gnp = np.zeros((n_repeat, n_interval))
n_results_pgsphere_gnp = np.zeros((n_repeat, n_interval))

time_direct_gc = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gc = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_gnp = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gnp = np.zeros((n_repeat_direct, n_interval_direct))

# Repeating the queries n_repeat times with the Q3C index
for j in range(n_repeat):
    print "run " + str(j+1) + " of " + str(n_repeat)

    # Loop through the list of radii
    for i, radius in enumerate(radii_q3c):

        # Prepare the PostgreSQL queries
        query_q3c_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_q3c WHERE " +\
            "q3c_radial_query(ra_degree, dec_degree, " + str(ra_gc) + ", " +\
            str(dec_gc) + ", " + str(radius/3600.) + ");"
        query_q3c_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_q3c WHERE " +\
            "q3c_radial_query(ra_degree, dec_degree, " + str(ra_gnp) +\
            ", " + str(dec_gnp) + ", " + str(radius/3600.) + ");"

        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543"
            )

        # Run the queries and save the results in arrays
        n_results_q3c_gc[j][i], time_q3c_gc[j][i] =\
            pq.run_query(conn, query_q3c_gc)
        n_results_q3c_gnp[j][i], time_q3c_gnp[j][i] =\
            pq.run_query(conn, query_q3c_gnp)

        # Print results
        print "(GC) Time elapsed for Q3C search radius " + str(radius) +\
            " arcsec : " + str(time_q3c_gc[j][i]) + ' No. of matches = ' +\
            str(n_results_q3c_gc[j][i])
        print "(GNP) Time elapsed for Q3C search radius " + str(radius) +\
            " arcsec : " + str(time_q3c_gnp[j][i]) + ' No. of matches = ' +\
            str(n_results_q3c_gnp[j][i])

        # Terminate connection to the database
        conn.close()


# Repeating the queries n_repeat times with the pgSphere index
for j in range(n_repeat):
    print "run " + str(j+1) + " of " + str(n_repeat)

    # Loop through the list of radii
    for i, radius in enumerate(radii_pgsphere):

        # Prepare the PostgreSQL queries
        query_pgsphere_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_gc) + "), radians(" +\
            str(dec_gc) + ")), RADIANS(" + str(radius / 3600.) + "))~coords;"
        query_pgsphere_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_gnp) + "), radians(" +\
            str(dec_gnp) + ")), RADIANS(" + str(radius / 3600.) + "))~coords;"

        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543"
            )

        # Run the queries and save the results in arrays
        n_results_pgsphere_gc[j][i], time_pgsphere_gc[j][i] =\
            pq.run_query(conn, query_pgsphere_gc)
        n_results_pgsphere_gnp[j][i], time_pgsphere_gnp[j][i] =\
            pq.run_query(conn, query_pgsphere_gnp)

        # Print results
        print "(GC) Time elapsed for pgSphere search radius " +\
            str(radius) + " arcsec : " + str(time_pgsphere_gc[j][i]) +\
            ' No. of matches = ' + str(n_results_pgsphere_gc[j][i])
        print "(GNP) Time elapsed for pgSphere search radius " +\
            str(radius) + " arcsec : " + str(time_pgsphere_gnp[j][i]) +\
            ' No. of matches = ' + str(n_results_pgsphere_gnp[j][i])

        # Terminate connection to the database
        conn.close()


# Repeating the queries n_repeat times with the pgSphere index
for j in range(n_repeat_direct):
    print "run " + str(j+1) + " of " + str(n_repeat_direct)

    # Loop through the list of radii
    for i, radius in enumerate(radii_direct):

        # Prepare the PostgreSQL queries
        query_direct_gc =\
            "EXPLAIN ANALYSE SELECT * FROM ( SELECT dec_degree, ra_degree," +\
            " vincenty(" + str(dec_gc) + ", " + str(ra_gc) +\
            ", dec_degree, ra_degree) AS distance FROM allkeys)" +\
            " AS d WHERE distance <= " + str(radius/3600.) + ";"
        query_direct_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM ( SELECT dec_degree, ra_degree," +\
            "vincenty(" + str(dec_gnp) + ", " + str(ra_gnp) +\
            ", dec_degree, ra_degree) AS distance FROM allkeys)" +\
            " AS d WHERE distance <= " + str(radius/3600.) + ";"

        # Connect to the database
        conn = psycopg2.connect(
            database="ltarchive",
            user="dbuser",
            password="dbuser",
            host="150.204.240.113",
            port="6543"
            )

        # Run the queries and save the results in arrays
        n_results_direct_gc[j][i], time_direct_gc[j][i] =\
            pq.run_query(conn, query_direct_gc)
        n_results_direct_gnp[j][i], time_direct_gnp[j][i] =\
            pq.run_query(conn, query_direct_gnp)

        # Print results
        print "(GC) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gc[j][i]) +\
            " No. of matches = " + str(n_results_direct_gc[j][i])
        print "(GNP) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gnp[j][i]) +\
            " No. of matches = " + str(n_results_direct_gnp[j][i])

        # Terminate connection to the database
        conn.close()

# Create a log-log plot
fig1 = plt.figure(1)
fig1.clf()
ax1 = fig1.add_subplot(111)
ax2 = ax1.twinx()
# GC
ax1.plot(radii_q3c,
         np.median(time_q3c_gc, axis=0),
         color='C0',
         label='(GC) Q3C')
ax1.plot(radii_pgsphere,
         np.median(time_pgsphere_gc, axis=0),
         color='C1',
         label='(GC) pgSphere')
ax1.plot(radii_direct,
         np.median(time_direct_gc, axis=0),
         color='C2',
         label='(GC) Direct')
# GNP
ax1.plot(radii_q3c,
         np.median(time_q3c_gnp, axis=0),
         color='C0',
         ls=':',
         label='(GNP) Q3C')
ax1.plot(radii_pgsphere,
         np.median(time_pgsphere_gnp, axis=0),
         color='C1',
         ls=':',
         label='(GNP) pgSphere')
ax1.plot(radii_direct,
         np.median(time_direct_gnp, axis=0),
         color='C2',
         ls=':',
         label='(GNP) Direct')
# Number count
ax2.plot(radii_q3c,
         np.median(n_results_q3c_gc, axis=0),
         color='C3',
         label='GC Number count')
ax2.plot(radii_q3c,
         np.median(n_results_q3c_gnp, axis=0),
         color='C4',
         label='GNP Number count')

ax1.grid()
ax1.set_xlim(1, 100000)
ax1.set_ylim(0.00001, 100)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_xlabel('Search radius / arcsec')
ax1.set_ylabel('Time taken / seconds')
ax2.set_ylabel('Number of results')
ax1.legend(loc='upper left')
ax2.legend(loc='center left')
ax1.set_title('PostgreSQL search radius')
plt.savefig(output_path + "psql_Newton_ltarchive_spatial_index_log.png")

# Same as fig1 but in linear scale
fig2 = plt.figure(2)
fig2.clf()
ax3 = fig2.add_subplot(111)
ax4 = ax3.twinx()
ax3.plot(radius_q3c,
         np.median(time_q3c_gc, axis=0),
         color='C0',
         label='(GC) Q3C')
ax3.plot(radii_pgsphere,
         np.median(time_pgsphere_gc, axis=0),
         color='C1',
         label='(GC) pgSphere')
ax3.plot(radii_direct,
         np.median(time_direct_gc, axis=0),
         color='C2',
         label='(GC) Direct')
ax3.plot(radius_q3c_,
         np.median(time_q3c_gnp, axis=0),
         color='C0',
         ls=':',
         label='(GNP) Q3C')
ax3.plot(radii_pgsphere,
         np.median(time_pgsphere_gnp, axis=0),
         color='C1',
         ls=':',
         label='(GNP) pgSphere')
ax3.plot(radii_direct,
         np.median(time_direct_gnp, axis=0),
         color='C2',
         ls=':',
         label='(GNP) Direct')
# Number count
ax4.plot(radii_q3c,
         np.median(n_results_q3c_gc, axis=0),
         color='C3',
         label='GC Number count')
ax4.plot(radii_q3c,
         np.median(n_results_q3c_gnp, axis=0),
         color='C4',
         label='GNP Number count')

ax3.grid()
ax3.set_xlim(0, 110000)
ax3.set_ylim(0, 5)
ax4.set_ylim(0, 300000)
ax3.set_xlabel('Search radius / arcsec')
ax3.set_ylabel('Time taken / seconds')
ax3.set_title('PostgreSQL search radius')
ax4.set_ylabel('Number of results')
ax3.legend(loc='upper left')
ax4.legend(loc='center left')
plt.savefig(output_path + "psql_Newton_ltarchive_spatial_index_linear.png")
