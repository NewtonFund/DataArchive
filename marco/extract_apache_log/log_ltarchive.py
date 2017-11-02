import time
import os
import re
import subprocess
from datetime import timedelta
from datetime import datetime


def get_creation_time(path_to_file):
    """
    Get the time of file creation/last modification.
    minimum requirement v2.3
    """
    try:
        ctime = float(os.path.getctime(path_to_file))
    except AttributeError:
        # Can't get creation time, returning last modified time
        ctime = float(os.path.getmtime(path_to_file))
    return ctime


def remove_rows_before_given_time(text, regex, ftime):
    """
    Remove lines in the chuck of log that was added before the given time.
    (minimum requirement v2.3)
    """
    text = text.splitlines()
    new_text = ''
    # populate logs into the dictionary
    for i, line in enumerate(text):
        items = re.match(regex, line).groups()
        t = items[3]
        # the timezone flat %z is broken in strptime
        t_diff = timedelta(hours=int(t[-5:-2]), minutes=int(t[-2:]))
        # strptime is still in time module in python 2.4.X
        item_time = datetime(
            *(time.strptime(t[:-6], "%d/%b/%Y:%H:%M:%S")[0:6])
            ) + t_diff
        item_unix_time = time.mktime(item_time.timetuple())
        if item_unix_time + max_file_age> ftime:
            new_text += line + '\n'
    return new_text


logs_path = "/var/log/httpd/"
logs_path = "/home/eng/log_mcl_test/"
output_path = "/home/eng/archive_log/"
base_dir = "/data/archive/scratch/"

# get current time
current_time = time.time()

# oldest file to process: number of system seconds before current_time
# 1 day: 86400.
# 7 days: 604800.
# 365 days: 31536000.
max_file_age = 6048000.

# set output file
output_file = output_path + "archive_log.txt"
output_file = logs_path + "archive_log.txt"

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
regex_access_log = '([(\d\.)]+) (.*) (.*) \[(.*?)\]' +\
                   ' "(.*?)" (\d+) (.*) "(.*?)" "(.*?)"'

# regular expression to split the [unique ID]_prog.html text
regex_prog_html = '(.*) (.*) (.*) (.*) \[(.*?)\]\<BR\>'

search_key_tarball = "\"GET /cgi-bin/createsearchtarball.cgi?"
search_key_download = "\"GET /data/archive/scratch/"

# Only goes through the access_logs
for i in range(2):
    if not i:
        log_path = logs_path + 'access_log'
    else:
        log_path = logs_path + 'access_log.' + str(i)
    if os.path.isfile(log_path):
        # if running the script for the first time, set file_ctime to 0
        file_ctime = get_creation_time(log_path)
        if current_time - file_ctime < max_file_age:
            # grep lines with the search key and pipe directly to memory
            if not i:
                access_log_lines = subprocess.Popen(
                    "egrep \'" + search_key_tarball + "|" +
                     search_key_download + "\' " + log_path, shell=True,
                    stdout=subprocess.PIPE).communicate()[0]
            else:
                if current_time - file_ctime < max_file_age:
                    access_log_lines += subprocess.Popen(
                        "egrep \'" + search_key_tarball + "|" +
                        search_key_download + "\' " + log_path,
                        shell=True, stdout=subprocess.PIPE).communicate()[0]
                else:
                    pass
        else:
            pass
    else:
        pass


access_log_lines = remove_rows_before_given_time(
                       access_log_lines, regex_access_log, current_time
                       )

access_log_lines = access_log_lines.splitlines()

# generate and loop through file list in the archive folder
file_list = os.listdir(base_dir)

output = []

