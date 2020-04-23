from mibs import host_mib, rfc1213_mib, lanmgr_mib
from snmp_api import *
import statistics

integer = 0
string = 1


def get_data(ip, port):
    cpu_cores = get_table_items(ip, port, host_mib.get('hrDevice').get('hrProcessorTable'), integer)
    storage_type = get_table_items(ip, port, host_mib.get('hrStorage').get('hrStorageType'), string)
    installed_ram = get_scalar(ip, port, host_mib.get('hrStorage').get('hrMemorySize'), int)
    storage_ind = 0
    for t in storage_type:
        if t == '1.3.6.1.2.1.25.2.1.2':  # hrStorageTypes --> hrStorageRam
            storage_ind = storage_type.index(t)
    all_units = (get_table_items(ip, port, host_mib.get('hrStorage').get('hrStorageAllocationUnits'), int))[storage_ind]
    used_units = (get_table_items(ip, port, host_mib.get('hrStorage').get('hrStorageUsed'), int))[storage_ind]
    used_ram = all_units*used_units

    return cpu_cores, installed_ram, used_ram


def get_static_data(ip, port):
    cpu_cores, installed_ram, used_ram = get_data(ip, port)
    descr = get_scalar(ip, port, rfc1213_mib.get('system').get('sysDescr'),
                       string).replace('Hardware: ', '').replace('Software: ', '').split(' - ')
    result = {
        # 'date': get_scalar(ip, port, host_mib.get('hrSystem').get('hrSystemDate'), string) TODO: decode received str
        'hardware': descr[0],
        'os_version': descr[1],
        'uptime': get_scalar(ip, port, rfc1213_mib.get('system').get('sysUpTime'), integer),
        'cpu_cores': len(cpu_cores),
        'installed_ram': installed_ram
    }
    return result


def get_variable_data(ip, port):
    cpu_cores, installed_ram, used_ram = get_data(ip, port)
    result = {
        # 'date': get_scalar(ip, port, host_mib.get('hrSystem').get('hrSystemDate'), string) TODO: decode received str
        'used_cpu': statistics.mean(cpu_cores)/100,
        'used_ram': round(used_ram/(installed_ram * 1000), 2)
    }
    return result
