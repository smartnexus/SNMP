from pysnmp.hlapi import *
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import threading

listening_ip = '127.0.0.1'
listening_port = 162
trap_list = []


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
    errorIndication, errorStatus, errorIndex, varBinds = next(
        sendNotification(SnmpEngine(),
                         CommunityData('public'),
                         UdpTransportTarget((ip, int(port))),
                         ContextData(),
                         'trap',
                         [ObjectType(ObjectIdentity(oid), Integer(value))]))
    if errorIndication or errorIndex or errorIndex:
        print('[SNMP API] Error sending trap for:' + oid)
    else:
        return True


# function for receiving trap notifications

def trap_engine():
    snmpEngine = engine.SnmpEngine()
    print('[SNMP API] Trap Server listening on ' + listening_ip + ":" + str(listening_port))
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((listening_ip, listening_port))
    )
    config.addV1System(snmpEngine, 'my-area', 'public')

    def callback(eng, ref, eng_id, name, var_binds, cb_ctx):
        sender_domain, sender_address = eng.msgAndPduDsp.getTransportInfo(ref)
        if not trap_list.__contains__(sender_address[0]):
            trap_list.append(sender_address[0])

    ntfrcv.NotificationReceiver(snmpEngine, callback)
    snmpEngine.transportDispatcher.jobStarted(1)

    try:
        snmpEngine.transportDispatcher.runDispatcher()
    finally:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise
