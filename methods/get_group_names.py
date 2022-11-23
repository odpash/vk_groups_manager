import requests

from methods.get_dialogs import API_HEADING, API_VERSION


def get_group_info(access_token: str) -> dict:
    response = requests.post(API_HEADING + f'messages.getConversations',
                             data={
                                 'access_token': access_token,
                                 'v': API_VERSION
                             }).json()
    peer = response['response']['items'][0]['conversation']['peer']['id']
    response = requests.post(API_HEADING + f'messages.getConversationMembers',
                             data={
                                 'access_token': access_token,
                                 'peer_id': peer,
                                 'v': '5.131'
                             }).json()

    r = requests.post(API_HEADING + f'groups.getOnlineStatus',
                             data={
                                 'access_token': access_token,
                                 'group_id': response['response']['groups'][0]['id'],
                                 'v': '5.131'
                             }).json()
    response['response']['groups'][0]['online'] = "Офлайн" if r['response']['status'] == 'none' else "Онлайн"
    return response['response']['groups']

