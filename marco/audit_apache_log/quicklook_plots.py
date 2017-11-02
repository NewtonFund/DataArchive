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



log_path = output_path + "log_quicklook.txt"

# The Apache 2.0 NCSA extended/combined log format:
# "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\""
# example:
#
# 80.229.2.174
# -
# NSO_Priority_3
# [20/May/2017:18:00:18 +0100]
# "GET /DataProd/quicklook/NSO_Priority_3/20170519/h_e_20170519_15_1_1_9.head
#  HTTP/1.1"
# 200
# 16966
# "http://telescope.livjm.ac.uk/DataProd/quicklook/NSO_Priority_3/20170519/"
# "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML,
#  like Gecko) Chrome/58.0.3029.110 Safari/537.36"

# regular expression to split the above text
regex_access_log = '([(\d\.)]+) (.*) (.*) \[(.*?)\] "(.*?)" (\d+) (.*) ' +\
                   '"(.*?)" "(.*?)"'


lines = open(log_path,'r').read()
lines_reduced = get_columns(lines, regex_access_log)

mask = (np.array(lines_reduced[5])=='200') & (np.array(lines_reduced[7]) != 'http://telescope.livjm.ac.uk/DataProd/quicklook/')

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

request = np.array(lines_reduced[4])[mask]
file_type = []
for i in range(number_lines):
    request[i] = request[i][4:-9]
    try:
        file_type.append(request[i].split('.')[1])
    except:
        file_type.append('not_file')

file_type = np.array(file_type)

request_size = np.array(lines_reduced[6])[mask].astype('int')
page = np.array(lines_reduced[7])[mask]
system = np.array(lines_reduced[8])[mask]

jpg_file_position = (file_type=='jpg')
log_file_position = (file_type=='log')
fits_file_position = (file_type=='fits')
head_file_position = (file_type=='head')

timerange = np.ptp(access_time_unix)/3600./24.
number_of_weeks = int(timerange/7.)
bin_size = timerange/number_of_weeks*7./365.35/2.

