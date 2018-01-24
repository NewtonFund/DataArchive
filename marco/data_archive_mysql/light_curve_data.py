import os
import inspect
import time
import numpy as np
import mysql.connector
import gc
import matplotlib
try:
    matplotlib.use('macosx')
except:
    pass

from matplotlib.pyplot import *
ion()

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
query = ("SELECT * FROM obsdat WHERE `usnoref` = '0552-0713804';")
cur.execute(query)
temp = cur.fetchall()
cur.close()
cur = None

temp = np.load('lightcurve.npy')
mjd = np.array(temp)[:,1]
RA = np.array(temp)[:,2]
DEC = np.array(temp)[:,3]
flux = np.array(temp)[:,4]
flux_err = np.array(temp)[:,5]
rcat = np.array(temp)[:,10]
sn = flux.astype('float')/flux_err.astype('float')

from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import units as u

alt = np.zeros(len(RA))
az = np.zeros(len(RA))
for i in range(len(RA)):
    coord = SkyCoord(ra=float(RA[i]), dec=float(DEC[i]), unit=(u.degree, u.degree))
    lapalma = EarthLocation(lat=28.7636*u.deg, lon=-17.8947*u.deg, height=2363*u.m)
    obs_time = Time(float(mjd[i]), format='mjd')
    coord_altaz = coord.transform_to(AltAz(obstime=obs_time,location=lapalma))
    alt[i] = coord_altaz.alt.value
    az[i] = coord_altaz.az.value



airmass = 1. / np.sin(np.radians(alt + 244/(165.+47*alt**1.1)))


mask_lt_180 = az < 180.
mask_gt_180 = az >= 180.

figure(1)
clf()
scatter(jd.astype('float'), rcat.astype('float'), s=1)
ylim(8,11)
grid()

figure(2)
clf()
scatter(jd.astype('float'), rcat.astype('float')-airmass*0.12, s=1, color='red')
ylim(8,11)
grid()

figure(3)
clf()
scatter(alt[mask_lt_180], rcat.astype('float')[mask_lt_180], s=1)
ylim(8,11)
grid()

figure(4)
clf()
scatter(alt[mask_gt_180], rcat.astype('float')[mask_gt_180], s=1)
ylim(8,11)
grid()

alt_sort_order = np.argsort(alt)
rcat_sorted = rcat.astype('float')[alt_sort_order]
alt_sorted = alt[alt_sort_order]

moving_median_mag = np.zeros(len(RA)-20)
moving_median_alt = np.zeros(len(RA)-20)
for i in range(len(RA)-20):
    moving_median_mag[i] = np.mean(rcat_sorted[i:i+20])
    moving_median_alt[i] = np.mean(alt_sorted[i:i+20])


figure(2)
plot(moving_median_alt, moving_median_mag)

figure(3)
plot(moving_median_alt, moving_median_mag)
