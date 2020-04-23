from pysnmp.hlapi import *


#
# Functions to allow easily use GET and SET operations from SNMP in rest of code.
#


def get_scalar(ip, port, oid, return_type):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public'),
               UdpTransportTarget((ip, int(port))),
               ContextData(),
               ObjectType(oid))
    )

    if errorIndication or errorIndex or errorIndex:
        print('[SNMP API] Error getting specified value:' + str(oid))
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

        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break
        else:
            for varBind in varBinds:
                item = str(varBind.__getitem__(1)) if return_type == 1 else int(varBind.__getitem__(1))
                result.append(item)
    return result
