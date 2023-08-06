import requests

url = 'http://127.0.0.1:8000/th/api/slack/webhook/'

payload = {
    'token': '99AU1adxvoRneDE3EK9nc8Jm',
    'team_id': 'T0001',
    'team_domain': 'example',
    'channel_id': 'C2147483705',
    'channel_name': 'test',
    'timestamp': '1355517523.000005',
    'user_id': 'U2147483697',
    'user_name': 'Steve',
    'text': 'googlebot: What is the air-speed velocity of an unladen swallow?',
    'trigger_word': 'googlebot:'
}

request = requests.post(url, data=payload)
print(request)
