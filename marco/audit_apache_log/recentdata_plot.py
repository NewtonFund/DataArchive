import os
import re
import time
import subprocess
import numpy as np
from collections import Counter
from datetime import timedelta
from datetime import datetime
from matplotlib.pyplot import *
ion()

# Get output path if provided, default at ~/Desktop
current_file = __file__
try:
    output_path = argv[1]
except:
    real_path = os.path.realpath(current_file)  # /home/user/test/my_script.py
    output_path = os.path.dirname(real_path) + '/output/'

def get_columns(text, regex):
    """
    Remove lines in the chuck of log that was added before the given time.
    (minimum requirement python 2.3)
    """
    text = text.splitlines()
    # populate logs into the dictionary
    i1 = []
    i2 = []
    i3 = []
    i4 = []
    i5 = []
    i6 = []
    i7 = []
    i8 = []
    i9 = []
    for i, line in enumerate(text):
        items = re.match(regex, line).groups()
        i1.append(items[0])
        i2.append(items[1])
        i3.append(items[2])
        i4.append(items[3])
        i5.append(items[4])
        i6.append(items[5])
        i7.append(items[6])
        i8.append(items[7])
        i9.append(items[8])
    return i1, i2, i3, i4, i5, i6, i7, i8, i9


def isotime_to_unixtime(t):
    t_diff = timedelta(hours=int(t[-5:-2]), minutes=int(t[-2:]))
    # this line can be replaced by strptime in python 2.4+
    item_time = datetime(
        *(time.strptime(t[:-6], "%d/%b/%Y:%H:%M:%S")[0:6])
        ) + t_diff
    # unix time
    return time.mktime(item_time.timetuple())



def isotime_get_hours(t):
    t_diff = timedelta(hours=int(t[-5:-2]), minutes=int(t[-2:]))
    # this line can be replaced by strptime in python 2.4+
    item_time = datetime(
        *(time.strptime(t[:-6], "%d/%b/%Y:%H:%M:%S")[0:6])
        ) + t_diff
    # unix time
    return item_time.timetuple().tm_hour



log_path = output_path + "log_recentdata.txt"

# The Apache 2.0 NCSA extended/combined log format:
# "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
# example:
#
# 80.229.2.174
# -
# NSO_Priority_3
# [20/May/2017:18:00:18 +0100]
# "GET /DataProd/recentdata/NSO_Priority_3/20170519/h_e_20170519_15_1_1_9.head
#  HTTP/1.1"
# 200
# 16966
# "http://telescope.livjm.ac.uk/DataProd/recentdata/NSO_Priority_3/20170519/"
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML,
#  like Gecko) Chrome/58.0.3029.110 Safari/537.36"

# regular expression to split the above text
regex_access_log = '([(\d\.)]+) (.*) (.*) \[(.*?)\] "(.*?)" (\d+) (.*) ' +\
                   '"(.*?)" "(.*?)"'


lines = open(log_path,'r').read()
lines_reduced = get_columns(lines, regex_access_log)

mask = (np.array(lines_reduced[5])=='200') & (np.array(lines_reduced[7]) != 'http://telescope.livjm.ac.uk/DataProd/recentdata/')

ip = np.array(lines_reduced[0])[mask]
proposalID = np.array(lines_reduced[2])[mask]
eng_mask = (proposalID=='eng')
NSO_mask = (proposalID=='NSO_Priority_1') | (proposalID=='NSO_Priority_2') | (proposalID=='NSO_Priority_3')

number_lines = len(ip)
access_time = np.array(lines_reduced[3])[mask]
access_time_unix = np.zeros(number_lines)
access_time_hour = np.zeros(number_lines)
for i in range(number_lines):
    access_time_unix[i] = isotime_to_unixtime(access_time[i])
    access_time_hour[i] = isotime_get_hours(access_time[i])

# separating rows into ['log', 'tar', 'tgz', 'tarlist', 'not_file', 'gz', 'jpg', 'avi', 'fits']
request = np.array(lines_reduced[4])[mask]
file_type = []
for i in range(number_lines):
    request[i] = request[i][4:-9]
    try:
        temp = request[i].split('.')[-1]
        if len(temp) < 8:
            file_type.append(temp)
        else:
            file_type.append('not_file')
    except:
        file_type.append('not_file')

