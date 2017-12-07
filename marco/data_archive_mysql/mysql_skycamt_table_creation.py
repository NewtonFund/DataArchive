import os
import inspect
import time
import numpy as np
import mysql.connector
from matplotlib.pyplot import *
import gc
ion()

# Get output path if provided, default at ~/Desktop
try:
    output_path = argv[1]
except:
    filename = inspect.getframeinfo(inspect.currentframe()).filename
    output_path = os.path.dirname(os.path.abspath(filename)) + '/output/'

ra_gc = 266.41683
dec_gc = -29.00781

ra_gnp = 192.85951
dec_gnp = 27.12834

search_radius_dif = 10.**np.arange(0.,5.51,0.01)
time_required_dif_htm_6_gc = []
number_results_dif_htm_6_gc = []
time_required_dif_htm_6_gnp = []
number_results_dif_htm_6_gnp = []
time_required_dif_healp_nest_6_gc = []
number_results_dif_healp_nest_6_gc = []
time_required_dif_healp_nest_6_gnp = []
number_results_dif_healp_nest_6_gnp = []
time_required_dif_htm_8_gc = []
number_results_dif_htm_8_gc = []
time_required_dif_htm_8_gnp = []
number_results_dif_htm_8_gnp = []
time_required_dif_healp_nest_8_gc = []
number_results_dif_healp_nest_8_gc = []
time_required_dif_healp_nest_8_gnp = []
number_results_dif_healp_nest_8_gnp = []
time_required_dif_htm_10_gc = []
number_results_dif_htm_10_gc = []
time_required_dif_htm_10_gnp = []
number_results_dif_htm_10_gnp = []
time_required_dif_healp_nest_10_gc = []
number_results_dif_healp_nest_10_gc = []
time_required_dif_healp_nest_10_gnp = []
number_results_dif_healp_nest_10_gnp = []

conn = mysql.connector.connect(user='root', password='@rin@rit', host="150.204.241.218", port="3306", database='gaia')

