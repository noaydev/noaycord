import asyncio
import requests
import websockets
import json

api_url = r"https://discord.com/api/v10"

async def heartbeat(websocket, heartbeat):
    while True:
        heartbeat_data = {
            "op": 1,
            "d": "null"
        }
        await asyncio.sleep(heartbeat / 1000)
        await websocket.send(json.dumps(heartbeat_data))

async def go_online(token: str):
    # Get the gateway url
    gateway_url = requests.get(api_url + '/gateway')
    gateway_url = gateway_url.json()
    gateway_url = gateway_url['url']
    # Establish connection
    async with websockets.connect(gateway_url) as ws:
        while True:
            response = await ws.recv()
            response = json.loads(response)
            if response['op'] == 10:
                asyncio.create_task(heartbeat(ws, response['d']['heartbeat_interval']))

class Bot:
    def __init__(self) -> None:
        pass
    def run(self, token: str):
        asyncio.run(go_online(token))