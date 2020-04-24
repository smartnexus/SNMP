from flask import Flask, request, make_response, Response
from slackclient import SlackClient

#
# Bot functions to send and receive messages from Slack Chat.
#

# TODO: Generate Slack chat to start config environment.
SLACK_BOT_TOKEN = "xoxb-1096471659041-1069373940215-BrYrc73i9UcbV5X7gaOBjh3v"
SLACK_VERIFICATION_TOKEN = ""

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)


def slackconnect():
    return slack_client.rtm_connect()


# Flask web server for incoming traffic from Slack
app = Flask(__name__)


def init_connection():
    # TODO: Declare methods to init Slack Bot chat.
    print('[Slack API] Initializing connection...')
