from pysnmp.hlapi import *

#
# SMIs storage to avoid using OIDs in entire code.
#

host_mib = {
    'hrSystem': {
        'hrSystemDate': '1.3.6.1.2.1.25.1.2.0',
        'hrSystemNumUsers': '1.3.6.1.2.1.25.1.5.0',
        'hrSystemProcesses': '1.3.6.1.2.1.25.1.6.0'
    },
    'hrStorage': {
        'hrMemorySize': '1.3.6.1.2.1.25.2.2.0',
        # Table data using 4th column: StorageTable
        # Hay que mirar que columnas son idex, hay que implementarlas obligatoriamente
        'hrStorageType': '1.3.6.1.2.1.25.2.3.1.2',
        'hrStorageAllocationUnits': '1.3.6.1.2.1.25.2.3.1.4',
        'hrStorageSize': '1.3.6.1.2.1.25.2.3.1.5',
        'hrStorageUsed': '1.3.6.1.2.1.25.2.3.1.6'
    },
    'hrDevice': {
        # This oid is for processorLoad
        'hrProcessorLoad': '1.3.6.1.2.1.25.3.3.1.2',
    },
    # Remaining OIDs objects are tables.
    'hrSWRun': {
        'hrSWOSIndex': '1.3.6.1.2.1.25.4.1.0',
        'hrSWRunName': '1.3.6.1.2.1.25.4.2.1.2'
    },
    'hrSWRunPerf': {
        'hrSWRunPerfCPU': '1.3.6.1.2.1.25.5.1.1.1',
        'hrSWRunPerfMem': '1.3.6.1.2.1.25.5.1.1.2'
    },
    'hrSWInstalled': {
        'hrSWInstalledName': '1.3.6.1.2.1.25.6.3.1.2'
    }
}
lanmgr_mib = {
    'domain': {
        'domPrimaryDomain': '1.3.6.1.4.1.77.1.4.1.0'
    }
}

rfc1213_mib = {
    'system': {
        'sysDescr': '1.3.6.1.2.1.1.1.0',
        'sysUpTime': '1.3.6.1.2.1.1.3.0',
        'sysContact': '1.3.6.1.2.1.1.4.0',
        'sysName': '1.3.6.1.2.1.1.5.0',
    },
    'ip': {
        'ipInReceives': '1.3.6.1.2.1.4.3.0',
        'ipInHdrErrors': '1.3.6.1.2.1.4.4.0',
        'ipInAddrErrors': '1.3.6.1.2.1.4.5.0'
    }
}