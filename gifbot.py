#!/usr/bin/env python

import zulip
import json
import requests
import random
import os

# create a Zulip client/bot
client = zulip.Client(email=os.environ['ZULIP_USERNAME'],
                      api_key=os.environ['ZULIP_API_KEY'])

# call Zulip API to get list of all streams
def get_zulip_streams():
    response = requests.get(
        'https://api.zulip.com/v1/streams',
        auth=requests.auth.HTTPBasicAuth(os.environ['ZULIP_USERNAME'], os.environ['ZULIP_API_KEY'])
    )

    if response.status_code == 200:
        return response.json()['streams']

    elif response.status_code == 401:
        raise RuntimeError('check yo auth')

    else:
        raise RuntimeError(':( we failed to GET streams.\n(%s)' % response)


# subscribe the bot to all streams
def subscribe_to_streams(streams):
    streams = [
            {'name': stream['name']}

            for stream in get_zulip_streams()
        ]

    client.add_subscriptions(streams)

# Class used to keep track of messages sent by the bot
# for undo functionality.
class LastMsg:

    def __init__(self):
        self.msg_ids = {}

    def update(self, _stream, _topic, _id):
        if _stream in self.msg_ids:
            if _topic in self.msg_ids[_stream]:
                self.msg_ids[_stream][_topic].append(_id)
            else:
                self.msg_ids[_stream][_topic] = [_id]
        else: 
            self.msg_ids[_stream] = dict()
            self.msg_ids[_stream][_topic] = [_id]
        
    def getMsgId(self, _stream, _topic):
        return self.msg_ids[_stream][_topic].pop()

    def checkEmpty(self, _stream, _topic):
        if (len(self.msg_ids) == 0):
            return True

        elif (_stream not in self.msg_ids or len(self.msg_ids[_stream]) == 0):
            return True

        elif (_topic not in self.msg_ids[_stream] or len(self.msg_ids[_stream][_topic]) == 0):
            return True

        else:
            return False

# instantiate a new LastMsg intance
last_message = LastMsg()

# call respond function when client interacts with gif bot
def respond(msg):

    # Make sure the bot never responds to itself or it results in infinite loop
    if msg['sender_email'] != "gif-bot@students.hackerschool.com":
        content = msg['content'].upper().split()
            
        # bot only sends msg back when messaged gif me or @gif bot gif me    
        if ((content[0] == "GIF" and content[1] == "ME") 
            or (content[0] == "@**GIF" and content[1] == "BOT**" and content[2] == "GIF" and content[3] == "ME")):

            normalized = normalize_query(content)
            api_call = "http://api.giphy.com/v1/gifs/search?limit=20&q=%s&api_key=dc6zaTOxFJmzC" % normalized
            img_url = call_giphy(api_call)

            # respond to public stream msgs
            if msg['type'] == 'stream':
                resp = client.send_message({
                    "type": "stream",
                    "subject": msg["subject"],
                    "to": msg['display_recipient'],
                    "content": "%s" % img_url
                })

                last_message.update(msg['display_recipient'], msg["subject"], resp['id'])

            # respond to private msg
            elif msg['type'] == 'private':
                resp = client.send_message({
                    "type": msg['type'],
                    "subject": msg['subject'],
                    "to": msg['sender_email'],
                    "content": "%s" % img_url
                })

                # Should undo be enabled in private msgs?
                # last_message.update(resp['id'])

        # undo logic
        elif (content[0] == "UNDO"):
            if not last_message.checkEmpty(msg['display_recipient'], msg['subject']):
                payload = { 'message_id': last_message.getMsgId(msg['display_recipient'], msg['subject']), 
                            'content': 'NOPE.'
                            }
                url = "https://api.zulip.com/v1/messages"
                resp = requests.patch(url, data=payload, auth=requests.auth.HTTPBasicAuth(os.environ['ZULIP_USERNAME'], os.environ['ZULIP_API_KEY']))

# grab a GIF by calling the GIPHY API
def call_giphy(api_url):    
    response = requests.get(api_url).content
    loaded_json = json.loads(response)
    count = loaded_json['pagination']['count']-1
    if count >= 0:
        rand_index = random.randint(0,count)
        url = loaded_json['data'][rand_index]['images']['fixed_width']['url']
    else:
        # need to replace with a fun 'sorry' image if no images found
        url = "http://i.imgflip.com/b2jul.jpg"
    return url

# accept the content of msg split into array
def normalize_query(arr):
    query = '+'.join(arr[2:])
    return query.lower()


ZULIP_STREAMS = get_zulip_streams()
subscribe_to_streams(ZULIP_STREAMS)

# This is a blocking call that will run forever
client.call_on_each_message(lambda msg: respond(msg))
