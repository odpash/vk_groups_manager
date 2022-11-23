import requests

API_HEADING = 'https://api.vk.com/method/'
ACCESS_TOKEN = "vk1.a.qXbaL3CYDwLowdChW2YLqj9_FpnYLgLqkJensYz8xYbM4hA8MWhI6djR_jBpAd4UfyUKPYKFkGynKFXz890HhvF1LxfZiD2UwATLYbHdZcaayV5ENiwuAIVwcH8cHFr4W-sSz3YPcAMXVQbiaPNUIrf9kN8KNd4ADFKXvr1OTndNSQiNsKQgToGWOPO1BXWnQ6J9d8D3ffSmhNlec9Q28Q"
response = requests.post(API_HEADING + f'messages.getConversations',
                         data={
                             'access_token': ACCESS_TOKEN,
                             'v': '5.131'
                         })  # получить все беседы группы

items = response.json()['response']['items']
for item in items:
    peer = item['conversation']['peer']['id']
    print(peer)
    response = requests.post(API_HEADING + f'messages.getConversationMembers',
                             data={
                                 'access_token': ACCESS_TOKEN,
                                 'peer_id': peer,
                                 'v': '5.131'
                             })  # получить информацию о пользователе
    print(2, response.json())

    response = requests.post(API_HEADING + f"messages.getHistory",
                             data={
                                 'access_token': ACCESS_TOKEN,
                                 'peer_id': peer,
                                 'v': '5.131'
                             })
    print(3, response.json())