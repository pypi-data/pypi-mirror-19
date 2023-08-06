'''
Usage:
    slackmsg (<text>) [<channel>] [-s]

Options:
    -h, --help                   Show this help.
    -v, --version              Show version.
    -s, --as-slack-bot      Post as 'API Bot'.
'''

import os

from slackclient import SlackClient
from docopt import docopt

arguments = docopt(__doc__, version='0.6.2')

def get_msg(arguments):
    return arguments.get('<text>')


def get_channel(arguments):
    arg_channel = arguments['<channel>']
    if not arg_channel:
        channel = '#admin'
    else:
        channel = '#{}'.format(arg_channel)
    return channel


def get_slack_bot(arguments):
    slack_bot = arguments['--as-slack-bot']
    return slack_bot

def post_slack_message(**kwargs):
    as_slack_bot = get_slack_bot(arguments)

    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    SLACKBOT_TOKEN = os.environ.get('SLACKBOT_TOKEN')

    if len(SLACK_TOKEN) == 0 and not as_slack_bot:
        slack_user_token = raw_input(
            'Your Slack token is missing.\nEnter your Slack token: ')
        print(
            '\nYou can also set the SLACK_TOKEN environment variable.')
    elif len(SLACK_TOKEN) > 0 and not as_slack_bot:
        slack_user_token = SLACK_TOKEN
    elif as_slack_bot and len(SLACKBOT_TOKEN) == 0:
        print('You are required to set the SLACKBOT_TOKEN environment variable.')
    elif as_slack_bot and len(SLACKBOT_TOKEN) > 0:
        slack_user_token= SLACKBOT_TOKEN

    slacker = SlackClient(slack_user_token)
    resp = slacker.api_call('chat.postMessage', **kwargs)
    print resp
    return resp


def __main__(**kwargs):
    message = get_msg(arguments)
    channel = get_channel(arguments)
    print arguments

    post_slack_message(channel=channel,
                       as_user=True,
                       text=message)
