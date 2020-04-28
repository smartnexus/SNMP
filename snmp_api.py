from pysnmp.hlapi import *


#
# Functions to allow easily use GET and SET operations from SNMP in rest of code.
#


def set_scalar(ip, port, oid, value):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        setCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((ip, int(port))),
               ContextData(),
               ObjectType(ObjectIdentity(oid),
                          OctetString(value)))
    )

    if errorIndication or errorIndex or errorIndex:
        print('[SNMP API] Error setting specified value:' + oid)
    else:
        return str(varBinds[0].__getitem__(1)) == value


def get_scalar(ip, port, oid, return_type):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((ip, int(port))),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication or errorIndex or errorIndex:
        print('[SNMP API] Error getting specified value:' + oid)
    else:
        # Returning only one value of those found
        return str(varBinds[0].__getitem__(1)) if return_type == 1 else int(varBinds[0].__getitem__(1))


# RETURN_TYPE --> 0 when expected integer and 1 when expected string.
def get_table_items(ip, port, column_oid, return_type):
    result = []
    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(SnmpEngine(),
                              CommunityData('public'),
                              UdpTransportTarget((ip, int(port))),
                              ContextData(),
                              ObjectType(ObjectIdentity(column_oid)),
                              lexicographicMode=False):

        if errorIndication or errorIndex or errorIndex:
            print('[SNMP API] Error getting specified value:' + column_oid)
        else:
            for varBind in varBinds:
                item = str(varBind.__getitem__(1)) if return_type == 1 else int(varBind.__getitem__(1))
                result.append(item)
    return result


def get_table_item(ip, port, column_oid, index, return_type):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((ip, int(port))),
               ContextData(),
               ObjectType(ObjectIdentity(column_oid + '.' + index)))
    )

    if errorIndication or errorIndex or errorIndex:
        print('[SNMP API] Error getting specified value:' + column_oid)
    else:
        # Returning only one value of those found
        return str(varBinds[0].__getitem__(1)) if return_type == 1 else int(varBinds[0].__getitem__(1))

"""
    #No se como si indican los valores umbrales en el agente.
    #No se muy bien que poner el return
def send_trap(ip, port, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(SnmpEngine(),
                         CommunityData('public'),
                         UdpTransportTarget((ip, int(port))),
                         ContextData(),
                         'trap',
                         NotificationType(ObjectIdentity(oid))
                         )
    )
    if errorIndication or errorIndex or errorIndex:
        print('[SNMP API] Error trap:' + oid)
    else:
        return .......

"""