file_type = np.array(file_type)

request_size = np.array(lines_reduced[6])[mask].astype('int')
page = np.array(lines_reduced[7])[mask]
system = np.array(lines_reduced[8])[mask]

jpg_file_position = (file_type=='jpg')
log_file_position = (file_type=='log')
fits_file_position = (file_type=='fits')
tar_file_position = (file_type=='tar')
tarlist_file_position = (file_type=='tarlist')
tgz_file_position = (file_type=='tgz')
gz_file_position = (file_type=='gz')
avi_file_position = (file_type=='avi')


timerange = np.ptp(access_time_unix)/3600./24.
number_of_weeks = int(timerange/7.)
bin_size = timerange/number_of_weeks*7./365.35/2.

n_jpg, t_jpg = np.histogram(access_time_unix[jpg_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log, t_log = np.histogram(access_time_unix[log_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits, t_fits = np.histogram(access_time_unix[fits_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tar, t_tar = np.histogram(access_time_unix[tar_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tarlist, t_tarlist = np.histogram(access_time_unix[tarlist_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tgz, t_tgz = np.histogram(access_time_unix[tgz_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_gz, t_gz = np.histogram(access_time_unix[gz_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_avi, t_avi = np.histogram(access_time_unix[avi_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)

jpg_file_non_eng_position = (file_type=='jpg') & (eng_mask==False)
log_file_non_eng_position = (file_type=='log') & (eng_mask==False)
fits_file_non_eng_position = (file_type=='fits') & (eng_mask==False)
tar_file_non_eng_position = (file_type=='tar') & (eng_mask==False)
tarlist_file_non_eng_position = (file_type=='tarlist') & (eng_mask==False)
tgz_file_non_eng_position = (file_type=='tgz') & (eng_mask==False)
gz_file_non_eng_position = (file_type=='gz') & (eng_mask==False)
avi_file_non_eng_position = (file_type=='avi') & (eng_mask==False)

n_jpg_non_eng, t_jpg = np.histogram(access_time_unix[jpg_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_non_eng, t_log = np.histogram(access_time_unix[log_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_non_eng, t_fits = np.histogram(access_time_unix[fits_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tar_non_eng, t_tar = np.histogram(access_time_unix[tar_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tarlist_non_eng, t_tarlist = np.histogram(access_time_unix[tarlist_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tgz_non_eng, t_tgz = np.histogram(access_time_unix[tgz_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_gz_non_eng, t_gz = np.histogram(access_time_unix[gz_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_avi_non_eng, t_tar = np.histogram(access_time_unix[avi_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)

jpg_file_non_eng_private_position = (file_type=='jpg') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
log_file_non_eng_private_position = (file_type=='log') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
fits_file_non_eng_private_position = (file_type=='fits') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
tar_file_non_eng_private_position = (file_type=='tar') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
tarlist_file_non_eng_private_position = (file_type=='tarlist') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
tgz_file_non_eng_private_position = (file_type=='tgz') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
gz_file_non_eng_private_position = (file_type=='gz') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
avi_file_non_eng_private_position = (file_type=='avi') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)

n_jpg_non_eng_private, t_jpg = np.histogram(access_time_unix[jpg_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_non_eng_private, t_log = np.histogram(access_time_unix[log_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_non_eng_private, t_fits = np.histogram(access_time_unix[fits_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tar_non_eng_private, t_tar = np.histogram(access_time_unix[tar_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tarlist_non_eng_private, t_tarlist = np.histogram(access_time_unix[tarlist_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_tgz_non_eng_private, t_tgz = np.histogram(access_time_unix[tgz_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_gz_non_eng_private, t_gz = np.histogram(access_time_unix[gz_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_avi_non_eng_private, t_head = np.histogram(access_time_unix[avi_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)


figure(1, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_jpg[:-1]+bin_size, n_jpg, label='jpg (all)', ls=':', color='C0')
plot(t_log[:-1]+bin_size, n_log, label='log (all)', ls=':', color='C1')
plot(t_fits[:-1]+bin_size, n_fits, label='fits (all)', ls=':', color='C2')
plot(t_tar[:-1]+bin_size, n_tar, label='tar (all)', ls=':', color='C3')
plot(t_tarlist[:-1]+bin_size, n_tarlist, label='tarlist (all)', ls=':', color='C4')
plot(t_tgz[:-1]+bin_size, n_tgz, label='tgz (all)', ls=':', color='C5')
plot(t_gz[:-1]+bin_size, n_gz, label='gz (all)', ls=':', color='C6')
plot(t_avi[:-1]+bin_size, n_avi, label='avi (all)', ls=':', color='C7')
plot(t_jpg[:-1]+bin_size, n_jpg_non_eng_private, label='jpg (non-eng/ops/NSO/unknown)', color='C0')
plot(t_log[:-1]+bin_size, n_log_non_eng_private, label='log (non-eng/ops/NSO/unknown)', color='C1')
plot(t_fits[:-1]+bin_size, n_fits_non_eng_private, label='fits (non-eng/ops/NSO/unknown)', color='C2')
plot(t_tar[:-1]+bin_size, n_tar_non_eng_private, label='tar (non-eng/ops/NSO/unknown)', color='C3')
plot(t_tarlist[:-1]+bin_size, n_tarlist_non_eng_private, label='tarlist (non-eng/ops/NSO/unknown)', color='C4')
plot(t_tgz[:-1]+bin_size, n_tgz_non_eng_private, label='tgz (non-eng/ops/NSO/unknown)', color='C5')
plot(t_gz[:-1]+bin_size, n_gz_non_eng_private, label='gz (non-eng/ops/NSO/unknown)', color='C6')
plot(t_avi[:-1]+bin_size, n_avi_non_eng_private, label='avi (non-eng/ops/NSO/unknown)', color='C7')
legend(ncol=2)
grid()
ylim(0,100)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('recentdata usage (22 Jan - 5 Jun 2017)')
savefig(output_path + 'recentdata_usage.png')


ip_eng = np.array(list(set(ip[eng_mask])))
ip_eng_mask = np.in1d(ip, ip_eng) | (proposalID == '-') | (file_type == 'not_file')
ip_standrew_mask = (ip=='138.251.106.151')

ip_jpg_count = Counter(ip[(ip_eng_mask==False)&jpg_file_non_eng_position])
ip_jpg_address, n_ip_jpg = np.array(ip_jpg_count.keys()), np.array(ip_jpg_count.values())
ip_jpg_sort_order = np.argsort(n_ip_jpg)
ip_jpg_address, n_ip_jpg = ip_jpg_address[ip_jpg_sort_order], n_ip_jpg[ip_jpg_sort_order]

ip_log_count = Counter(ip[(ip_eng_mask==False)&log_file_non_eng_position])
ip_log_address, n_ip_log = np.array(ip_log_count.keys()), np.array(ip_log_count.values())
ip_log_sort_order = np.argsort(n_ip_log)
ip_log_address, n_ip_log = ip_log_address[ip_log_sort_order], n_ip_log[ip_log_sort_order]

ip_fits_count = Counter(ip[(ip_eng_mask==False)&fits_file_non_eng_position])
ip_fits_address, n_ip_fits = np.array(ip_fits_count.keys()), np.array(ip_fits_count.values())
ip_fits_sort_order = np.argsort(n_ip_fits)
ip_fits_address, n_ip_fits = ip_fits_address[ip_fits_sort_order], n_ip_fits[ip_fits_sort_order]

ip_tar_count = Counter(ip[(ip_eng_mask==False)&tar_file_non_eng_position])
ip_tar_address, n_ip_tar = np.array(ip_tar_count.keys()), np.array(ip_tar_count.values())
ip_tar_sort_order = np.argsort(n_ip_tar)
ip_tar_address, n_ip_tar = ip_tar_address[ip_tar_sort_order], n_ip_tar[ip_tar_sort_order]

ip_tgz_count = Counter(ip[(ip_eng_mask==False)&tgz_file_non_eng_position])
ip_tgz_address, n_ip_tgz = np.array(ip_tgz_count.keys()), np.array(ip_tgz_count.values())
ip_tgz_sort_order = np.argsort(n_ip_tgz)
ip_tgz_address, n_ip_tgz = ip_tgz_address[ip_tgz_sort_order], n_ip_tgz[ip_tgz_sort_order]


figure(2, figsize=(12,8))
clf()
bar(range(len(ip_jpg_address)), n_ip_jpg[::-1], color='C0',log=True, label='jpg')
bar(range(len(ip_fits_address)), n_ip_fits[::-1], color='C2',log=True, alpha=0.8, label='log')
bar(range(len(ip_log_address)), n_ip_log[::-1], color='C1',log=True, alpha=0.6, label='fits')
bar(range(len(ip_tar_address)), n_ip_tar[::-1], color='C3',log=True, alpha=0.4, label='tar')
bar(range(len(ip_tgz_address)), n_ip_tgz[::-1], color='C3',log=True, alpha=0.4, label='tgz')
xlabel('unique ip')
ylabel('Number')
title('recent data usage by unique ip (22 Jan - 5 Jun 2017)')
xlim(0,235)
grid()
legend()
savefig(output_path + 'recentdata_usage_by_ip.png')



figure(3, figsize=(12,8))
clf()
hist(access_time_hour[ip_eng_mask==False],bins=24,range=(0,24),color='grey', alpha=0.5, label='total')
hist(access_time_hour[(ip_eng_mask==False)&jpg_file_non_eng_position],bins=24,range=(0,24),color='C0', label='jpg', histtype='step')
hist(access_time_hour[(ip_eng_mask==False)&log_file_non_eng_position],bins=24,range=(0,24),color='C1', label='log', histtype='step')
hist(access_time_hour[(ip_eng_mask==False)&fits_file_non_eng_position],bins=24,range=(0,24),color='C2', label='fits', histtype='step')
hist(access_time_hour[(ip_eng_mask==False)&tar_file_non_eng_position],bins=24,range=(0,24),color='C3', label='tar', histtype='step')
hist(access_time_hour[(ip_eng_mask==False)&tgz_file_non_eng_position],bins=24,range=(0,24),color='C4', label='tgz', histtype='step')
xlim(0,24)
grid()
title('Hours (UT) when recent data files opened (22 Jan - 5 Jun 2017)')
xlabel('Hours')
ylabel('Number')
text(6.5, 160, '<- St. Andrews')
legend()
savefig(output_path + 'recentdata_usage_by_hours.png')

ip_ljmu = np.ones(len(ip))==0

for k, ip_k in enumerate(ip):
    if ip_k[:12] == '150.204.241.':
        ip_ljmu[k] = True


ip_eng_mask_2 = ip_eng_mask | ip_ljmu | NSO_mask | ip_standrew_mask

figure(4, figsize=(12,8))
clf()
hist(access_time_hour[ip_eng_mask_2==False],bins=24,range=(0,24),color='grey', alpha=0.5, label='total')
hist(access_time_hour[(ip_eng_mask_2==False)&jpg_file_non_eng_position],bins=24,range=(0,24),color='C0', label='jpg', histtype='step')
hist(access_time_hour[(ip_eng_mask_2==False)&log_file_non_eng_position],bins=24,range=(0,24),color='C1', label='log', histtype='step')
hist(access_time_hour[(ip_eng_mask_2==False)&fits_file_non_eng_position],bins=24,range=(0,24),color='C2', label='fits', histtype='step')
hist(access_time_hour[(ip_eng_mask_2==False)&tar_file_non_eng_position],bins=24,range=(0,24),color='C3', label='tar', histtype='step')
hist(access_time_hour[(ip_eng_mask_2==False)&tgz_file_non_eng_position],bins=24,range=(0,24),color='C4', label='tgz', histtype='step')
xlim(0,24)
grid()
title('Hours (UT) when redent data files opened (ip & NSO filtered, 15 Jan - 1 Jun 2017)')
xlabel('Hours')
ylabel('Number')
legend()
savefig(output_path + 'recentdata_usage_ip_&_NSO_filtered_by_hours.png')



