import asyncio
import requests
import websockets
import json
import platform
import datetime
from enum import Enum

api_url = r"https://discord.com/api/v10"

async def identify(websocket, token, intent_number):
    identify = {
        "op": 2,
        "d": {
            "token": f"{token}",
            "intents": intent_number,
            "properties": {
                "os": f"{platform.system()}",
                "browser": "noaycord",
                "device": "noaycord"
            }
        }
    }
    await websocket.send(json.dumps(identify))

async def heartbeat(websocket, heartbeat):
    while True:
        heartbeat_data = {
            "op": 1,
            "d": "null"
        }
        await websocket.send(json.dumps(heartbeat_data))
        await asyncio.sleep(heartbeat / 1000)

async def event_loop(token: str, bot, intents):
    # Get the gateway url
    gateway_url = requests.get(api_url + '/gateway')
    gateway_url = gateway_url.json()
    gateway_url = gateway_url['url']
    # Calculate intent number
    intent_number = 0
    for intent in intents:
        if isinstance(intent, Enum):
            intent_number |= intent.value
        else:
            intent_number |= intent
    print(intent_number)
    # Establish connection
    async with websockets.connect(gateway_url) as ws:
        while True:
            response = await ws.recv()
            response = json.loads(response)
            #print(response)
            if response['op'] == 10:
                asyncio.create_task(heartbeat(ws, response['d']['heartbeat_interval']))
                asyncio.create_task(identify(ws, token, intent_number))
            elif response['t'] == 'READY':
                bot.on_ready(opt=f'{datetime.datetime.now().date()} {platform.system()}')