from mibs import host_mib, rfc1213_mib, lanmgr_mib
from slack_api import *
from api import *
import time
import json

port = 161
port_trap = 162
test_time = 60  # duracion de la prueba
sample_time = 5
count = 0  # variable que controlará el tiempo de duracion de la prueba
discard = False
# Umbrales
cpu_thr = 2
ram_thr = 4
uptime_thr = 43200000


# TODO: (1)Iniciar el slack y que me devuelva la lista de ips (list_ip) de todos los usuarios que realizan la prueba. (¿y la lisa de slack_users?)

#init_slack()
list_ip = ['localhost']

# TODO: generar un identificador único para cada usuario y haciendo uso de la función addAgent(user, uuid, ip)
# addAgent(user, uuid, ip)

for ip in list_ip:
    count = 0
    discard = False
    n_user = list_ip.index(ip)
    trap_config(ip, port_trap)       #Configuro traps

    print('[Main] Starting analysis for', ip + ':' + str(port))

    print('[Main] Getting device information...')
    static_data = get_static_data(ip, port)
    print(get_static_data(ip, port))
    # TODO: Comprobar si los datos pueden suponer el descarte de la prueba
    if static_data['cpu_cores'] < cpu_thr:
        discard = True
        # TODO: Añadir a arbol json, rama discard, la variable cpu_cores
        # list[n_user].['discard'].append(static_data['cpu_cores'])
        print('[DISCARD] cpu_cores < ', cpu_thr)

    if static_data['installed_ram'] < ram_thr:
        discard = True
        # TODO: Añadir a arbol json, rama discard, la variable installed_ram
        # list[n_user].['discard'].append(static_data['installed_ram'])
        print('[DISCARD] installed_ram < ', ram_thr)

    if static_data['uptime'] > uptime_thr:
        discard = True
        # TODO: Añadir a arbol json, rama discard, la variable uptime
        # list[n_user].['discard'].append(static_data['uptime'])
        print('[DISCARD] uptime >', uptime_thr)

    # TODO: Comprobacion de processorLoads


    # TODO: añadir los datos estaticos al arbol json (en lo comentado he puesto arbol inventado de ejemplo)
    # list[n_user].['date'].append(static_data['date'])
    # list[n_user].['hardware'].append(static_data['hardware'])
    # list[n_user].['os_version'].append(static_data['os_version'])
    # list[n_user].['uptime'].append(static_data['uptime'])
    # list[n_user].['cpu_cores'].append(static_data['cpu_cores'])
    # list[n_user].['installed_ram'].append(static_data['installed_ram'])

    print('[Main] Gathering device use each 5 secs...')
    while count < test_time:
        variable_data = get_variable_data(ip, port)
        print(get_variable_data(ip, port))
        # TODO: compobar si este usuario deberia ser descartado para la prueba
        if trap_check(ip):
            discard = True
            # TODO: Añadir a arbol json, rama discard, trap
            print('[DISCARD] Trap received')


        # TODO: añadir los datos estaticos al arbol json (en lo comentado he puesto arbol inventado de ejemplo
        # list[n_user].['used_cpu'].append(variable_data['used_cpu'])
        # list[n_user].['used_ram'].append(variable_data['used_ram'])
        count += sample_time
        time.sleep(sample_time)

# TODO: Comprobar si la prueba ha sido valida
if not discard:
    print('Prueba realizada correctamente')
else:
    print('Alguna variable no cumple los umbrales, descartamos prueba')

# TODO: Enviar todos los datos recogidos (agol json) a slack con la función xxxAngelitorb99xxx.
