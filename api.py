from mibs import host_mib, rfc1213_mib, lanmgr_mib
from snmp_api import *
from slack_api import *
import uuid
import statistics

integer = 0
string = 1

trap_list = []
users = []

port = 161
port_trap = 162
ipInReceives_thr = 5000000
ipInHdrErrors_thr = 0
ipInAddrErrors_thr = 0
discard_sw = ['update.exe', 'SkypeBackgroundHost.exe', 'SkypeBridge.exe', 'SkypeApp.exe',
              'Skype.exe', 'MicrosoftEdge.exe', 'MicrosoftEdgeCP.exe', 'MicrosoftEdgesh.exe',
              'OneDrive.exe', 'firefox.exe', 'java.exe']


def add_agent(ip, slack_user):
    if not any(user['slack'] == slack_user for user in users):  # Prevents duplicated slack users in list
        user = {
            "id": uuid.uuid4().hex,
            "ip": ip,
            "slack": slack_user,
            "discard": False
        }
        set_scalar(ip, port, rfc1213_mib.get('system').get('sysName'), user['id'])
        set_scalar(ip, port, rfc1213_mib.get('system').get('sysContact'), user['slack'])
        users.append(user)


def get_discard(ip):
    OS_index = get_scalar(ip, port, host_mib.get('hrSWRun').get('hrSWOSIndex'), string)
    os_cpu_perf = get_table_item(ip, port, host_mib.get('hrSWRunPerf').get('hrSWRunPerfCPU'), OS_index, integer)
    installed_sw = get_table_items(ip, port, host_mib.get('hrSWInstalled').get('hrSWInstalledName'), string)
    run_sw = get_table_items(ip, port, host_mib.get('hrSWRun').get('hrSWRunName'), string)
    percent_os_cpu = round(os_cpu_perf / 24000000, 2)

    return percent_os_cpu, any(installed.startswith('MATLAB') for installed in installed_sw), any(elem in run_sw for elem in discard_sw)


def get_data(ip):
    cpu_cores = get_table_items(ip, port, host_mib.get('hrDevice').get('hrProcessorLoad'), integer)
    storage_type = get_table_items(ip, port, host_mib.get('hrStorage').get('hrStorageType'), string)
    installed_ram = get_scalar(ip, port, host_mib.get('hrStorage').get('hrMemorySize'), int)
    storage_ind = 0
    for t in storage_type:
        if t == '1.3.6.1.2.1.25.2.1.2':  # hrStorageTypes --> hrStorageRam
            storage_ind = storage_type.index(t)
    all_units = (get_table_items(ip, port, host_mib.get('hrStorage').get('hrStorageAllocationUnits'), integer))[
        storage_ind]
    used_units = (get_table_items(ip, port, host_mib.get('hrStorage').get('hrStorageUsed'), integer))[storage_ind]
    used_ram = all_units * used_units

    return cpu_cores, installed_ram, used_ram


def get_static_data(ip):
    cpu_cores, installed_ram, used_ram = get_data(ip)
    descr = get_scalar(ip, port, rfc1213_mib.get('system').get('sysDescr'),
                       string).replace('Hardware: ', '').replace('Software: ', '').split(' - ')
    result = {
        'date': get_scalar(ip, port, host_mib.get('hrSystem').get('hrSystemDate'), string),  # TODO: decode received str
        'hardware': descr[0],
        'os_version': descr[1],
        'uptime': get_scalar(ip, port, rfc1213_mib.get('system').get('sysUpTime'), integer),
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


def trap_server_init():
    trap_server = threading.Thread(target=trap_engine)  # Iniciamos la escucha en el background del servidor de traps.
    trap_server.start()


def trap_config(ip):
    send_trap(ip, port_trap, rfc1213_mib.get('ip').get('ipInReceives'), ipInReceives_thr)
    send_trap(ip, port_trap, rfc1213_mib.get('ip').get('ipInHdrErrors'), ipInHdrErrors_thr)
    send_trap(ip, port_trap, rfc1213_mib.get('ip').get('ipInAddrErrors'), ipInAddrErrors_thr)
