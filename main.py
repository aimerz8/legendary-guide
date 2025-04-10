import requests
import json

# Telegram
BOT_TOKEN = '475650137:AAERYaUkg5Q2UwXBeZHG6n9oAx6MsCkZJg8'
CHANNEL_USERNAME = '@million_na_marketplace'

# WordPress API (замени своими данными)
WP_API_URL = 'https://твой_сайт/wp-json/wp/v2/posts'
WP_USER = 'твой_логин'
WP_PASS = 'твой_пароль'

def get_latest_post():
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    res = requests.get(url).json()
    messages = [x['message'] for x in res['result'] if 'message' in x]
    if not messages:
        return None
    return messages[-1]

def post_to_wordpress(text):
    data = {
        'title': text[:40],
        'content': text,
        'status': 'publish'
    }
    auth = (WP_USER, WP_PASS)
    headers = {'Content-Type': 'application/json'}
    res = requests.post(WP_API_URL, auth=auth, headers=headers, data=json.dumps(data))
    return res.status_code == 201

def main():
    latest = get_latest_post()
    if not latest:
        return

    with open('last_id.txt', 'r+') as f:
        last_id = f.read().strip()
        if str(latest['message_id']) == last_id:
            return
        f.seek(0)
        f.write(str(latest['message_id']))
        f.truncate()

    post_to_wordpress(latest['text'])

if __name__ == '__main__':
    main()
