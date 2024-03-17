import asyncio
from .methods import *

class Bot:
    def __init__(self, *intents) -> None:
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