for radius in search_radius_dif:
    query_htm_6_gc = ("SELECT count(*) FROM gaia.tgas_htm_6 WHERE DIF_Circle(" + str(ra_gc) + ", " + str(dec_gc) + ", " + str(radius/60.) + ") ;")
    query_htm_6_gnp = ("SELECT count(*) FROM gaia.tgas_htm_6 WHERE DIF_Circle(" + str(ra_gnp) + ", " + str(dec_gnp) + ", " + str(radius/60.) + ") ;")
    query_htm_8_gc = ("SELECT count(*) FROM gaia.tgas_htm_8 WHERE DIF_Circle(" + str(ra_gc) + ", " + str(dec_gc) + ", " + str(radius/60.) + ") ;")
    query_htm_8_gnp = ("SELECT count(*) FROM gaia.tgas_htm_8 WHERE DIF_Circle(" + str(ra_gnp) + ", " + str(dec_gnp) + ", " + str(radius/60.) + ") ;")
    query_htm_10_gc = ("SELECT count(*) FROM gaia.tgas_htm_10 WHERE DIF_Circle(" + str(ra_gc) + ", " + str(dec_gc) + ", " + str(radius/60.) + ") ;")
    query_htm_10_gnp = ("SELECT count(*) FROM gaia.tgas_htm_10 WHERE DIF_Circle(" + str(ra_gnp) + ", " + str(dec_gnp) + ", " + str(radius/60.) + ") ;")
    query_healp_nest_6_gc = ("SELECT count(*) FROM gaia.tgas_healp_nest_6 WHERE DIF_Circle(" + str(ra_gc) + ", " + str(dec_gc) + ", " + str(radius/60.) + ") ;")
    query_healp_nest_6_gnp = ("SELECT count(*) FROM gaia.tgas_healp_nest_6 WHERE DIF_Circle(" + str(ra_gnp) + ", " + str(dec_gnp) + ", " + str(radius/60.) + ") ;")
    query_healp_nest_8_gc = ("SELECT count(*) FROM gaia.tgas_healp_nest_8 WHERE DIF_Circle(" + str(ra_gc) + ", " + str(dec_gc) + ", " + str(radius/60.) + ") ;")
    query_healp_nest_8_gnp = ("SELECT count(*) FROM gaia.tgas_healp_nest_8 WHERE DIF_Circle(" + str(ra_gnp) + ", " + str(dec_gnp) + ", " + str(radius/60.) + ") ;")
    query_healp_nest_10_gc = ("SELECT count(*) FROM gaia.tgas_healp_nest_10 WHERE DIF_Circle(" + str(ra_gc) + ", " + str(dec_gc) + ", " + str(radius/60.) + ") ;")
    query_healp_nest_10_gnp = ("SELECT count(*) FROM gaia.tgas_healp_nest_10 WHERE DIF_Circle(" + str(ra_gnp) + ", " + str(dec_gnp) + ", " + str(radius/60.) + ") ;")
    conn = mysql.connector.connect(user='root', password='@rin@rit', host="150.204.241.218", port="3306", database='gaia')
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_htm_6_gc)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_htm_6_gc.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_htm_6_gc.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_htm_6_gnp)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_htm_6_gnp.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_htm_6_gnp.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_htm_8_gc)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_htm_8_gc.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_htm_8_gc.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_htm_8_gnp)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_htm_8_gnp.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_htm_8_gnp.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_htm_10_gc)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_htm_10_gc.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_htm_10_gc.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_htm_10_gnp)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_htm_10_gnp.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_htm_10_gnp.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_healp_nest_6_gc)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_healp_nest_6_gc.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_healp_nest_6_gc.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_healp_nest_6_gnp)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_healp_nest_6_gnp.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_healp_nest_6_gnp.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_healp_nest_8_gc)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_healp_nest_8_gc.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_healp_nest_8_gc.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_healp_nest_8_gnp)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_healp_nest_8_gnp.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_healp_nest_8_gnp.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_healp_nest_10_gc)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_healp_nest_10_gc.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_healp_nest_10_gc.append(time2-time1)
    cur = conn.cursor()
    time1 = time.time()
    cur.execute(query_healp_nest_10_gnp)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_dif_healp_nest_10_gnp.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_dif_healp_nest_10_gnp.append(time2-time1)
    print "(GC htm6) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_htm_6_gc[-1]) + ' No. of matches = ' + str(number_results_dif_htm_6_gc[-1])
    print "(GNP htm6) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_htm_6_gnp[-1]) + ' No. of matches = ' + str(number_results_dif_htm_6_gnp[-1])
    print "(GC htm8) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_htm_8_gc[-1]) + ' No. of matches = ' + str(number_results_dif_htm_8_gc[-1])
    print "(GNP htm8) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_htm_8_gnp[-1]) + ' No. of matches = ' + str(number_results_dif_htm_8_gnp[-1])
    print "(GC htm10) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_htm_10_gc[-1]) + ' No. of matches = ' + str(number_results_dif_htm_10_gc[-1])
    print "(GNP htm10) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_htm_10_gnp[-1]) + ' No. of matches = ' + str(number_results_dif_htm_10_gnp[-1])
    print "(GC healp6) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_healp_nest_6_gc[-1]) + ' No. of matches = ' + str(number_results_dif_healp_nest_6_gc[-1])
    print "(GNP healp6) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_healp_nest_6_gnp[-1]) + ' No. of matches = ' + str(number_results_dif_healp_nest_6_gnp[-1])
    print "(GC healp8) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_healp_nest_8_gc[-1]) + ' No. of matches = ' + str(number_results_dif_healp_nest_8_gc[-1])
    print "(GNP healp8) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_healp_nest_8_gnp[-1]) + ' No. of matches = ' + str(number_results_dif_healp_nest_8_gnp[-1])
    print "(GC healp10) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_healp_nest_10_gc[-1]) + ' No. of matches = ' + str(number_results_dif_healp_nest_10_gc[-1])
    print "(GNP healp10) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_dif_healp_nest_10_gnp[-1]) + ' No. of matches = ' + str(number_results_dif_healp_nest_10_gnp[-1])


conn.close()
conn = None
gc.collect()

time_required_dif_htm_6_gc = np.array(time_required_dif_htm_6_gc)
time_required_dif_htm_8_gc = np.array(time_required_dif_htm_8_gc)
time_required_dif_htm_10_gc = np.array(time_required_dif_htm_10_gc)
time_required_dif_htm_6_gnp = np.array(time_required_dif_htm_6_gnp)
time_required_dif_htm_8_gnp = np.array(time_required_dif_htm_8_gnp)
time_required_dif_htm_10_gnp = np.array(time_required_dif_htm_10_gnp)
time_required_dif_healp_nest_6_gc = np.array(time_required_dif_healp_nest_6_gc)
time_required_dif_healp_nest_8_gc = np.array(time_required_dif_healp_nest_8_gc)
time_required_dif_healp_nest_10_gc = np.array(time_required_dif_healp_nest_10_gc)
time_required_dif_healp_nest_6_gnp = np.array(time_required_dif_healp_nest_6_gnp)
time_required_dif_healp_nest_8_gnp = np.array(time_required_dif_healp_nest_8_gnp)
time_required_dif_healp_nest_10_gnp = np.array(time_required_dif_healp_nest_10_gnp)