n_jpg, t_jpg = np.histogram(access_time_unix[jpg_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log, t_log = np.histogram(access_time_unix[log_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits, t_fits = np.histogram(access_time_unix[fits_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head, t_head = np.histogram(access_time_unix[head_file_position]/3600./24./365.25+1970.,bins=number_of_weeks)

jpg_file_non_eng_position = (file_type=='jpg') & (eng_mask==False)
log_file_non_eng_position = (file_type=='log') & (eng_mask==False)
fits_file_non_eng_position = (file_type=='fits') & (eng_mask==False)
head_file_non_eng_position = (file_type=='head') & (eng_mask==False)

n_jpg_non_eng, t_jpg = np.histogram(access_time_unix[jpg_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_non_eng, t_log = np.histogram(access_time_unix[log_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_non_eng, t_fits = np.histogram(access_time_unix[fits_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_non_eng, t_head = np.histogram(access_time_unix[head_file_non_eng_position]/3600./24./365.25+1970.,bins=number_of_weeks)

jpg_file_non_eng_private_position = (file_type=='jpg') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
log_file_non_eng_private_position = (file_type=='log') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
fits_file_non_eng_private_position = (file_type=='fits') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)
head_file_non_eng_private_position = (file_type=='head') & (eng_mask==False) & (proposalID!='-') & (NSO_mask==False)

n_jpg_non_eng_private, t_jpg = np.histogram(access_time_unix[jpg_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_non_eng_private, t_log = np.histogram(access_time_unix[log_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_non_eng_private, t_fits = np.histogram(access_time_unix[fits_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_non_eng_private, t_head = np.histogram(access_time_unix[head_file_non_eng_private_position]/3600./24./365.25+1970.,bins=number_of_weeks)


figure(1, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_jpg[:-1]+bin_size, n_jpg, label='jpg (all)', ls=':', color='C0')
plot(t_log[:-1]+bin_size, n_log, label='log (all)', ls=':', color='C1')
plot(t_fits[:-1]+bin_size, n_fits, label='fits (all)', ls=':', color='C2')
plot(t_head[:-1]+bin_size, n_head, label='header (all)', ls=':', color='C3')
plot(t_jpg[:-1]+bin_size, n_jpg_non_eng, label='jpg (non-eng)', ls='-.', color='C0')
plot(t_log[:-1]+bin_size, n_log_non_eng, label='log (non-eng)', ls='-.', color='C1')
plot(t_fits[:-1]+bin_size, n_fits_non_eng, label='fits (non-eng)', ls='-.', color='C2')
plot(t_head[:-1]+bin_size, n_head_non_eng, label='header (non-eng)', ls='-.', color='C3')
plot(t_jpg[:-1]+bin_size, n_jpg_non_eng_private, label='jpg (non-eng/ops/NSO/unknown)', color='C0')
plot(t_log[:-1]+bin_size, n_log_non_eng_private, label='log (non-eng/ops/NSO/unknown)', color='C1')
plot(t_fits[:-1]+bin_size, n_fits_non_eng_private, label='fits (non-eng/ops/NSO/unknown)', color='C2')
plot(t_head[:-1]+bin_size, n_head_non_eng_private, label='header (non-eng/ops/NSO/unknown)', color='C3')
legend()
grid()
ylim(0,500)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook usage (15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_usage.png')



proposal_type = ['CL', 'IL', 'JL', 'PL', 'PQ', 'TL', 'ZL', 'NS', '-', 'eng', 'ops']
p_cl = (np.ones(len(proposalID)) == 0)
p_il = (np.ones(len(proposalID)) == 0)
p_jl = (np.ones(len(proposalID)) == 0)
p_pl = (np.ones(len(proposalID)) == 0)
p_pq = (np.ones(len(proposalID)) == 0)
p_tl = (np.ones(len(proposalID)) == 0)
p_zl = (np.ones(len(proposalID)) == 0)
p_ns = (np.ones(len(proposalID)) == 0)
p_unknown = (np.ones(len(proposalID)) == 0)
p_eng = (np.ones(len(proposalID)) == 0)
p_ops = (np.ones(len(proposalID)) == 0)
for i, proposal in enumerate(proposalID):
    p_len = len(proposal)
    if p_len<=3:
        if proposal == '-':
            p_unknown[i] = True
        if proposal == 'eng':
            p_eng[i] = True
        if proposal == 'ops':
            p_ops[i] = True
    else:
        if proposal[:2] == 'CL':
            p_cl[i] = True
        if proposal[:2] == 'IL':
            p_il[i] = True
        if proposal[:2] == 'JL':
            p_jl[i] = True
        if proposal[:2] == 'PL':
            p_pl[i] = True
        if proposal[:2] == 'PQ':
            p_pq[i] = True
        if proposal[:2] == 'TL':
            p_tl[i] = True
        if proposal[:2] == 'ZL':
            p_zl[i] = True
        if proposal[:2] == 'NS':
            p_ns[i] = True


n_jpg_cl, t_jpg_cl = np.histogram(access_time_unix[jpg_file_position*p_cl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_il, t_jpg_il = np.histogram(access_time_unix[jpg_file_position*p_il]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_jl, t_jpg_jl = np.histogram(access_time_unix[jpg_file_position*p_jl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_pl, t_jpg_pl = np.histogram(access_time_unix[jpg_file_position*p_pl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_pq, t_jpg_pq = np.histogram(access_time_unix[jpg_file_position*p_pq]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_tl, t_jpg_tl = np.histogram(access_time_unix[jpg_file_position*p_tl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_zl, t_jpg_zl = np.histogram(access_time_unix[jpg_file_position*p_zl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_ns, t_jpg_ns = np.histogram(access_time_unix[jpg_file_position*p_ns]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_unknown, t_jpg_unknown = np.histogram(access_time_unix[jpg_file_position*p_unknown]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_eng, t_jpg_eng = np.histogram(access_time_unix[jpg_file_position*p_eng]/3600./24./365.25+1970.,bins=number_of_weeks)
n_jpg_ops, t_jpg_ops = np.histogram(access_time_unix[jpg_file_position*p_ops]/3600./24./365.25+1970.,bins=number_of_weeks)

figure(11, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_jpg_cl[:-1]+bin_size, n_jpg_cl, label='CL', ls=':', color='C0')
plot(t_jpg_il[:-1]+bin_size, n_jpg_il, label='IL', ls=':', color='C1')
plot(t_jpg_jl[:-1]+bin_size, n_jpg_jl, label='JL', ls=':', color='C2')
plot(t_jpg_pl[:-1]+bin_size, n_jpg_pl, label='PL', ls=':', color='C3')
plot(t_jpg_pq[:-1]+bin_size, n_jpg_pq, label='PQ', ls=':', color='C4')
plot(t_jpg_tl[:-1]+bin_size, n_jpg_tl, label='TL', ls=':', color='C5')
plot(t_jpg_zl[:-1]+bin_size, n_jpg_zl, label='ZL', ls=':', color='C6')
plot(t_jpg_ns[:-1]+bin_size, n_jpg_ns, label='NSO', ls=':', color='C7')
plot(t_jpg_unknown[:-1]+bin_size, n_jpg_unknown, label='unknown', ls=':', color='C8')
plot(t_jpg_eng[:-1]+bin_size, n_jpg_eng, label='eng', ls=':', color='C9')
plot(t_jpg_ops[:-1]+bin_size, n_jpg_ops, label='ops', color='C0')
legend()
grid()
ylim(0,300)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook jpg usage by proposal(15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_jpg_usage_by_proposal.png')



n_log_cl, t_log_cl = np.histogram(access_time_unix[log_file_position*p_cl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_il, t_log_il = np.histogram(access_time_unix[log_file_position*p_il]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_jl, t_log_jl = np.histogram(access_time_unix[log_file_position*p_jl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_pl, t_log_pl = np.histogram(access_time_unix[log_file_position*p_pl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_pq, t_log_pq = np.histogram(access_time_unix[log_file_position*p_pq]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_tl, t_log_tl = np.histogram(access_time_unix[log_file_position*p_tl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_zl, t_log_zl = np.histogram(access_time_unix[log_file_position*p_zl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_ns, t_log_ns = np.histogram(access_time_unix[log_file_position*p_ns]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_unknown, t_log_unknown = np.histogram(access_time_unix[log_file_position*p_unknown]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_eng, t_log_eng = np.histogram(access_time_unix[log_file_position*p_eng]/3600./24./365.25+1970.,bins=number_of_weeks)
n_log_ops, t_log_ops = np.histogram(access_time_unix[log_file_position*p_ops]/3600./24./365.25+1970.,bins=number_of_weeks)

figure(12, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_log_cl[:-1]+bin_size, n_log_cl, label='CL', ls=':', color='C0')
plot(t_log_il[:-1]+bin_size, n_log_il, label='IL', ls=':', color='C1')
plot(t_log_jl[:-1]+bin_size, n_log_jl, label='JL', ls=':', color='C2')
plot(t_log_pl[:-1]+bin_size, n_log_pl, label='PL', ls=':', color='C3')
plot(t_log_pq[:-1]+bin_size, n_log_pq, label='PQ', ls=':', color='C4')
plot(t_log_tl[:-1]+bin_size, n_log_tl, label='TL', ls=':', color='C5')
plot(t_log_zl[:-1]+bin_size, n_log_zl, label='ZL', ls=':', color='C6')
plot(t_log_ns[:-1]+bin_size, n_log_ns, label='NSO', ls=':', color='C7')
plot(t_log_unknown[:-1]+bin_size, n_log_unknown, label='unknown', ls=':', color='C8')
plot(t_log_eng[:-1]+bin_size, n_log_eng, label='eng', ls=':', color='C9')
plot(t_log_ops[:-1]+bin_size, n_log_ops, label='ops', color='C0')
legend()
grid()
ylim(0,50)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook log usage by proposal(15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_log_usage_by_proposal.png')



n_fits_cl, t_fits_cl = np.histogram(access_time_unix[fits_file_position*p_cl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_il, t_fits_il = np.histogram(access_time_unix[fits_file_position*p_il]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_jl, t_fits_jl = np.histogram(access_time_unix[fits_file_position*p_jl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_pl, t_fits_pl = np.histogram(access_time_unix[fits_file_position*p_pl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_pq, t_fits_pq = np.histogram(access_time_unix[fits_file_position*p_pq]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_tl, t_fits_tl = np.histogram(access_time_unix[fits_file_position*p_tl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_zl, t_fits_zl = np.histogram(access_time_unix[fits_file_position*p_zl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_ns, t_fits_ns = np.histogram(access_time_unix[fits_file_position*p_ns]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_unknown, t_fits_unknown = np.histogram(access_time_unix[fits_file_position*p_unknown]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_eng, t_fits_eng = np.histogram(access_time_unix[fits_file_position*p_eng]/3600./24./365.25+1970.,bins=number_of_weeks)
n_fits_ops, t_fits_ops = np.histogram(access_time_unix[fits_file_position*p_ops]/3600./24./365.25+1970.,bins=number_of_weeks)

figure(13, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_fits_cl[:-1]+bin_size, n_fits_cl, label='CL', ls=':', color='C0')
plot(t_fits_il[:-1]+bin_size, n_fits_il, label='IL', ls=':', color='C1')
plot(t_fits_jl[:-1]+bin_size, n_fits_jl, label='JL', ls=':', color='C2')
plot(t_fits_pl[:-1]+bin_size, n_fits_pl, label='PL', ls=':', color='C3')
plot(t_fits_pq[:-1]+bin_size, n_fits_pq, label='PQ', ls=':', color='C4')
plot(t_fits_tl[:-1]+bin_size, n_fits_tl, label='TL', ls=':', color='C5')
plot(t_fits_zl[:-1]+bin_size, n_fits_zl, label='ZL', ls=':', color='C6')
plot(t_fits_ns[:-1]+bin_size, n_fits_ns, label='NSO', ls=':', color='C7')
plot(t_fits_unknown[:-1]+bin_size, n_fits_unknown, label='unknown', ls=':', color='C8')
plot(t_fits_eng[:-1]+bin_size, n_fits_eng, label='eng', ls=':', color='C9')
plot(t_fits_ops[:-1]+bin_size, n_fits_ops, label='ops', color='C0')
legend()
grid()
ylim(0,200)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook fits usage by proposal(15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_fits_usage_by_proposal.png')


n_head_cl, t_head_cl = np.histogram(access_time_unix[head_file_position*p_cl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_il, t_head_il = np.histogram(access_time_unix[head_file_position*p_il]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_jl, t_head_jl = np.histogram(access_time_unix[head_file_position*p_jl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_pl, t_head_pl = np.histogram(access_time_unix[head_file_position*p_pl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_pq, t_head_pq = np.histogram(access_time_unix[head_file_position*p_pq]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_tl, t_head_tl = np.histogram(access_time_unix[head_file_position*p_tl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_zl, t_head_zl = np.histogram(access_time_unix[head_file_position*p_zl]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_ns, t_head_ns = np.histogram(access_time_unix[head_file_position*p_ns]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_unknown, t_head_unknown = np.histogram(access_time_unix[head_file_position*p_unknown]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_eng, t_head_eng = np.histogram(access_time_unix[head_file_position*p_eng]/3600./24./365.25+1970.,bins=number_of_weeks)
n_head_ops, t_head_ops = np.histogram(access_time_unix[head_file_position*p_ops]/3600./24./365.25+1970.,bins=number_of_weeks)

figure(14, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_head_cl[:-1]+bin_size, n_head_cl, label='CL', ls=':', color='C0')
plot(t_head_il[:-1]+bin_size, n_head_il, label='IL', ls=':', color='C1')
plot(t_head_jl[:-1]+bin_size, n_head_jl, label='JL', ls=':', color='C2')
plot(t_head_pl[:-1]+bin_size, n_head_pl, label='PL', ls=':', color='C3')
plot(t_head_pq[:-1]+bin_size, n_head_pq, label='PQ', ls=':', color='C4')
plot(t_head_tl[:-1]+bin_size, n_head_tl, label='TL', ls=':', color='C5')
plot(t_head_zl[:-1]+bin_size, n_head_zl, label='ZL', ls=':', color='C6')
plot(t_head_ns[:-1]+bin_size, n_head_ns, label='NSO', ls=':', color='C7')
plot(t_head_unknown[:-1]+bin_size, n_head_unknown, label='unknown', ls=':', color='C8')
plot(t_head_eng[:-1]+bin_size, n_head_eng, label='eng', ls=':', color='C9')
plot(t_head_ops[:-1]+bin_size, n_head_ops, label='ops', color='C0')
legend()
grid()
ylim(0,25)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook header usage by proposal(15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_header_usage_by_proposal.png')



figure(15, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_jpg_cl[:-1]+bin_size, n_jpg_cl + n_jpg_il + n_jpg_jl + n_jpg_pl + n_jpg_pq + n_jpg_tl + n_jpg_zl, label='Science', ls=':', color='C0')
plot(t_jpg_ns[:-1]+bin_size, n_jpg_ns, label='NSO', ls=':', color='C1')
plot(t_jpg_eng[:-1]+bin_size, n_jpg_unknown + n_jpg_eng + n_jpg_ops, label='Others', ls=':', color='C2')
legend()
grid()
ylim(0,300)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook jpg usage by proposal group (15 Jan - 1 Jun 2017)')
savefig(output + 'quicklook_jpg_usage_by_group.png')



figure(16, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_fits_cl[:-1]+bin_size, n_fits_cl + n_fits_il + n_fits_jl + n_fits_pl + n_fits_pq + n_fits_tl + n_fits_zl, label='Science', ls=':', color='C0')
plot(t_fits_ns[:-1]+bin_size, n_fits_ns, label='NSO', ls=':', color='C1')
plot(t_fits_eng[:-1]+bin_size, n_fits_unknown + n_fits_eng + n_fits_ops, label='Others', ls=':', color='C2')
legend()
grid()
ylim(0,350)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook fits usage by proposal group (15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_fits_usage_by_group.png')



figure(17, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_log_cl[:-1]+bin_size, n_log_cl + n_log_il + n_log_jl + n_log_pl + n_log_pq + n_log_tl + n_log_zl, label='Science', ls=':', color='C0')
plot(t_log_ns[:-1]+bin_size, n_log_ns, label='NSO', ls=':', color='C1')
plot(t_log_eng[:-1]+bin_size, n_log_unknown + n_log_eng + n_log_ops, label='Others', ls=':', color='C2')
legend()
grid()
ylim(0,70)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook log usage by proposal group (15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_log_usage_by_group.png')


figure(18, figsize=(8,8))
clf()
ticklabel_format(useOffset=False)
xticks(rotation = 90)
plot(t_head_cl[:-1]+bin_size, n_head_cl + n_head_il + n_head_jl + n_head_pl + n_head_pq + n_head_tl + n_head_zl, label='Science', ls=':', color='C0')
plot(t_head_ns[:-1]+bin_size, n_head_ns, label='NSO', ls=':', color='C1')
plot(t_head_eng[:-1]+bin_size, n_head_unknown + n_head_eng + n_head_ops, label='Others', ls=':', color='C2')
legend()
grid()
ylim(0,30)
xlim(2017.1,2017.5)
ylabel('Number')
xlabel('Time (7-day bin)')
title('Quicklook header usage by proposal group (15 Jan - 1 Jun 2017)')
savefig(output_path + 'quicklook_header_usage_by_group.png')



ip_eng = np.array(list(set(ip[eng_mask])))
ip_eng_mask = np.in1d(ip, ip_eng) & (proposalID != '-')

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

ip_head_count = Counter(ip[(ip_eng_mask==False)&head_file_non_eng_position])
ip_head_address, n_ip_head = np.array(ip_head_count.keys()), np.array(ip_head_count.values())
ip_head_sort_order = np.argsort(n_ip_head)
ip_head_address, n_ip_head = ip_head_address[ip_head_sort_order], n_ip_head[ip_head_sort_order]



figure(2, figsize=(12,8))
clf()
bar(range(len(ip_jpg_address)), n_ip_jpg[::-1], color='C0',log=True, label='jpg')
bar(range(len(ip_fits_address)), n_ip_fits[::-1], color='C2',log=True, alpha=0.8, label='log')
bar(range(len(ip_log_address)), n_ip_log[::-1], color='C1',log=True, alpha=0.6, label='fits')
bar(range(len(ip_head_address)), n_ip_head[::-1], color='C3',log=True, alpha=0.4, label='head')
xlabel('unique ip')
ylabel('Number')
title('Quicklook usage by unique ip (15 Jan - 1 Jun 2017)')
xlim(0,235)
grid()
legend()
savefig(output_path + 'quicklook_usage_by_ip.png')



figure(3, figsize=(12,8))
clf()
hist(access_time_hour[ip_eng_mask==False],bins=24,range=(0,24),color='grey', alpha=0.5, label='total')
hist(access_time_hour[(ip_eng_mask==False)&jpg_file_non_eng_position],bins=24,range=(0,24),color='C0', label='jpg', histtype='step')
hist(access_time_hour[(ip_eng_mask==False)&log_file_non_eng_position],bins=24,range=(0,24),color='C1', label='log', histtype='step')
hist(access_time_hour[(ip_eng_mask==False)&fits_file_non_eng_position],bins=24,range=(0,24),color='C2', label='fits', histtype='step')
hist(access_time_hour[(ip_eng_mask==False)&head_file_non_eng_position],bins=24,range=(0,24),color='C3', label='head', histtype='step')
xlim(0,24)
grid()
title('Hours (UT) when quickloook files opened (15 Jan - 1 Jun 2017)')
xlabel('Hours')
ylabel('Number')
legend()
savefig(output_path + 'quicklook_usage_by_hours.png')

ip_ljmu = np.ones(len(ip))==0

for k, ip_k in enumerate(ip):
    if ip_k[:12] == '150.204.241.':
        ip_ljmu[k] = True


ip_eng_mask_2 = ip_eng_mask | ip_ljmu | NSO_mask

figure(4, figsize=(12,8))
clf()
hist(access_time_hour[ip_eng_mask_2==False],bins=24,range=(0,24),color='grey', alpha=0.5, label='total')
hist(access_time_hour[(ip_eng_mask_2==False)&jpg_file_non_eng_position],bins=24,range=(0,24),color='C0', label='jpg', histtype='step')
hist(access_time_hour[(ip_eng_mask_2==False)&log_file_non_eng_position],bins=24,range=(0,24),color='C1', label='log', histtype='step')
hist(access_time_hour[(ip_eng_mask_2==False)&fits_file_non_eng_position],bins=24,range=(0,24),color='C2', label='fits', histtype='step')
hist(access_time_hour[(ip_eng_mask_2==False)&head_file_non_eng_position],bins=24,range=(0,24),color='C3', label='head', histtype='step')
xlim(0,24)
grid()
title('Hours (UT) when quickloook files opened (ip & NSO filtered, 15 Jan - 1 Jun 2017)')
xlabel('Hours')
ylabel('Number')
legend()
savefig(output_path + 'quicklook_usage_ip_&_NSO_filtered_by_hours.png')

'''
jpg download
'150.204.241.213': 818 - Liverpool (ARI)
'150.204.241.229': 293 - Liverpool (ARI)
'80.229.2.174': 200 - Westminster
'84.127.149.1': 132 - Santander
'90.205.241.34': 132 - Winsford (ARI?)
'94.5.69.40': 118 - Northwich (ARI?)
'82.28.98.22': 100.  - wigan (ARI?)
'209.93.238.114': 100 - Sanderstead, Croydon
'150.204.241.157': 83 - Liverpool (ARI)
'138.246.2.125': 78 - Munich (LMU)
'''






