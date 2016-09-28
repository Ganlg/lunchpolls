from channels import Group
from channels.sessions import channel_session
from lunch.models import Post
from django.contrib.auth.models import User
from .models import Message
from django.shortcuts import get_object_or_404
import json
from django.utils.timezone import get_current_timezone


# def ws_add(message):
#     Group('chat').add(message.reply_channel)
#
#
# def ws_echo(message):
#     Group('chat').send({
#         'text': message.content['text'],
#     })

@channel_session
def ws_connect(message):
    post_id = message['path'].strip('/')
    post = get_object_or_404(Post, pk=post_id)
    Group('chat-' + str(post.pk)).add(message.reply_channel)
    message.channel_session['post_id'] = post.pk


@channel_session
def ws_receive(message):
    post_id = message.channel_session['post_id']
    post = get_object_or_404(Post, pk=post_id)
    data = json.loads(message['text'])
    user = get_object_or_404(User, username=data['user'])
    m = Message.objects.create(post=post, user=user, message=data['message'])
    tz = get_current_timezone()
    echo = {
        'user': user.username,
        'message': m.message,
        'timestamp': tz.normalize(m.timestamp.astimezone(tz)).strftime("%b %d %Y %H:%M:%S")
    }
    Group('chat-'+ str(post.pk)).send({'text': json.dumps(echo)})

@channel_session
def ws_disconnect(message):
    post_id = message.channel_session['post_id']
    Group('chat-'+post_id).discard(message.reply_channel)