number_results_dif_htm_6_gc = np.array(number_results_dif_htm_6_gc)
number_results_dif_htm_8_gc = np.array(number_results_dif_htm_8_gc)
number_results_dif_htm_10_gc = np.array(number_results_dif_htm_10_gc)
number_results_dif_htm_6_gnp = np.array(number_results_dif_htm_6_gnp)
number_results_dif_htm_8_gnp = np.array(number_results_dif_htm_8_gnp)
number_results_dif_htm_10_gnp = np.array(number_results_dif_htm_10_gnp)
number_results_dif_healp_nest_6_gc = np.array(number_results_dif_healp_nest_6_gc)
number_results_dif_healp_nest_8_gc = np.array(number_results_dif_healp_nest_8_gc)
number_results_dif_healp_nest_10_gc = np.array(number_results_dif_healp_nest_10_gc)
number_results_dif_healp_nest_6_gnp = np.array(number_results_dif_healp_nest_6_gnp)
number_results_dif_healp_nest_8_gnp = np.array(number_results_dif_healp_nest_8_gnp)
number_results_dif_healp_nest_10_gnp = np.array(number_results_dif_healp_nest_10_gnp)

search_radius_direct = 10.**np.linspace(0.,5.51,20.)
time_required_direct_gc = []
number_results_direct_gc = []
time_required_direct_gnp = []
number_results_direct_gnp = []

conn = mysql.connector.connect(user='root', password='@rin@rit', host="150.204.241.218", port="3306", database='gaia')

for radius in search_radius_direct:
    cur = conn.cursor()
    query_gc = ("SELECT count(*) FROM ( SELECT declination, ra, vincenty(" + str(dec_gc) + ", " + str(ra_gc) + ", declination, ra) AS distance FROM gaia.tgas ) as d WHERE distance <= " + str(radius/3600.) + " ;")
    time1 = time.time()
    cur.execute(query_gc)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_direct_gc.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_direct_gc.append(time2-time1)
    cur = conn.cursor()
    query_gnp = ("SELECT count(*) FROM ( SELECT declination, ra, vincenty(" + str(dec_gnp) + ", " + str(ra_gnp) + ", declination, ra) AS distance FROM gaia.tgas ) as d WHERE distance <= " + str(radius/3600.) + " ;")
    time1 = time.time()
    cur.execute(query_gnp)
    time2 = time.time()
    temp = cur.fetchall()[0][0]
    number_results_direct_gnp.append(temp)
    temp = None
    cur.close()
    cur = None
    time_required_direct_gnp.append(time2-time1)
    print "(GC) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_direct_gc[-1]) + ' No. of matches = ' + str(number_results_direct_gc[-1])
    print "(GNP) Time elapsed for search radius " + str(radius) + " arcsec : " + str(time_required_direct_gnp[-1]) + ' No. of matches = ' + str(number_results_direct_gnp[-1])


conn.close()
conn = None

time_required_direct_gc = np.array(time_required_direct_gc)
time_required_direct_gnp = np.array(time_required_direct_gnp)