for uniqueID in file_list:
    # check if the uniqueID is numeric, if not ignore folder
    if not uniqueID.isdigit():
        continue
    # get log file path
    uniqueID_html_file = base_dir + uniqueID + "/" + uniqueID + "_prog.html"
    #uniqueID_html_file = base_dir + uniqueID + "_prog.html"
    uniqueID_txt_file = base_dir + uniqueID + "/cat" + uniqueID + ".txt"
    # get file creation/last modification time
    creation_time = get_creation_time(uniqueID_html_file)
    # if file is older than 1 week, ignore
    if current_time - creation_time > max_file_age:
        continue
    # open the html file
    if not os.path.isfile(uniqueID_html_file):
        continue
    f_temp = open(uniqueID_html_file, 'r')
    html_lines = f_temp.readlines()
    f_temp.close()
    if len(html_lines) < 13:
        continue
    # get the number of queried fields
    number_of_items = int(html_lines[12].split()[1])
    d = {}
    for line in html_lines[13:13 + number_of_items]:
        num, tab1, key, tab2, val = re.match(regex_prog_html, line).groups()
        val = val.strip()
        if (val != ''):
            d[key] = val
    # count the number of lines in the txt file (i.e. number of search result)
    if os.path.isfile(uniqueID_txt_file):
        number_of_results = subprocess.Popen(
                            "wc -l < " + uniqueID_txt_file, shell=True,
                            stdout=subprocess.PIPE).communicate()[0][:-1]
        d['number_of_results'] = number_of_results - 1
    else:
        number_of_results = '0'
        d['number_of_results'] = number_of_results
        continue
    # regular expression for tarball creation + reduced/raw + pub/priv
    regex_tc_reduced_pub = ".*\"GET /cgi-bin/createsearchtarball.*" +\
                           uniqueID + "&.*&reduced&pub.*"
    regex_tc_reduced_priv = ".*\"GET /cgi-bin/createsearchtarball.*" +\
                            uniqueID + "&.*&reduced&priv.*"
    regex_tc_raw_pub = ".*\"GET /cgi-bin/createsearchtarball.*" +\
                       uniqueID + "&.*&raw&pub.*"
    regex_tc_raw_priv = ".*\"GET /cgi-bin/createsearchtarball.*" +\
                        uniqueID + "&.*&raw&priv.*"
    # search key for tarball download + pub/priv
    regex_td_pub = ".*\"GET /data/archive/scratch/" + uniqueID +\
                   "/.*/Pub.*.t.*"
    regex_td_priv = ".*\"GET /data/archive/scratch/" + uniqueID +\
                    "/.*/Priv.*.t.*"
    # search key for jpg/fits download
    regex_jpg_d_pub = ".*GET.*" + uniqueID + "/.*/Pub/.*\.jpg.*"
    regex_jpg_d_priv = ".*GET.*" + uniqueID + "/.*/Priv/.*\.jpg.*"
    regex_fits_d_pub = ".*GET.*" + uniqueID + "/.*/Pub/.*\.fits.*"
    regex_fits_d_priv = ".*GET.*" + uniqueID + "/.*/Priv/.*\.fits.*"
    for line in access_log_lines:
        if re.match(regex_tc_reduced_pub, line) != None:
            if 'tarball_reduced_public' in d:
                d['tarball_reduced_public'] += 1
            else:
                d['tarball_reduced_public'] = 1
            continue
        if re.match(regex_tc_reduced_priv, line) != None:
            if 'tarball_reduced_private' in d:
                d['tarball_reduced_private'] += 1
            else:
                d['tarball_reduced_private'] = 1
            continue
        if re.match(regex_tc_raw_pub, line) != None:
            if 'tarball_raw_public' in d:
                d['tarball_raw_public'] += 1
            else:
                d['tarball_raw_public'] = 1
            continue
        if re.match(regex_tc_raw_priv, line) != None:
            if 'tarball_raw_private' in d:
                d['tarball_raw_private'] += 1
            else:
                d['tarball_raw_private'] = 1
            continue
        if re.match(regex_td_pub, line) != None:
            if 'tarball_download_public' in d:
                d['tarball_download_public'] += 1
            else:
                d['tarball_download_public'] = 1
            continue
        if re.match(regex_td_priv, line) != None:
            if 'tarball_download_private' in d:
                d['tarball_download_private'] += 1
            else:
                d['tarball_download_private'] = 1
            continue
        if re.match(regex_jpg_d_pub, line) != None:
            if 'jpg_download_public' in d:
                d['jpg_download_public'] += 1
            else:
                d['jpg_download_public'] = 1
            continue
        if re.match(regex_jpg_d_priv, line) != None:
            if 'jpg_download_private' in d:
                d['jpg_download_private'] += 1
            else:
                d['jpg_download_private'] = 1
            continue
        if re.match(regex_fits_d_pub, line) != None:
            if 'fits_download_public' in d:
                d['fits_download_public'] += 1
            else:
                d['fits_download_public'] = 1
            continue
        if re.match(regex_fits_d_priv, line) != None:
            if 'fits_download_private' in d:
                d['fits_download_private'] += 1
            else:
                d['fits_download_private'] = 1
            continue
    output.append(d)


for item in output:
    try:
        item['number_of_results']
    except:
        pass


# generate empty output file if not exist
if not os.path.isfile(output_file):
    subprocess.call("touch " + output_file, shell=True)

# open output file
f = open(output_file, 'rw+')
f.write(output)
f.close()
