import os
import time
import re
from slackclient import SlackClient

# instantiate the Slack client with the token we exported from the app
# Within the same directory export SLACK_BOT_TOKEN=' bot user access token here'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
print(os.environ.get('SLACK_BOT_TOKEN'))
# TO-DO: fix the issue of always having to declare the env token & certs for ssl errors
# initially declare the id as None and once app starts up value gets assigned

starterbot_id = None
rtm_read_delay = 2
default_command = "Are there any issues with PAT6 lab ? My modem is stuck in scanning"

# the first pattern '<@(|[WU].+?)>' represents the username format in slack
# the second sub pattern '(.*)' contains the remaining message in the text event,
# typically when you tag @bot followed by  a question, the question is the remaining message.
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned.
        If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    if matches:

        return matches.group(1), matches.group(2).strip()

    else:
        (None, None)


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(default_command)

    # Finds and executes the given command, filling in response
    response = None

    # build the rule based response here
    if command.startswith('Is there any cadence going on?'):
        # TO-DO: work on integrating this with the cadence api to get hold of daily cadences scehduled
        response = "Yes the cadence for today is 'https:cadence.viasat.io'"

    elif 'outage' in command:
        # TO-DO: Tag lab support as well using the format <@WL..>
        response = "Check out the grafana page for PAT6 'https:grafana.preprod-pat6.viasat.io'"

    else:
        # TO-DO : add more bag of words for rule based responses
        # If no matches, use the web api method chat.postMessage to send the responses
        response = default_response

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Slack Bot is successfully connected!! Waiting to communicate!")

        # Bot user has a user ID for each workspace the Slack App is installed within.
        # Obtaining the user ID will be needed if it gets mentioned in a message.
        # Get this using the auth.test method
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            # pause for RTM_READ_DELAY seconds so to not exhaust the CPU time
            time.sleep(rtm_read_delay)
    else:
        print("Connection failed. Exception traceback printed above.")
