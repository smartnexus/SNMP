import api
import time

test, thr = api.load_config()
api.trap_server_init()
api.slack_server_init()
while len(api.users) < test['min_users']:
    time.sleep(5)
api.running = True
uid = api.uid
print('[Main] Starting the test... (UID: ' + uid + ')')
for user in api.users:
    ip = user['ip']
    domain = user['slack'] + '@' + user['ip']
    user['discard'] = []
    discard = False
    api.trap_config(ip)

    print('[Main] Starting analysis for', domain)

    print('[Main] Getting device information for ' + domain + '...')

    static_data = api.get_static_data(ip)

    if static_data['cpu_cores'] < thr['cpu_thr']:
        discard = True
        user['discard'].append({"cpu_cores": static_data['cpu_cores']})
        print('[DISCARD] ' + domain + ' has cpu_cores < ', thr['cpu_thr'])

    if static_data['installed_ram'] < thr['ram_thr']:
        discard = True
        user['discard'].append({"installed_ram": static_data['installed_ram']})
        print('[DISCARD] ' + domain + ' installed_ram < ', thr['ram_thr'])

    if static_data['uptime'] > thr['uptime_thr']:
        discard = True
        user['discard'].append({"uptime": static_data['uptime']})
        print('[DISCARD] ' + domain + ' uptime >', thr['uptime_thr'])

    os_processor_load, matlab, os_installed = api.get_discard(ip)

    if os_processor_load > thr['os_max_processor_load']:
        discard = True
        user['discard'].append({"os_processor_load": os_processor_load})
        print('[DISCARD] ' + domain + ' os_processor_load >', thr['os_max_processor_load'])
    if not matlab:
        discard = True
        user['discard'].append({"matlab_installed": matlab})
        print('[DISCARD] ' + domain + ' matlab not installed')

    if os_installed:
        discard = True
        user['discard'].append({"malware_installed": os_installed})
        print('[DISCARD] ' + domain + ' malware installed')

    user['test_date'] = static_data['date']
    user['hardware'] = static_data['hardware']
    user['os_version'] = static_data['os_version']
    user['uptime'] = static_data['uptime']
    user['cpu_cores'] = static_data['cpu_cores']
    user['installed_ram'] = static_data['installed_ram']
    user['data'] = {
        'used_cpu': [],
        'used_ram': []
    }

    if discard:
        print('[Main] Discarding test for user:', user['slack'])

print('[Main] Gathering device use each ' + str(test['sample_time']) + ' secs...')
count = 0
trap = []
while count < test['test_time']:
    for user in api.users:
        ip = user['ip']
        domain = user['slack'] + '@' + user['ip']
        variable_data = api.get_variable_data(ip)
        if api.trap_check(ip):
            # TODO: Configurar bien para que se guarde y notifique solo una vez.
            discard = True
            if any(key == domain for key in trap):
                print('[DISCARD] Trap received from ' + domain)
                user["discard"].append({"trap_received": True})
                trap.append(domain)

        user["data"]["used_cpu"].append(variable_data["used_cpu"])
        user["data"]["used_ram"].append(variable_data["used_ram"])
    count += test['sample_time']
    time.sleep(test['sample_time'])

api.export(api.users, 'results.json')
#TODO: Llamar funcion de slack para subir el archivo al canal de gestores
