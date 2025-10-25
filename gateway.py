import asyncio, aiohttp, requests, websockets, json, inspect
from .classes import User

APIURL = "https://discord.com/api"

# Heartbeat function
async def heartbeat(websocket, interval):
    while True:
        await asyncio.sleep(interval / 1000)
        await websocket.send(json.dumps({"op": 1, "d": None}))

# Identify function
async def identify(websocket, intents: list, token):
    intent_int = 0
    for intent in intents:
        intent_int = intent_int | intent
    
    identify_payload = {
        "op": 2,
        "d": {
            "token": f"Bot {token}",
            "properties": {
                "os": "noaycord",
                "browser": "noaycord",
                "device": "noaycord"
            },
            "intents": intent_int
        }

    }
    
    await websocket.send(json.dumps(identify_payload))

# Main gateway loop
async def event_loop(bot, token):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{APIURL}/gateway") as resp:
            data = await resp.json()
            GATEWAYURL = data["url"]
    
    async with websockets.connect(GATEWAYURL) as ws:
        while True:
            response = json.loads(await ws.recv())
            
            if response["op"] == 10:
                asyncio.create_task(heartbeat(ws, response["d"]["heartbeat_interval"]))
                await identify(ws, bot.intents, token)
            
            if response["t"] == "READY" and inspect.iscoroutinefunction(bot.event_handlers["on_ready"]):
                bot_user = User(
                    response["d"]["user"]["id"],
                    response["d"]["user"]["username"]
                )
                
                bot.user = bot_user
                #TODO: fill the rest of the user class
                await bot.event_handlers["on_ready"]()
            
            if response["t"] == "MESSAGE_CREATE" and inspect.iscoroutinefunction(bot.event_handlers["on_message"]):
                await bot.event_handlers["on_message"](response["d"]["content"])
