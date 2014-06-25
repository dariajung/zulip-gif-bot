#!/usr/bin/env python

import zulip
import sys
import config
import json
import requests

client = zulip.Client(email=config.USERNAME,
                      api_key=config.API_KEY)

# Send a private message
client.send_message({
    "type": "private",
    "to": config.EMAIL,
    "content": "testing"
})

# call respond function when client interacts with gif bot
def respond(msg):
    if msg['sender_email'] != "gif-bot@students.hackerschool.com":
        content = msg['content'].upper().split()
            
        if (content[0] == "GIF" and content[1] == "ME"):
            print "yay gif me"

        else:
            client.send_message({
                "type": "private",
                "to": config.EMAIL,
                "content": "I don't know what you're talking about :tired_face:"
            })

def call_giphy(search_param):
    response = requests.get("http://api.giphy.com/v1/gifs/search?limit=20&q=funny+cat&api_key=dc6zaTOxFJmzC")

def normalize_query(arr):
    query = '+'.join(arr[2:])
    return query.lower()

# Print each message the user receives
# This is a blocking call that will run forever
client.call_on_each_message(lambda msg: respond(msg))

# Print every event relevant to the user
# This is a blocking call that will run forever
# This will never be reached unless you comment out the previous line
#client.call_on_each_event(lambda msg: sys.stdout.write(str(msg) + "\n"))