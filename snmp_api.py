from pysnmp.hlapi import *
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import asyncio

trap_list = ['']


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

    if errorIndication or errorStatus or errorIndex:
        print('[SNMP API] Error getting specified value:' + column_oid)
    else:
        # Returning only one value of those found
        return str(varBinds[0].__getitem__(1)) if return_type == 1 else int(varBinds[0].__getitem__(1))


def send_trap(ip, port, oid, value):
    errorIndication, errorStatus, errorIndex, varBinds = next(sendNotification(SnmpEngine(),
                                                                               CommunityData('public'),
                                                                               UdpTransportTarget((ip, int(port))),
                                                                               ContextData(),
                                                                               'trap',
                                                                               [ObjectType(ObjectIdentity(oid),
                                                                                           Integer(value))]))
    if errorIndication or errorIndex or errorIndex:
        print('[SNMP API] Error sending trap for:' + oid)
    else:
        return True


# function for receiving trap notifications
# TODO probarlo
def callback_trap(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    sender_domain, sender_address = snmpEngine.msgAndPduDsp.getTransportInfo(stateReference)
    # print de comprobacion
    print('Notification from ' + sender_address)
    cbCtx.append(sender_address)


def trap_engine(ip, port):
    loop = asyncio.get_event_loop()
    snmpEngine = engine.SnmpEngine()
    print('TrapServer listening on' + ip + ":" + port)
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((ip, port))
    )
    config.addV1System(snmpEngine, 'my-area', 'public')
    global_list = ntfrcv.NotificationReceiver(snmpEngine, callback_trap, cbCtx=trap_list)
    return global_list
    loop.run_forever()


if __name__ == "__main__":
    send_trap("192.168.1.111", 162, '1.3.6.1.2.1.4.3.0', 31060000)
