#!/usr/bin/env python

import zulip
import config
import json
import requests
import random

client = zulip.Client(email=config.USERNAME,
                      api_key=config.API_KEY)

# call respond function when client interacts with gif bot
def respond(msg):
    if msg['sender_email'] != "gif-bot@students.hackerschool.com":
        content = msg['content'].upper().split()
            
        if (content[0] == "GIF" and content[1] == "ME"):
            normalized = normalize_query(content)
            api_call = "http://api.giphy.com/v1/gifs/search?limit=20&q=%s&api_key=dc6zaTOxFJmzC" % normalized
            img_url = call_giphy(api_call)

            client.send_message({
                "type": msg['type'],
                "subject": msg['subject'],
                "to": msg['sender_email'],
                "content": "%s" % img_url
            })

        else:
            client.send_message({
                "type": msg['type'],
                "subject": msg['subject'],
                "to": msg['sender_email'],
                "content": "I don't know what you're talking about :tired_face:"
            })

def call_giphy(api_url):    
    response = requests.get(api_url).content
    loaded_json = json.loads(response)
    rand_index = random.randint(0,19)
    url = loaded_json['data'][rand_index]['images']['fixed_width']['url']
    return url

# accept the content of msg split into array
def normalize_query(arr):
    query = '+'.join(arr[2:])
    return query.lower()

# This is a blocking call that will run forever
client.call_on_each_message(lambda msg: respond(msg))
