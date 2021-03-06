from slack import WebClient
from flask import Flask, request, make_response
import api
import json
import logging
import datetime
import time

uid = ''
values = {}
client = WebClient()
app = Flask(__name__)


def load_values(config):
    global values
    values = config


def send_init():  # Sends message to admins inviting them to start the test.
    return client.chat_postMessage(
        channel=values['channel_gestores'],
        as_user=True,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Bienvenido al sistema de comprobación de rendimiento para diferentes aplicaciones de software mediante consultas vía SNMP.\n \n Se le recuerda que es necesario *disponer de un agente SNMP* de windows instalado en *todos los equipos* donde se vaya a realizar la prueba y que dichos usuarios *estén dentro* del canal #usuarios.\n\n Cuando desee comenzar la prueba *pulse el botón comenzar*.\n\n"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Comenzar la prueba :heavy_check_mark:",
                            "emoji": True
                        },
                        "value": "start_test"
                    }
                ]
            }
        ]
    )


def send_state_waiting(ts):  # Updates message to admins telling them to app is waiting users.
    return client.chat_update(
        channel=values['channel_gestores'],
        as_user=True,
        ts=ts,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Bienvenido al sistema de comprobación de rendimiento para diferentes aplicaciones de software mediante consultas vía SNMP.\n \n Se le recuerda que es necesario *disponer de un agente SNMP* de windows instalado en *todos los equipos* donde se vaya a realizar la prueba y que dichos usuarios *estén dentro* del canal #usuarios.\n\n Cuando desee comenzar la prueba *pulse el botón comenzar*.\n\n"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":warning:*AVISO*:  La prueba se esta desarrollando."
                    }
                ]
            }
        ]
    )


def send_invite_users():
    return client.chat_postMessage(
        channel=values['channel_usuarios'],
        as_user=True,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning:*AVISO* Un gestor ha comenzado recientemente una prueba. Recuerda que para poder participar tendras que *iniciar previamente* el software y obtener tu *dirección ip*. ¡Haz click en el botón para participar!"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Participar en la prueba :bar_chart:",
                            "emoji": True
                        },
                        "value": "subscribe_test"
                    }
                ]
            }
        ]
    )


def open_modal_for(trigger_id):
    return client.views_open(
        channel=values['channel_usuarios'],
        trigger_id=trigger_id,
        view=
        {
            "type": "modal",
            "callback_id": "modal_identifier",
            "title": {
                "type": "plain_text",
                "text": "Antes de comenzar"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel"
            },
            "blocks": [
                {
                    "type": "divider"
                },
                {
                    "type": "input",
                    "block_id": "address",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "ip"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Introduzca aquí su dirección IP:"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "1. Abra la consola de Windows (aplicación cmd)"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "2. Introduzca el comando ipconfig y busque la parte del texto donde figura Adaptador de Ethernet 'VPN'."
                    }
                },
                {
                    "type": "image",
                    "image_url": "https://i.imgur.com/KWfKF7t.png",
                    "alt_text": "image1"
                }
            ]
        }
    )


def send_state_subscribed(user, result, ip):
    if result:
        return client.chat_postMessage(
            channel=user,
            as_user=True,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Dirección ip recibida:* " + ip + "\n*Identificador de la prueba:* " + uid
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": ":heavy_check_mark: Tu subscripción se ha registrado correctamente."
                        }
                    ]
                }
            ]
        )
    else:
        return client.chat_postMessage(
            channel=user,
            as_user=True,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":disappointed_relieved: Lo sentimos, la prueba ya está en curso."
                    }
                }
            ]
        )


def send_state_final(ts):
    return client.chat_update(
        channel=values['channel_gestores'],
        as_user=True,
        ts=ts,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Bienvenido al sistema de comprobación de rendimiento para diferentes aplicaciones de software mediante consultas vía SNMP.\n \n Se le recuerda que es necesario *disponer de un agente SNMP* de windows instalado en *todos los equipos* donde se vaya a realizar la prueba y que dichos usuarios *estén dentro* del canal #usuarios.\n\n Cuando desee comenzar la prueba *pulse el botón comenzar*.\n\n"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":heavy_check_mark:  La prueba se ha realizado correctamente."
                    }
                ]

            }
        ]
    )


def send_file(file):  # Sends file with test's results
    return client.files_upload(
        token=values["slack_token"],
        channels=values['channel_gestores'],
        file=file,
        filename='test_results.json',
        filetype="json",
        initial_comment="*Fichero con los resultados de la prueba:*"
    )


@app.route("/slack/actions", methods=["POST"])
def message_actions():
    form_json = json.loads(request.form["payload"])
    if form_json["type"] == "view_submission":
        ip = form_json["view"]["state"]["values"]['address']['ip']['value']
        user_id = form_json['user']['id']
        user = form_json['user']['username']
        result = api.add_agent(ip, user)
        send_state_subscribed(user_id, result, ip)
        if result:
            print('[Slack API] ' + user + ' has subscribed to the test.')
    elif form_json["token"] == values['verification_token']:
        value = form_json["actions"][0]["value"]
        if value == "start_test":  # An admin has started the test.
            admin = form_json['user']['username']
            print('[Slack API] ' + admin + ' has started the test.')
            global uid
            ts = form_json['container']['message_ts']
            uid = datetime.datetime.now().strftime('%Y%m%d%H%M')
            api.start_test(uid)
            send_state_waiting(ts)
            send_invite_users()
            while api.running or api.waiting:
                time.sleep(5)
            send_state_final(ts)
        elif value == "subscribe_test":
            tg = form_json['trigger_id']
            open_modal_for(tg)

    return make_response("", 200)


def slack_engine():
    global client
    client = WebClient(token=values['slack_token'])
    send_init()
    print('[Slack API] Http Server listening on 0.0.0.0:5000')
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True
    app.run(host='0.0.0.0')
