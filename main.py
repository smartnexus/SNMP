from mibs import host_mib, rfc1213_mib, lanmgr_mib
from slack_api import *
from api import *
import time
import json

ip = 'localhost'
port = 161

init_slack()

print('[Main] Starting analysis for', ip + ':' + str(port))
print('[Main] Getting device information...')
print(get_static_data(ip, port))
print('[Main] Gathering device use each 5 secs...')

while 1:
    print(get_variable_data(ip, port))
    time.sleep(5)
