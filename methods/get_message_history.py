import requests

from methods.get_dialogs import API_HEADING, API_VERSION


def get_story(access_token: str, peer) -> dict:
    response = requests.post(API_HEADING + f'messages.getHistory',
                             data={
                                 'access_token': access_token,
                                 'peer_id': peer,
                                 'v': API_VERSION
                             }).json()
    return response
