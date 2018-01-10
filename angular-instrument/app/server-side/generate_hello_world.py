import time
import sys

time_stamp = time.strftime('%X %x %Z')

text_file = open("hello_world_" + str(int(time.time())) + ".txt", 'w+')
text_file.write(str(time_stamp))
text_file.close()

print("hello_world_" + str(int(time.time())) + ".txt")
sys.stdout.flush()
