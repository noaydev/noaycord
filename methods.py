import asyncio
import requests
import websockets
import json
import platform
import datetime
from enum import Enum

from .classes import User, Message
from .http_handler import set_token

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

seq_number = "null"

async def heartbeat(websocket, heartbeat):
    while True:
        heartbeat_data = {
            "op": 1,
            "d": seq_number
        }
        await websocket.send(json.dumps(heartbeat_data))
        await asyncio.sleep(heartbeat / 1000)

async def event_loop(token: str, bot, intents):
    set_token(token)
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
    # Establish connection
    async with websockets.connect(gateway_url) as ws:
        while True:
            response = await ws.recv()
            response = json.loads(response)
            #print(response)
            if response['op'] == 10:
                asyncio.create_task(heartbeat(ws, response['d']['heartbeat_interval']))
                asyncio.create_task(identify(ws, token, intent_number))
            elif response['op'] == 0:
                global seq_number
                seq_number = int(response['s'])
                if response['t'] == 'READY':
                    bot.on_ready(opt=f'{datetime.datetime.now().date()} {platform.system()}')
                if response['t'] == 'MESSAGE_CREATE':
                    user = User(response['d']['author']['id'], \
                    response['d']['author']['username'], response['d']['author']['global_name'], \
                    response['d']['author']['discriminator'])
                    
                    message = Message(response['d']['id'], response['d']['channel_id'],
                    response['d']['guild_id'] ,user,\
                    response['d']['content'])
                    
                    bot.on_message(message, opt=f'{datetime.datetime.now().date()} {platform.system()}')
class Bot:
    def __init__(self, intents) -> None:
        self.event_handlers = {}
        self.intents = []
        for intent in intents:
            self.intents.append(intent)
    def run(self, token: str):
        try:
            asyncio.run(event_loop(token, self, self.intents))
        except KeyboardInterrupt:
            print('\nExited successfully')
            quit(0)
    def on_ready(self, opt=None):
        def wrapper(func):
            self.event_handlers['ready'] = func
        if opt == f'{datetime.datetime.now().date()} {platform.system()}' \
        and self.event_handlers.get('ready') != None:
            asyncio.create_task(self.event_handlers['ready']())
            return
        return wrapper
    def on_message(self, message=None, opt=None):
        def wrapper(func):
            self.event_handlers['message'] = func
        if opt == f'{datetime.datetime.now().date()} {platform.system()}' \
        and self.event_handlers.get('message') != None:
            asyncio.create_task(self.event_handlers['message'](message))
            return
        return wrapper