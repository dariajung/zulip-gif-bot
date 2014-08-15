zulip-gif-bot
=============

####What is it
---
A gif bot for the Hacker School Zulip.


####Usage
---

Gif bot is intended to be very simple to use. It will only respond to messages starting with gif me or @gif bot gif me.

`gif me < QUERY >` or `@gif bot gif me < QUERY >`.

Due to popular demand, there is also an undo functionality. Simply write `undo` in the thread where the unwanted gif was posted by Gif Bot. The image will be replaced with `NOPE.`

####Screenshots
----
Query:

!["Gif bot in action"](http://i.imgur.com/o1l67Zi.png)

Undo:

![Imgur](http://i.imgur.com/zplkxRK.png)

####Notes about Zulip API
----
I used the Zulip API [Python bindings](https://github.com/zulip/python-zulip) for this project. However, there is no binding for updating a post. To do this, I had to directly send a `PATCH` request to the Zulip messages endpoint of their API. Zulip uses BasicAuth which I wasn't aware of until speaking with one of their engineers.

**Example**

```python
payload = { 'message_id': last_message.getMsgId(msg['display_recipient'], msg['subject']), 
            'content': 'NOPE.'
          }
url = "https://api.zulip.com/v1/messages"
resp = requests.patch(url, data=payload, auth=requests.auth.HTTPBasicAuth(os.environ['ZULIP_USERNAME'], os.environ['ZULIP_API_KEY']))
```

There is also no way to subscribe the bot to all of the streams without subscribing it to all individual streams. In order to achieve this, I used a console hack to list all of the streams, piped it to a text file, `subscriptions.txt`, and subscribed the bot to all streams.

####Siblings
---

Gif bot has a sibling [meme bot](https://github.com/bruslim/zulip-meme-bot).


####LICENSE

```
The MIT License (MIT)

Copyright (c) 2014 Daria Jung

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
