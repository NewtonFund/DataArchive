#!/usr/bin/python

'''
    File name: spatial_timing_ltarchive.py
    Prepared by: MCL
    Date created: 9/8/2017
    Date last modified: 2/11/2017
    Python Version: 2.7

    This script compares the run time of PostgreSQL queries by position,
    3 cases are compared:
    (1) Database with Q3C index
    (2) Database with pgSphere index
    (3) Database without index
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

# Random point 1
ra_random_1 = 78.216622
dec_random_1 = 46.598981

# Random point 2
ra_random_2 = 7.901244
dec_random_2 = 16.016359

# Random point 3
ra_random_3 = 325.298163
dec_random_3 = -3.499611

# Cone search parameters
min_radius = 0.
max_radius = np.log10(30. * 3600.)  # (arcsecs)
n_interval = 100
n_repeat = 10
n_interval_direct = 5
n_repeat_direct = 5

# Set the search radius (degrees)
radii_spatial = 10.**np.linspace(min_radius, max_radius, n_interval)
radii_direct = 10.**np.linspace(min_radius, max_radius, n_interval_direct)

# Create zero arrays for the number of results and execution times
time_q3c_gc = np.zeros((n_repeat, n_interval))
n_results_q3c_gc = np.zeros((n_repeat, n_interval))
time_q3c_gnp = np.zeros((n_repeat, n_interval))
n_results_q3c_gnp = np.zeros((n_repeat, n_interval))
time_q3c_r1 = np.zeros((n_repeat, n_interval))
n_results_q3c_r1 = np.zeros((n_repeat, n_interval))
time_q3c_r2 = np.zeros((n_repeat, n_interval))
n_results_q3c_r2 = np.zeros((n_repeat, n_interval))
time_q3c_r3 = np.zeros((n_repeat, n_interval))
n_results_q3c_r3 = np.zeros((n_repeat, n_interval))

time_pgsphere_gc = np.zeros((n_repeat, n_interval))
n_results_pgsphere_gc = np.zeros((n_repeat, n_interval))
time_pgsphere_gnp = np.zeros((n_repeat, n_interval))
n_results_pgsphere_gnp = np.zeros((n_repeat, n_interval))
time_pgsphere_r1 = np.zeros((n_repeat, n_interval))
n_results_pgsphere_r1 = np.zeros((n_repeat, n_interval))
time_pgsphere_r2 = np.zeros((n_repeat, n_interval))
n_results_pgsphere_r2 = np.zeros((n_repeat, n_interval))
time_pgsphere_r3 = np.zeros((n_repeat, n_interval))
n_results_pgsphere_r3 = np.zeros((n_repeat, n_interval))

time_direct_gc = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gc = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_gnp = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_gnp = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_r1 = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_r1 = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_r2 = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_r2 = np.zeros((n_repeat_direct, n_interval_direct))
time_direct_r3 = np.zeros((n_repeat_direct, n_interval_direct))
n_results_direct_r3 = np.zeros((n_repeat_direct, n_interval_direct))

# Repeating the queries n_repeat times with the Q3C index
for j in range(n_repeat):
    print "run " + str(j+1) + " of " + str(n_repeat)

    # Loop through the list of radii
    for i, radius in enumerate(radii_spatial):

        # Prepare the PostgreSQL queries
        query_q3c_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_q3c WHERE " +\
            "q3c_radial_query(ra_degree, dec_degree, " + str(ra_gc) + ", " +\
            str(dec_gc) + ", " + str(radius/3600.) + ");"
        query_q3c_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_q3c WHERE " +\
            "q3c_radial_query(ra_degree, dec_degree, " + str(ra_gnp) +\
            ", " + str(dec_gnp) + ", " + str(radius/3600.) + ");"
        query_q3c_r1 =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_q3c WHERE " +\
            "q3c_radial_query(ra_degree, dec_degree, " + str(ra_random_1) +\
            ", " + str(dec_random_1) + ", " + str(radius/3600.) + ");"
        query_q3c_r2 =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_q3c WHERE " +\
            "q3c_radial_query(ra_degree, dec_degree, " + str(ra_random_2) +\
            ", " + str(dec_random_2) + ", " + str(radius/3600.) + ");"
        query_q3c_r3 =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_q3c WHERE " +\
            "q3c_radial_query(ra_degree, dec_degree, " + str(ra_random_3) +\
            ", " + str(dec_random_3) + ", " + str(radius/3600.) + ");"

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
        n_results_q3c_r1[j][i], time_q3c_r1[j][i] =\
            pq.run_query(conn, query_q3c_r1)
        n_results_q3c_r2[j][i], time_q3c_r2[j][i] =\
            pq.run_query(conn, query_q3c_r2)
        n_results_q3c_r3[j][i], time_q3c_r3[j][i] =\
            pq.run_query(conn, query_q3c_r3)

        # Print results
        print "(GC) Time elapsed for Q3C search radius " + str(radius) +\
            " arcsec : " + str(time_q3c_gc[j][i]) + ' No. of matches = ' +\
            str(n_results_q3c_gc[j][i])
        print "(GNP) Time elapsed for Q3C search radius " + str(radius) +\
            " arcsec : " + str(time_q3c_gnp[j][i]) + ' No. of matches = ' +\
            str(n_results_q3c_gnp[j][i])
        print "(Random 1) Time elapsed for Q3C search radius " + str(radius) +\
            " arcsec : " + str(time_q3c_r1[j][i]) + ' No. of matches = ' +\
            str(n_results_q3c_r1[j][i])
        print "(Random 2) Time elapsed for Q3C search radius " + str(radius) +\
            " arcsec : " + str(time_q3c_r2[j][i]) + ' No. of matches = ' +\
            str(n_results_q3c_r2[j][i])
        print "(Random 3) Time elapsed for Q3C search radius " + str(radius) +\
            " arcsec : " + str(time_q3c_r3[j][i]) + ' No. of matches = ' +\
            str(n_results_q3c_r3[j][i])

        # Terminate connection to the database
        conn.close()

# Repeating the queries n_repeat times with the pgSphere index
for j in range(n_repeat):
    print "run " + str(j+1) + " of " + str(n_repeat)

    # Loop through the list of radii
    for i, radius in enumerate(radii_spatial):

        # Prepare the PostgreSQL queries
        query_pgsphere_gc =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_gc) + "), radians(" +\
            str(dec_gc) + ")), RADIANS(" + str(radius / 3600.) + "))~coords;"
        query_pgsphere_gnp =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_gnp) + "), radians(" +\
            str(dec_gnp) + ")), RADIANS(" + str(radius / 3600.) + "))~coords;"
        query_pgsphere_r1 =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_random_1) + "), radians(" +\
            str(dec_random_1) + ")), RADIANS(" + str(radius / 3600.) +\
            "))~coords;"
        query_pgsphere_r2 =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_random_2) + "), radians(" +\
            str(dec_random_2) + ")), RADIANS(" + str(radius / 3600.) +\
            "))~coords;"
        query_pgsphere_r3 =\
            "EXPLAIN ANALYSE SELECT * FROM allkeys_pgsphere WHERE " +\
            "scircle(spoint(radians(" + str(ra_random_3) + "), radians(" +\
            str(dec_random_3) + ")), RADIANS(" + str(radius / 3600.) +\
            "))~coords;"

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
        n_results_pgsphere_r1[j][i], time_pgsphere_r1[j][i] =\
            pq.run_query(conn, query_pgsphere_r1)
        n_results_pgsphere_r2[j][i], time_pgsphere_r2[j][i] =\
            pq.run_query(conn, query_pgsphere_r2)
        n_results_pgsphere_r3[j][i], time_pgsphere_r3[j][i] =\
            pq.run_query(conn, query_pgsphere_r3)

        # Print results
        print "(GC) Time elapsed for pgSphere search radius " +\
            str(radius) + " arcsec : " + str(time_pgsphere_gc[j][i]) +\
            ' No. of matches = ' + str(n_results_pgsphere_gc[j][i])
        print "(GNP) Time elapsed for pgSphere search radius " +\
            str(radius) + " arcsec : " + str(time_pgsphere_gnp[j][i]) +\
            ' No. of matches = ' + str(n_results_pgsphere_gnp[j][i])
        print "(Random 1) Time elapsed for pgSphere search radius " +\
            str(radius) + " arcsec : " + str(time_pgsphere_r1[j][i]) +\
            ' No. of matches = ' + str(n_results_pgsphere_r1[j][i])
        print "(Random 2) Time elapsed for pgSphere search radius " +\
            str(radius) + " arcsec : " + str(time_pgsphere_r2[j][i]) +\
            ' No. of matches = ' + str(n_results_pgsphere_r2[j][i])
        print "(Random 3) Time elapsed for pgSphere search radius " +\
            str(radius) + " arcsec : " + str(time_pgsphere_r3[j][i]) +\
            ' No. of matches = ' + str(n_results_pgsphere_r3[j][i])

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
        query_direct_r1 =\
            "EXPLAIN ANALYSE SELECT * FROM ( SELECT dec_degree, ra_degree," +\
            "vincenty(" + str(dec_random_1) + ", " + str(ra_random_1) +\
            ", dec_degree, ra_degree) AS distance FROM allkeys)" +\
            " AS d WHERE distance <= " + str(radius/3600.) + ";"
        query_direct_r2 =\
            "EXPLAIN ANALYSE SELECT * FROM ( SELECT dec_degree, ra_degree," +\
            "vincenty(" + str(dec_random_2) + ", " + str(ra_random_2) +\
            ", dec_degree, ra_degree) AS distance FROM allkeys)" +\
            " AS d WHERE distance <= " + str(radius/3600.) + ";"
        query_direct_r3 =\
            "EXPLAIN ANALYSE SELECT * FROM ( SELECT dec_degree, ra_degree," +\
            "vincenty(" + str(dec_random_3) + ", " + str(ra_random_3) +\
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
        n_results_direct_r1[j][i], time_direct_r1[j][i] =\
            pq.run_query(conn, query_direct_r1)
        n_results_direct_r2[j][i], time_direct_r2[j][i] =\
            pq.run_query(conn, query_direct_r2)
        n_results_direct_r3[j][i], time_direct_r3[j][i] =\
            pq.run_query(conn, query_direct_r3)

        # Print results
        print "(GC) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gc[j][i]) +\
            " No. of matches = " + str(n_results_direct_gc[j][i])
        print "(GNP) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_gnp[j][i]) +\
            " No. of matches = " + str(n_results_direct_gnp[j][i])
        print "(Random 1) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_r1[j][i]) +\
            " No. of matches = " + str(n_results_direct_r1[j][i])
        print "(Random 2) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_r2[j][i]) +\
            " No. of matches = " + str(n_results_direct_r2[j][i])
        print "(Random 3) Time elapsed for search radius " + str(radius) +\
            " arcsec : " + str(time_direct_r3[j][i]) +\
            " No. of matches = " + str(n_results_direct_r3[j][i])

        # Terminate connection to the database
        conn.close()

# Create a log-log plot
fig1 = plt.figure(1, figsize=(8,8))
fig1.clf()
ax1 = fig1.add_subplot(111)
ax2 = ax1.twinx()
# GC
ax1.plot(radii_spatial,
         np.median(time_q3c_gc, axis=0),
         color='C0',
         label='(GC) Q3C')
ax1.plot(radii_spatial,
         np.median(time_pgsphere_gc, axis=0),
         color='C1',
         label='(GC) pgSphere')
ax1.plot(radii_direct,
         np.median(time_direct_gc, axis=0),
         color='C2',
         label='(GC) Direct')
# GNP
ax1.plot(radii_spatial,
         np.median(time_q3c_gnp, axis=0),
         color='C0',
         ls=':',
         label='(GNP) Q3C')
ax1.plot(radii_spatial,
         np.median(time_pgsphere_gnp, axis=0),
         color='C1',
         ls=':',
         label='(GNP) pgSphere')
ax1.plot(radii_direct,
         np.median(time_direct_gnp, axis=0),
         color='C2',
         ls=':',
         label='(GNP) Direct')
# Random 1
ax1.plot(radii_spatial,
         np.median(time_pgsphere_r1, axis=0),
         color='C0',
         ls='-.',
         label='(R1) Q3C')
ax1.plot(radii_spatial,
         np.median(time_q3c_r1, axis=0),
         color='C1',
         ls='-.',
         label='(R1) pgSphere')
ax1.plot(radii_direct,
         np.median(time_direct_r1, axis=0),
         color='C2',
         ls='-.',
         label='(R1) Direct')
# Random 2
ax1.plot(radii_spatial,
         np.median(time_q3c_r2, axis=0),
         color='C0',
         ls='--',
         label='(R2) Q3C')
ax1.plot(radii_spatial,
         np.median(time_pgsphere_r2, axis=0),
         color='C1',
         ls='--',
         label='(R2) pgSphere')
ax1.plot(radii_direct,
         np.median(time_direct_r2, axis=0),
         color='C2',
         ls='--',
         label='(R2) Direct')
# Random 3
ax1.plot(radii_spatial,
         np.median(time_q3c_r3, axis=0),
         color='C0',
         ls='-',
         lw=3,
         label='(R3) Q3C')
ax1.plot(radii_spatial,
         np.median(time_pgsphere_r3, axis=0),
         color='C1',
         ls='-',
         lw=3,
         label='(R3) pgSphere')
ax1.plot(radii_direct,
         np.median(time_direct_r3, axis=0),
         color='C2',
         ls='-',
         lw=3,
         label='(R3) Direct')


'''# Number count
ax2.plot(radii_spatial,
         np.median(n_results_q3c_gc, axis=0),
         color='C5',
         label='GC Number count')
