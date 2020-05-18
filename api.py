from mibs import host_mib, rfc1213_mib
from snmp_api import *
from slack_api import *
import uuid
import statistics
import json

integer = 0
string = 1
running = False
waiting = False

test_id = ''
thr = {}
test = {}
users = []


def start_test(number):
    global test_id, waiting
    test_id = number
    waiting = True


def export(data, file):
    print('[Main] Exporting json file with results...')
    with open('exports/' + test_id + '-' + file, 'w') as outfile:
        json.dump(data, outfile)
        print('[Main] Exported "exports/' + test_id + '-' + file + '"!')


def to_slack():
    file = "exports/" + test_id + "-results.json"
    # send_state_final(ts_admin) Not working because we dont have correct ts.
    send_file(file)


def load_config():
    print('[Main] Importing configuration...')
    global thr, test
    with open('config/thresholds.json') as thr_config:
        thr = json.load(thr_config)
        print('[Main] Loaded "config/thresholds.json"!')
    with open('config/test.json') as main_config:
        test = json.load(main_config)
        print('[Main] Loaded "config/test.json"!')
    with open('config/slack.json') as slack_config:
        slack = json.load(slack_config)
        print('[Main] Loaded "config/slack.json"!')
        load_values(slack)
    return test, thr


def add_agent(ip, slack_user):
    if not any(user['slack'] == slack_user for user in users) and waiting:  # Prevents duplicated slack users in list
        user = {
            "id": uuid.uuid4().hex,
            "ip": ip,
            "slack": slack_user,
            "discard": False
        }
        set_scalar(ip, test['port'], rfc1213_mib.get('system').get('sysName'), user['id'])
        set_scalar(ip, test['port'], rfc1213_mib.get('system').get('sysContact'), user['slack'])
        users.append(user)
    return not running


def get_discard(ip):
    OS_index = get_scalar(ip, test['port'], host_mib.get('hrSWRun').get('hrSWOSIndex'), string)
    os_cpu_perf = get_table_item(ip, test['port'], host_mib.get('hrSWRunPerf').get('hrSWRunPerfCPU'), OS_index, integer)
    installed_sw = get_table_items(ip, test['port'], host_mib.get('hrSWInstalled').get('hrSWInstalledName'), string)
    run_sw = get_table_items(ip, test['port'], host_mib.get('hrSWRun').get('hrSWRunName'), string)
    percent_os_cpu = round(os_cpu_perf / 24000000, 2)

    return percent_os_cpu, any(installed.startswith('MATLAB') for installed in installed_sw), any(elem in run_sw for elem in thr['discard_sw'])


def get_data(ip):
    cpu_cores = get_table_items(ip, test['port'], host_mib.get('hrDevice').get('hrProcessorLoad'), integer)
    storage_type = get_table_items(ip, test['port'], host_mib.get('hrStorage').get('hrStorageType'), string)
    installed_ram = get_scalar(ip, test['port'], host_mib.get('hrStorage').get('hrMemorySize'), int)
    storage_ind = 0
    for t in storage_type:
        if t == '1.3.6.1.2.1.25.2.1.2':  # hrStorageTypes --> hrStorageRam
            storage_ind = storage_type.index(t)
    all_units = (get_table_items(ip, test['port'], host_mib.get('hrStorage').get('hrStorageAllocationUnits'), integer))[
        storage_ind]
    used_units = (get_table_items(ip, test['port'], host_mib.get('hrStorage').get('hrStorageUsed'), integer))[storage_ind]
    used_ram = all_units * used_units

    return cpu_cores, installed_ram, used_ram


def get_static_data(ip):
    cpu_cores, installed_ram, used_ram = get_data(ip)
    descr = get_scalar(ip, test['port'], rfc1213_mib.get('system').get('sysDescr'),
                       string).replace('Hardware: ', '').replace('Software: ', '').split(' - ')
    result = {
        'date': get_scalar(ip, test['port'], host_mib.get('hrSystem').get('hrSystemDate'), string),  # TODO: decode received str
        'hardware': descr[0],
        'os_version': descr[1],
        'uptime': get_scalar(ip, test['port'], rfc1213_mib.get('system').get('sysUpTime'), integer),
        'cpu_cores': len(cpu_cores),
        'installed_ram': installed_ram
    }
    return result


def get_variable_data(ip):
    cpu_cores, installed_ram, used_ram = get_data(ip)
    result = {
        'used_cpu': statistics.mean(cpu_cores) / 100,
        'used_ram': round(used_ram / (installed_ram * 1000), 2)
    }
    return result


def trap_check(ip):
    check = False
    if ip in trap_list:
        check = True
    return check


def slack_server_init():
    slack_server = threading.Thread(target=slack_engine)
    slack_server.start()


def trap_server_init():
    trap_server = threading.Thread(target=trap_engine)
    trap_server.start()


def trap_config(ip):
    send_trap(ip, test['port_trap'], rfc1213_mib.get('ip').get('ipInReceives'), thr['ipInReceives_thr'])
    send_trap(ip, test['port_trap'], rfc1213_mib.get('ip').get('ipInHdrErrors'), thr['ipInHdrErrors_thr'])
    send_trap(ip, test['port_trap'], rfc1213_mib.get('ip').get('ipInAddrErrors'), thr['ipInAddrErrors_thr'])
