# import json
#
# from asgiref.sync import async_to_sync
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import uuid


def trigger_welcome_message():
    data = {
        "type": "welcome_message",
        "message": "Hello buddy!",
    }
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)('task', data)


# def broadcast_msg_to_chat(msg, group_name, user='admin', event_type='broadcast_message'):
#     channel_layer = get_channel_layer()
#     actual_message = json.dumps({'msg': msg, 'user': user})
#     broadcast_data = {
#         'type': event_type,
#         'message': actual_message
#     }
#     async_to_sync(channel_layer.group_send)(group_name, broadcast_data)
#
#


def random_id_generator():
    return uuid.uuid4().hex[:1].upper() + uuid.uuid4().hex[:1].lower()\
           + uuid.uuid4().hex[:1].upper() + uuid.uuid4().hex[:1].lower()\
           + uuid.uuid4().hex[:1].upper() + uuid.uuid4().hex[:1].lower()\



def random_username_generator():
    ls = []
    for i in range(12):
        ls.append(uuid.uuid4().hex[:1].upper() + uuid.uuid4().hex[:1].lower())

    return ''.join(ls)
