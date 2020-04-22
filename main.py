from pysnmp.hlapi import *

host_mib = {
    'hrSystem': {
        'hrSystemDate': ObjectIdentity('1.3.6.1.2.1.25.1.2.0'),
        'hrSystemNumUsers': ObjectIdentity('1.3.6.1.2.1.25.1.5.0'),
        'hrSystemProcesses': ObjectIdentity('1.3.6.1.2.1.25.1.6.0')
    },
    'hrStorage': {
        'hrMemorySize': ObjectIdentity('1.3.6.1.2.1.25.2.2.0'),
        # Table data using 4th column
        'hrStorageAllocationUnits': ObjectIdentity('1.3.6.1.2.1.25.2.3.1.4.4'),
        'hrStorageSize': ObjectIdentity('1.3.6.1.2.1.25.2.3.1.5.4'),
        'hrStorageUsed': ObjectIdentity('1.3.6.1.2.1.25.2.3.1.6.4')
    },
    'hrDevice': {
        # TODO: Get all rows to match all specific core cases. This is just column's OID.
        'hrProcessorTable': ObjectIdentity('1.3.6.1.2.1.25.3.3.1.2')
    },
    # Remaining OIDs objects are tables.
    'hrSWRun': {
        'hrSWRunTable': ObjectIdentity('1.3.6.1.2.1.25.4.2')
    },
    'hrSWRunPerf': {
        'hrSWRunPerfTable': ObjectIdentity('1.3.6.1.2.1.25.5.1')
    },
    'hrSWInstalled': {
        'hrSWInstalledTable': ObjectIdentity('1.3.6.1.2.1.25.6.3')
    }
}

lanmgr_mib = {
    'domain': {
        'domPrimaryDomain': ObjectIdentity('1.3.6.1.4.1.77.1.4.1.0')
    }
}

rfc1213_mib = {
    'system': {
        'sysDescr': ObjectIdentity('1.3.6.1.2.1.1.1.0'),
        'sysUpTime': ObjectIdentity('1.3.6.1.2.1.1.3.0'),
        'sysContact': ObjectIdentity('1.3.6.1.2.1.1.4.0')
    },
    'ip': {
        'ipInReceives': ObjectIdentity('1.3.6.1.2.1.4.3.0'),
        'ipInHdrErrors': ObjectIdentity('1.3.6.1.2.1.4.4.0'),
        'ipInAddrErrors': ObjectIdentity('1.3.6.1.2.1.4.5.0')
    }
}


def get_scalar(oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget(('localhost', 161)),
               ContextData(),
               ObjectType(oid))
    )

    if errorIndication or errorIndex or errorIndex:
        print('Error')
    else:
        return varBinds

