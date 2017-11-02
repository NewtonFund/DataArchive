#!/usr/bin/python

'''
    File name: spatial_timing_gaia.py
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
import time
import numpy as np
import psycopg2  
from matplotlib.pyplot import *
ion()

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

search_radius_q3c_gc = 10.**np.arange(0.,5.8,0.01)
time_required_q3c_gc = []
number_results_q3c_gc = []
time_required_q3c_gnp = []
number_results_q3c_gnp = []
for radius in search_radius_q3c_gc:
    query_gc = "EXPLAIN ANALYSE SELECT * FROM tgas_q3c WHERE q3c_radial_query(ra, declination, " + str(ra_gc) + ", " + str(dec_gc) + ", " + str(radius/3600.) + ");"
    query_gnp = "EXPLAIN ANALYSE SELECT * FROM tgas_q3c WHERE q3c_radial_query(ra, declination, " + str(ra_gnp) + ", " + str(dec_gnp) + ", " + str(radius/3600.) + ");"
    conn = psycopg2.connect(database="gaia", user="dbuser", password="dbuser", host="150.204.240.113", port="6543")  
    cur = conn.cursor()
    cur.execute(query_gc)
    temp = cur.fetchall()
    number_results_q3c_gc.append(int((temp[0][0].split(' ')[-2]).split('=')[-1]))
    time_required_q3c_gc.append(float(temp[-1][0].split(' ')[-2])/1000.)
    temp = None
    cur.close()
    cur = None
    cur = conn.cursor()
    cur.execute(query_gnp)
    temp = cur.fetchall()
    number_results_q3c_gnp.append(int((temp[0][0].split(' ')[-2]).split('=')[-1]))
    time_required_q3c_gnp.append(float(temp[-1][0].split(' ')[-2])/1000.)
    temp = None
    cur.close()
    cur = None
    print "(GC) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_q3c_gc[-1]) + ' No. of matches = ' + str(number_results_q3c_gc[-1])
    print "(GNP) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_q3c_gnp[-1]) + ' No. of matches = ' + str(number_results_q3c_gnp[-1])
    conn.close()


search_radius_pgsphere_gc = 10.**np.arange(0.,5.8,0.01)
time_required_pgsphere_gc = []
number_results_pgsphere_gc = []
time_required_pgsphere_gnp = []
number_results_pgsphere_gnp = []
for radius in search_radius_pgsphere_gc:
    query_gc = "EXPLAIN ANALYSE SELECT * FROM tgas_pgsphere WHERE scircle(spoint(radians("+str(ra_gc)+"), radians("+str(dec_gc)+")), RADIANS(" + str(radius/3600.) + "))~coords;"
    query_gnp = "EXPLAIN ANALYSE SELECT * FROM tgas_pgsphere WHERE scircle(spoint(radians("+str(ra_gnp)+"), radians("+str(dec_gnp)+")), RADIANS(" + str(radius/3600.) + "))~coords;"
    conn = psycopg2.connect(database="gaia", user="dbuser", password="dbuser", host="150.204.240.113", port="6543")  
    cur = conn.cursor()
    cur.execute(query_gc)
    temp = cur.fetchall()
    number_results_pgsphere_gc.append(int((temp[0][0].split(' ')[-2]).split('=')[-1]))
    time_required_pgsphere_gc.append(float(temp[-1][0].split(' ')[-2])/1000.)
    temp = None
    cur.close()
    cur = None
    cur = conn.cursor()
    cur.execute(query_gnp)
    temp = cur.fetchall()
    number_results_pgsphere_gnp.append(int((temp[0][0].split(' ')[-2]).split('=')[-1]))
    time_required_pgsphere_gnp.append(float(temp[-1][0].split(' ')[-2])/1000.)
    temp = None
    cur.close()
    cur = None
    print "(GC) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_pgsphere_gc[-1]) + ' No. of matches = ' + str(number_results_pgsphere_gc[-1])
    print "(GNP) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_pgsphere_gnp[-1]) + ' No. of matches = ' + str(number_results_pgsphere_gnp[-1])
    conn.close()



search_radius_direct_gc = 10.**np.linspace(0.,5.8,10)
time_required_direct_gc = []
number_results_direct_gc = []
time_required_direct_gnp = []
number_results_direct_gnp = []
for radius in search_radius_direct_gc:
    query_gc = ("EXPLAIN ANALYSE SELECT * FROM ( SELECT declination, ra, vincenty(" + str(dec_gc) + ", " + str(ra_gc) + ", declination, ra) AS distance FROM tgas ) as d WHERE distance <= " + str(radius/3600.) + ";")
    query_gnp = ("EXPLAIN ANALYSE SELECT * FROM ( SELECT declination, ra, vincenty(" + str(dec_gnp) + ", " + str(ra_gnp) + ", declination, ra) AS distance FROM tgas ) as d WHERE distance <= " + str(radius/3600.) + ";")
    conn = psycopg2.connect(database="gaia", user="dbuser", password="dbuser", host="150.204.240.113", port="6543")  
    cur = conn.cursor()
    cur.execute(query_gc)
    temp = cur.fetchall()
    number_results_direct_gc.append(int((temp[0][0].split(' ')[-2]).split('=')[-1]))
    time_required_direct_gc.append(float(temp[-1][0].split(' ')[-2])/1000.)
    temp = None
    cur.close()
    cur = None
    cur = conn.cursor()
    cur.execute(query_gnp)
    temp = cur.fetchall()
    number_results_direct_gnp.append(int((temp[0][0].split(' ')[-2]).split('=')[-1]))
    time_required_direct_gnp.append(float(temp[-1][0].split(' ')[-2])/1000.)
    temp = None
    cur.close()
    cur = None
    print "(GC) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_direct_gc[-1]) + ' No. of matches = ' + str(number_results_direct_gc[-1])
    print "(GNP) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_direct_gnp[-1]) + ' No. of matches = ' + str(number_results_direct_gnp[-1])
    conn.close()


time_required_q3c_gc = np.array(time_required_q3c_gc)
time_required_pgsphere_gc = np.array(time_required_pgsphere_gc)
time_required_direct_gc = np.array(time_required_direct_gc)

time_required_q3c_gnp = np.array(time_required_q3c_gnp)
time_required_pgsphere_gnp = np.array(time_required_pgsphere_gnp)
time_required_direct_gnp = np.array(time_required_direct_gnp)

number_results_q3c_gc = np.array(number_results_q3c_gc)
number_results_pgsphere_gc = np.array(number_results_pgsphere_gc)
number_results_direct_gc = np.array(number_results_direct_gc)

number_results_q3c_gnp = np.array(number_results_q3c_gnp)
number_results_pgsphere_gnp = np.array(number_results_pgsphere_gnp)
number_results_direct_gnp = np.array(number_results_direct_gnp)

figure(1)
clf()
plot(search_radius_q3c_gc[:len(time_required_q3c_gc)],time_required_q3c_gc, color='C0', label='(GC) Q3C')
plot(search_radius_pgsphere_gc[:len(time_required_pgsphere_gc)],time_required_pgsphere_gc, color='C1', label='(GC) pgSphere')
plot(search_radius_direct_gc[:len(time_required_direct_gc)],time_required_direct_gc, color='C2', label='(GC) Direct')

plot(search_radius_q3c_gc[:len(time_required_q3c_gnp)],time_required_q3c_gnp, color='C0', ls=':', label='(GNP) Q3C')
plot(search_radius_pgsphere_gc[:len(time_required_pgsphere_gnp)],time_required_pgsphere_gnp, color='C1', ls=':', label='(GNP) pgSphere')
plot(search_radius_direct_gc[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C2', ls=':', label='(GNP) Direct')

grid()
xlim(1,500000)
ylim(0.00001,100)
xscale('log')
yscale('log')
xlabel('Search radius / arcsec')
ylabel('Time taken / seconds')
legend(loc='upper left')
title('PostgreSQL search radius')
savefig(output_path + 'psql_Newton_indexing_timing_1.png')

figure(2)
clf()
plot(search_radius_q3c_gc[:len(time_required_q3c_gc)],time_required_q3c_gc, color='C0', label='(GC) Q3C')
plot(search_radius_pgsphere_gc[:len(time_required_pgsphere_gc)],time_required_pgsphere_gc, color='C1', label='(GC) pgSphere')
plot(search_radius_direct_gc[:len(time_required_direct_gc)],time_required_direct_gc, color='C2', label='(GC) Direct')

plot(search_radius_q3c_gc[:len(time_required_q3c_gnp)],time_required_q3c_gnp, color='C0', ls=':', label='(GNP) Q3C')
plot(search_radius_pgsphere_gc[:len(time_required_pgsphere_gnp)],time_required_pgsphere_gnp, color='C1', ls=':', label='(GNP) pgSphere')
plot(search_radius_direct_gc[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C2', ls=':', label='(GNP) Direct')

grid()
xlim(5000,350000)
ylim(0,50)
xlabel('Search radius / arcsec')
ylabel('Time taken / seconds')
title('PostgreSQL search radius')
legend(loc='upper left')
savefig(output_path + 'psql_Newton_indexing_timing_1_zoomed_in.png')




figure(3)
clf()
plot(number_results_q3c_gc[:len(time_required_q3c_gc)],time_required_q3c_gc, color='C0', label='(GC) Q3C')
plot(number_results_pgsphere_gc[:len(time_required_pgsphere_gc)],time_required_pgsphere_gc, color='C1', label='(GC) pgSphere')
plot(number_results_direct_gc[:len(time_required_direct_gc)],time_required_direct_gc, color='C2', label='(GC) Direct')

plot(number_results_q3c_gnp[:len(time_required_q3c_gnp)],time_required_q3c_gnp, color='C0', ls=':', label='(GNP) Q3C')
plot(number_results_pgsphere_gnp[:len(time_required_pgsphere_gnp)],time_required_pgsphere_gnp, color='C1', ls=':', label='(GNP) pgSphere')
plot(number_results_direct_gnp[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C2', ls=':', label='(GNP) Direct')

grid()
xlim(1,1100000)
ylim(0.00001,100)
xscale('log')
yscale('log')
xlabel('Number of mathces')
ylabel('Time taken / seconds')
title('PostgreSQL number of matches')
legend(loc='upper left')
savefig(output_path + 'psql_Newton_indexing_timing_2.png')


figure(4)
clf()
plot(number_results_q3c_gc[:len(time_required_q3c_gc)],time_required_q3c_gc, color='C0', label='(GC) Q3C')
plot(number_results_pgsphere_gc[:len(time_required_pgsphere_gc)],time_required_pgsphere_gc, color='C1', label='(GC) pgSphere')
plot(number_results_direct_gc[:len(time_required_direct_gc)],time_required_direct_gc, color='C2', label='(GC) Direct')

plot(number_results_q3c_gnp[:len(time_required_q3c_gnp)],time_required_q3c_gnp, color='C0', ls=':', label='(GNP) Q3C')
plot(number_results_pgsphere_gnp[:len(time_required_pgsphere_gnp)],time_required_pgsphere_gnp, color='C1', ls=':', label='(GNP) pgSphere')
plot(number_results_direct_gnp[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C2', ls=':', label='(GNP) Direct')

grid()
xlim(1,1100000)
ylim(0,50)
xlabel('Number of mathces')
ylabel('Time taken / seconds')
title('PostgreSQL number of matches')
legend(loc='upper left')
savefig(output_path + 'psql_Newton_indexing_timing_2_zoomed_in.png')

