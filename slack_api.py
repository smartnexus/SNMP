from flask import Flask, request, make_response, Response
#from slackclient import SlackClient

#
# Bot functions to send and receive messages from Slack Chat.
#

# TODO: Generate Slack chat to start config environment.
SLACK_BOT_TOKEN = ""
SLACK_VERIFICATION_TOKEN = ""

# Slack client for Web API requests
#slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)


def init_connection():
    # TODO: Declare methods to init Slack Bot chat.
    print('[Slack API] Initializing connection...')
