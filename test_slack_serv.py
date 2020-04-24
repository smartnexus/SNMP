import os
from slack import WebClient
#from slackclient import Slackclient
from slack.errors import SlackApiError

client = WebClient(token='xoxb-1096471659041-1069373940215-BrYrc73i9UcbV5X7gaOBjh3v')

try:
    response = client.chat_postMessage(
        channel='#proyectogestion',
        text="Celia te estoy vigilando")
    assert response["message"]["text"] == "Celia te estoy vigilando"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")