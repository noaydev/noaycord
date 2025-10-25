import asyncio
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    global_name: Optional[str] = None
    discriminator: str = "0000"
    avatar: Optional[str] = None
    bot: bool = False
    system: bool = False
    mfa_enabled: Optional[bool] = None
    banner: Optional[str] = None
    accent_color: Optional[int] = None
    locale: Optional[str] = None
    verified: Optional[bool] = None
    email: Optional[str] = None
    flags: Optional[int] = 0
    premium_type: Optional[int] = 0
    public_flags: Optional[int] = 0

# Needed so the code doesnt throw a circular import 
from .gateway import event_loop
class Bot():
    
    def __init__(self, intents: list):
        self.event_handlers = {}
        self.intents = intents
        self.user: User
    
    def event(self, func):
        self.event_handlers[func.__name__] = func
        return func
        
    async def dispatch(self, event_name: str, *args, **kwargs):
        if event_name in self.event_handlers:
            await self.event_handlers[event_name](*args, **kwargs)
        
    def run(self, token):
        try:
            asyncio.run(event_loop(self, token))
        except KeyboardInterrupt:
            exit(0)
