from slack import WebClient
from flask import Flask, request, make_response, Response
import api
import json

app = Flask(__name__)

slack_token = "xoxb-1096471659041-1086356946467-hgDY5l937lAbsnZPmO8C8hm7"
verification_token = "OWsReC2914G1XxtLbhSNYjly"
channel_gestores = 'C012PN83MQC'
channel_usuarios = 'C012AR4E5T8'
client = WebClient(token=slack_token)


def send_init():  # Sends message to admins inviting them to start the test.
    return client.chat_postMessage(
        channel=channel_gestores,
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
        channel=channel_gestores,
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
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning:*AVISO*:  La prueba se esta desarrollando."
                }
            }
        ]
    )


def send_invite_users():
    return client.chat_postMessage(
        channel=channel_usuarios,
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
        channel=channel_usuarios,
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
                        "text": "1.Abra la consola de Window(aplciación cmd)"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "2. Introduzca el comando ipconfig y busque la parte del texto donde pone Adaptador de Lan."
                    }
                },
                {
                    "type": "image",
                    "image_url": "https://www.groovypost.com/wp-content/uploads/2015/10/ipconfig.png",
                    "alt_text": "image1"
                }
            ]
        }
    )


def send_state_subscribed(user):
    return client.chat_postMessage(
        channel=user,
        as_user=True,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":heavy_check_mark: Tu subscripción se ha registrado correctamente."
                }
            }
        ]
    )


@app.route("/slack/actions", methods=["POST"])
def message_actions():
    form_json = json.loads(request.form["payload"])

    if form_json["type"] == "view_submission":
        ip = form_json["view"]["state"]["values"]['address']['ip']['value']
        user_id = form_json['user']['id']
        user = form_json['user']['username']
        api.add_agent(ip, user)
        send_state_subscribed(user_id)
    elif form_json["token"] == verification_token:
        value = form_json["actions"][0]["value"]
        if value == "start_test":  # An admin has started the test.
            admin = form_json['user']['username']
            print('[Slack API] ' + admin + ' has started the test.')
            ts = form_json['container']['message_ts']
            send_state_waiting(ts)
            send_invite_users()
        elif value == "subscribe_test":
            user = form_json['user']['username']
            print('[Slack API] ' + user + ' has subscribed to the test.')
            tg = form_json['trigger_id']
            # TODO: Ask for the ip. Ideas: Open modal, send private message, etc...
            open_modal_for(tg)

    return make_response("", 200)


if __name__ == "__main__":
    send_init()
    app.run(host='0.0.0.0')
