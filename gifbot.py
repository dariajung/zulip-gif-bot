#!/usr/bin/env python

import zulip
import sys
import config
import json

client = zulip.Client(email=config.USERNAME,
                      api_key=config.API_KEY)

# Send a private message
client.send_message({
    "type": "private",
    "to": "djj2115cu@gmail.com",
    "content": "testing"
})

# call respond function when client interacts with gif bot
def respond():
    pass

# Print each message the user receives
# This is a blocking call that will run forever
client.call_on_each_message(lambda msg: sys.stdout.write(str(msg) + "\n"))

# Print every event relevant to the user
# This is a blocking call that will run forever
# This will never be reached unless you comment out the previous line
client.call_on_each_event(lambda msg: sys.stdout.write(str(msg) + "\n"))