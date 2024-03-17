import requests
import json

TOKEN = ''
api_url = r"https://discord.com/api/v10"

def set_token(token: str):
    global TOKEN
    TOKEN = token

def send_request_post(route, body):
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{api_url}{route}", data=json.dumps(body), headers=headers)