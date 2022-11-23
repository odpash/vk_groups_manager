import dataclasses
import datetime
import json

import requests


API_HEADING = 'https://api.vk.com/method/'
API_VERSION = '5.131'


@dataclasses.dataclass
class MessagePreview:
    first_name: str
    last_name: str
    photo_link: str
    group_name: str
    peer: int
    last_message_text: str
    last_message_date: int
    is_unread: bool
    api_key: str


def get_conversations(access_token: str) -> dict:
    response = requests.post(API_HEADING + f'messages.getConversations',
                             data={
                                 'access_token': access_token,
                                 'v': API_VERSION
                             }).json()
    return response


def get_user_info(conversations: dict, access_token: str) -> list:
    items = conversations['response']['items']
    res = []
    for item in items:
        peer = item['conversation']['peer']['id']
        response = requests.post(API_HEADING + f'messages.getConversationMembers',
                                 data={
                                     'access_token': access_token,
                                     'peer_id': peer,
                                     'v': '5.131'
                                 }).json()['response']
        profile = response['profiles'][0]
        first_name = profile['first_name']
        last_name = profile['last_name']
        photo = profile['photo_50']
        group_name = response['groups'][0]['name']
        item['members'] = {'first_name': first_name, 'last_name': last_name, 'photo': photo, 'group_name': group_name}
        res.append(item)
    return res


def get_message_object(item: dict, access_token) -> MessagePreview:
    return MessagePreview(
        first_name=item['members']['first_name'],
        last_name=item['members']['last_name'],
        photo_link=item['members']['photo'],
        group_name=item['members']['group_name'],
        peer=item['conversation']['peer']['id'],
        last_message_text=item['last_message']['text'],
        last_message_date=int(item['last_message']['date']),
        is_unread='unread_count' in item['conversation'].keys(),
        api_key=access_token
    )


def sort_messages(messages: list[MessagePreview]) -> list[MessagePreview]:
    messages.sort(key=lambda x: x.last_message_date, reverse=True)
    messages.sort(key=lambda x: x.is_unread, reverse=True)
    return messages


def run():
    messages = []
    for access_token in json.loads(open('api_keys.json', 'r').read()):
        items = get_user_info(get_conversations(access_token), access_token)
        for item in items:
            messages.append(get_message_object(item, access_token))
    messages = sort_messages(messages)
    return messages