figure(1)
clf()
plot(search_radius_dif[:len(time_required_dif_htm_6_gc)],time_required_dif_htm_6_gc, color='C0', label='(GC) HTM depth = 6')
plot(search_radius_dif[:len(time_required_dif_htm_8_gc)],time_required_dif_htm_8_gc, color='C1', label='(GC) HTM depth = 8')
plot(search_radius_dif[:len(time_required_dif_htm_10_gc)],time_required_dif_htm_10_gc, color='C2', label='(GC) HTM depth = 10')
plot(search_radius_dif[:len(time_required_dif_htm_6_gnp)],time_required_dif_htm_6_gnp, color='C0', ls=':', label='(GNP) HTM depth 6')
plot(search_radius_dif[:len(time_required_dif_htm_8_gnp)],time_required_dif_htm_8_gnp, color='C1', ls=':', label='(GNP) HTM depth 8')
plot(search_radius_dif[:len(time_required_dif_htm_10_gnp)],time_required_dif_htm_10_gnp, color='C2', ls=':', label='(GNP) HTM depth 10')
plot(search_radius_direct[:len(time_required_direct_gc)],time_required_direct_gc, color='C3', label='(GC) Direct query')
plot(search_radius_direct[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C3', ls=':', label='(GNP) Direct query')

grid()
xlim(1,500000)
ylim(0.001,500)
xscale('log')
yscale('log')
xlabel('Search radius / arcsec')
ylabel('Time taken / seconds')
title('MySQL search radius (HTM)')
legend()
savefig(output_path + 'mysql_htm_timing.png')


figure(2)
plot(search_radius_dif[:len(time_required_dif_healp_nest_6_gc)],time_required_dif_healp_nest_6_gc, color='C0', label='(GC) HEALPix order = 6')
plot(search_radius_dif[:len(time_required_dif_healp_nest_8_gc)],time_required_dif_healp_nest_8_gc, color='C1', label='(GC) HEALPix order = 8')
plot(search_radius_dif[:len(time_required_dif_healp_nest_10_gc)],time_required_dif_healp_nest_10_gc, color='C2', label='(GC) HEALPix order = 10')
plot(search_radius_dif[:len(time_required_dif_healp_nest_6_gnp)],time_required_dif_healp_nest_6_gnp, color='C0', ls=':', label='(GNP) HEALPix order = 6')
plot(search_radius_dif[:len(time_required_dif_healp_nest_8_gnp)],time_required_dif_healp_nest_8_gnp, color='C1', ls=':', label='(GNP) HEALPix order = 8')
plot(search_radius_dif[:len(time_required_dif_healp_nest_10_gnp)],time_required_dif_healp_nest_10_gnp, color='C2', ls=':', label='(GNP) HEALPix order = 10')
plot(search_radius_direct[:len(time_required_direct_gc)],time_required_direct_gc, color='C3', label='(GC) Direct query')
plot(search_radius_direct[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C3', ls=':', label='(GNP) Direct query')

grid()
xlim(1,500000)
ylim(0.001,500)
xscale('log')
yscale('log')
xlabel('Search radius / arcsec')
ylabel('Time taken / seconds')
title('MySQL search radius (HEALPix)')
legend()
savefig(output_path + 'mysql_healp_timing.png')


figure(3)
clf()
plot(number_results_dif_healp_nest_6_gc[:len(time_required_dif_healp_nest_6_gc)],time_required_dif_healp_nest_6_gc, color='C0', label='(GC) HEALPix order = 6')
plot(number_results_dif_healp_nest_8_gc[:len(time_required_dif_healp_nest_8_gc)],time_required_dif_healp_nest_8_gc, color='C1', label='(GC) HEALPix order = 8')
plot(number_results_dif_healp_nest_10_gc[:len(time_required_dif_healp_nest_10_gc)],time_required_dif_healp_nest_10_gc, color='C2', label='(GC) HEALPix order = 10')
plot(number_results_dif_healp_nest_6_gnp[:len(time_required_dif_healp_nest_6_gnp)],time_required_dif_healp_nest_6_gnp, color='C0', ls=':', label='(GNP) HEALPix order = 6')
plot(number_results_dif_healp_nest_8_gnp[:len(time_required_dif_healp_nest_8_gnp)],time_required_dif_healp_nest_8_gnp, color='C1', ls=':', label='(GNP) HEALPix order = 8')
plot(number_results_dif_healp_nest_10_gnp[:len(time_required_dif_healp_nest_10_gnp)],time_required_dif_healp_nest_10_gnp, color='C2', ls=':', label='(GNP) HEALPix order = 10')
plot(number_results_direct_gc[:len(time_required_direct_gc)],time_required_direct_gc, color='C3', label='(GC) Direct query')
plot(number_results_direct_gnp[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C3', ls=':', label='(GNP) Direct query')

scatter(number_results_direct_gc[:len(time_required_direct_gc)],time_required_direct_gc, color='C3', s=5)
scatter(number_results_direct_gnp[:len(time_required_direct_gnp)],time_required_direct_gnp, color='C3', s=5)

grid()
xlim(1,1200000)
ylim(0.0001,500)
xscale('log')
yscale('log')
xlabel('Number of matches')
ylabel('Time taken / seconds')
legend()
savefig(output_path + 'mysql_number_of_matches.png')