ax2.plot(radii_spatial,
         np.median(n_results_q3c_gnp, axis=0),
         color='C6',
         label='GNP Number count')
ax2.plot(radii_spatial,
         np.median(n_results_q3c_r1, axis=0),
         color='C7',
         label='R1 Number count')
ax2.plot(radii_spatial,
         np.median(n_results_q3c_r2, axis=0),
         color='C8',
         label='R2 Number count')
ax2.plot(radii_spatial,
         np.median(n_results_q3c_r3, axis=0),
         color='C9',
         label='R3 Number count')
'''
ax1.grid()
ax1.set_xlim(1, 100000)
ax1.set_ylim(0.0001, 100)
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
fig2 = plt.figure(2, figsize=(8,8))
fig2.clf()
ax3 = fig2.add_subplot(111)
ax4 = ax3.twinx()

# GC
ax3.plot(radius_spatial,
         np.median(time_q3c_gc, axis=0),
         color='C0',
         label='(GC) Q3C')
ax3.plot(radii_spatial,
         np.median(time_pgsphere_gc, axis=0),
         color='C1',
         label='(GC) pgSphere')
ax3.plot(radii_direct,
         np.median(time_direct_gc, axis=0),
         color='C2',
         label='(GC) Direct')

# GNP
ax3.plot(radii_spatial,
         np.median(time_q3c_gnp, axis=0),
         color='C0',
         ls=':',
         label='(GNP) Q3C')
ax3.plot(radii_spatial,
         np.median(time_pgsphere_gnp, axis=0),
         color='C1',
         ls=':',
         label='(GNP) pgSphere')
ax3.plot(radii_direct,
         np.median(time_direct_gnp, axis=0),
         color='C2',
         ls=':',
         label='(GNP) Direct')

# Random 1
ax3.plot(radii_spatial,
         np.median(time_q3c_r1, axis=0),
         color='C0',
         ls='-.',
         label='(R1) Q3C')
ax3.plot(radii_spatial,
         np.median(time_pgsphere_r1, axis=0),
         color='C1',
         ls='-.',
         label='(R1) pgSphere')
ax3.plot(radii_direct,
         np.median(time_direct_r1, axis=0),
         color='C2',
         ls='-.',
         label='(R1) Direct')

# Random 2
ax3.plot(radii_spatial,
         np.median(time_q3c_r2, axis=0),
         color='C0',
         ls='--',
         label='(R2) Q3C')
ax3.plot(radii_spatial,
         np.median(time_pgsphere_r2, axis=0),
         color='C1',
         ls='--',
         label='(R2) pgSphere')
ax3.plot(radii_direct,
         np.median(time_direct_r2, axis=0),
         color='C2',
         ls='--',
         label='(R3) Direct')

# Random 3
ax3.plot(radii_spatial,
         np.median(time_q3c_r3, axis=0),
         color='C0',
         ls='-',
         lw=3,
         label='(R3) Q3C')
ax3.plot(radii_spatial,
         np.median(time_pgsphere_r3, axis=0),
         color='C1',
         ls='-',
         lw=3,
         label='(R3) pgSphere')
ax3.plot(radii_direct,
         np.median(time_direct_r3, axis=0),
         color='C2',
         ls='-',
         lw=3,
         label='(R3) Direct')

'''# Number count
ax4.plot(radii_spatial,
         np.median(n_results_q3c_gc, axis=0),
         color='C3',
         label='GC Number count')
ax4.plot(radii_spatial,
         np.median(n_results_q3c_gnp, axis=0),
         color='C4',
         label='GNP Number count')
ax4.plot(radii_spatial,
         np.median(n_results_q3c_r1, axis=0),
         color='C5',
         label='R1 Number count')
ax4.plot(radii_spatial,
         np.median(n_results_q3c_r2, axis=0),
         color='C6',
         label='R2 Number count')
ax4.plot(radii_spatial,
         np.median(n_results_q3c_r3, axis=0),
         color='C7',
         label='R3 Number count')
'''
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
