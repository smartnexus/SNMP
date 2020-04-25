import os
import time
from slack import WebClient
from slack.errors import SlackApiError
from flask import Flask, request, make_response, Response
import json

app = Flask(__name__)

slack_token = "xoxb-1096471659041-1086356946467-hgDY5l937lAbsnZPmO8C8hm7"
verification_token = "OWsReC2914G1XxtLbhSNYjly"
client = WebClient(token=slack_token)


def send_slack_message(ch):
    return client.chat_postMessage(
        channel=ch,
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
                        "value": "click_me_123"
                    }
                ]
            }
        ]
    )


@app.route("/slack/actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Verify that the request came from Slack
    print(form_json["token"])
    print(form_json)

    # Check to see what the user's selection was and update the message accordingly
    # selection = form_json["actions"][0]["selected_options"][0]["value"]

    # if selection == "cappuccino":
    # message_text = "cappuccino"
    # else:
    # message_text = "latte"

    # response = client.chat_update(
    #   channel=form_json["channel"]["id"],
    #   ts=form_json["message_ts"],
    #   text="One {}, right coming up! :coffee:".format(message_text),
    # )

    # Send an HTTP 200 response with empty body so Slack knows we're done here
    return make_response("", 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
