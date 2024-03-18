import requests
import json

TOKEN = ''
api_url = r"https://discord.com/api/v10"

def set_token(token: str):
    global TOKEN
    TOKEN = token

def send_request_post_json(route, body):
    print('Got ehre lol')
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    print(headers, json.dumps(body))
    response = requests.post(f"{api_url}{route}", data=json.dumps(body), headers=headers)