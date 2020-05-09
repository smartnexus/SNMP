from mibs import host_mib, rfc1213_mib, lanmgr_mib
from slack_api import *
from api import *
import time

port = 161
port_trap = 162
test_time = 60  # duracion de la prueba
sample_time = 5

# UMBRALES
cpu_thr = 2
ram_thr = 4
uptime_thr = 43200000
os_max_processor_load = 0.05
ipInReceives_thr = 5000000
ipInHdrErrors_thr = 0
ipInAddrErrors_thr = 0
discard_sw = ['update.exe', 'SkypeBackgroundHost.exe', 'SkypeBridge.exe', 'SkypeApp.exe',
              'Skype.exe', 'MicrosoftEdge.exe', 'MicrosoftEdgeCP.exe', 'MicrosoftEdgesh.exe',
              'OneDrive.exe', 'firefox.exe', 'java.exe']

# TODO: (1)Iniciar el slack y que me devuelva la lista de ips (list_ip) de todos los usuarios que realizan la prueba. (¿y la lisa de slack_users?)

trap_server_init()
slack_server_init()
while len(users) < 1:
    time.sleep(5)
api.running = True
trap_server_init()

for user in users:
    ip = user['ip']
    domain = user['slack'] + '@' + user['ip']
    user['discard'] = []
    discard = False
    trap_config(ip)

    print('[Main] Starting analysis for', domain)

    print('[Main] Getting device information for ' + domain + '...')

    static_data = get_static_data(ip)

    if static_data['cpu_cores'] < cpu_thr:
        discard = True
        user['discard'].append({"cpu_cores": static_data['cpu_cores']})
        print('[DISCARD] ' + domain + ' has cpu_cores < ', cpu_thr)

    if static_data['installed_ram'] < ram_thr:
        discard = True
        user['discard'].append({"installed_ram": static_data['installed_ram']})
        print('[DISCARD] ' + domain + ' installed_ram < ', ram_thr)

    if static_data['uptime'] > uptime_thr:
        discard = True
        user['discard'].append({"uptime": static_data['uptime']})
        print('[DISCARD] ' + domain + ' uptime >', uptime_thr)

    os_processor_load, matlab, os_installed = get_discard(ip)

    if os_processor_load > os_max_processor_load:
        discard = True
        user['discard'].append({"os_processor_load": os_processor_load})
        print('[DISCARD] ' + domain + ' os_processor_load >', uptime_thr)
    if not matlab:
        discard = True
        user['discard'].append({"matlab_installed": matlab})
        print('[DISCARD] ' + domain + ' matlab not installed')

    if os_installed:
        discard = True
        user['discard'].append({"malware_installed": os_installed})
        print('[DISCARD] ' + domain + ' malware installed')

    user['test_date'] = static_data['date']
    user['hardware'] = static_data['hardware']
    user['os_version'] = static_data['os_version']
    user['uptime'] = static_data['uptime']
    user['cpu_cores'] = static_data['cpu_cores']
    user['installed_ram'] = static_data['installed_ram']
    user['data'] = {
        'used_cpu': [],
        'used_ram': []
    }

    if discard:
        print('[Main] Discarding test for user:', user['slack'])

print('[Main] Gathering device use each ' + str(sample_time) + ' secs...')
count = 0
while count < test_time:
    for user in users:
        ip = user['ip']
        domain = user['slack'] + '@' + user['ip']
        variable_data = get_variable_data(ip)
        if trap_check(ip):
            discard = True
            print('[DISCARD] Trap received from ' + domain)
            user["discard"].append({"trap_received": True})

        user["data"]["used_cpu"].append(variable_data["used_cpu"])
        user["data"]["used_ram"].append(variable_data["used_ram"])
    count += sample_time
    time.sleep(sample_time)

print(users)
