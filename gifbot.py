#!/usr/bin/env python

import zulip
import json
import requests
import random
import os

f = open('subscriptions.txt', 'r')

ZULIP_STREAMS = []

for line in f: 
    ZULIP_STREAMS.append(line.strip())

print ZULIP_STREAMS

client = zulip.Client(email=os.environ['ZULIP_USERNAME'],
                      api_key=os.environ['ZULIP_API_KEY'])

client.add_subscriptions([{"name": stream_name} for stream_name in ZULIP_STREAMS])

# call respond function when client interacts with gif bot
def respond(msg):

    if msg['sender_email'] != "gif-bot@students.hackerschool.com":
        content = msg['content'].upper().split()
            
        if ((content[0] == "GIF" and content[1] == "ME") 
            or (content[0] == "@**GIF" and content[1] == "BOT**" and content[2] == "GIF" and content[3] == "ME")):

            normalized = normalize_query(content)
            api_call = "http://api.giphy.com/v1/gifs/search?limit=20&q=%s&api_key=dc6zaTOxFJmzC" % normalized
            img_url = call_giphy(api_call)

            if msg['type'] == 'stream':
                client.send_message({
                    "type": "stream",
                    "subject": msg["subject"],
                    "to": msg['display_recipient'],
                    "content": "%s" % img_url
                })
            else:
                client.send_message({
                    "type": msg['type'],
                    "subject": msg['subject'],
                    "to": msg['sender_email'],
                    "content": "%s" % img_url
                })

def call_giphy(api_url):    
    response = requests.get(api_url).content
    loaded_json = json.loads(response)
    count = loaded_json['pagination']['count']-1
    if count >= 0:
        rand_index = random.randint(0,count)
        url = loaded_json['data'][rand_index]['images']['fixed_width']['url']
    else:
        # need to replace with a fun 'sorry' image if no images found
        url = "https://d29xw0ra2h4o4u.cloudfront.net/assets/logo-no-text-d8ed16eddb595505005e8a9c69eb6011.png"
    return url

# accept the content of msg split into array
def normalize_query(arr):
    query = '+'.join(arr[2:])
    return query.lower()

# This is a blocking call that will run forever
client.call_on_each_message(lambda msg: respond(msg))
