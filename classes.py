import asyncio
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    username: str
    display_name: Optional[str] = None
    discriminator: str = "0000"
    avatar: Optional[str] = None
    is_bot: bool = False
    is_system: bool = False
    is_mfa_enabled: Optional[bool] = None
    banner: Optional[str] = None
    accent_color: Optional[int] = None
    locale: Optional[str] = None
    is_verified: Optional[bool] = None
    email: Optional[str] = None
    flags: Optional[int] = 0
    premium_type: Optional[int] = 0
    public_flags: Optional[int] = 0

@dataclass
class Message:
    id: int
    channel_id: int
    author: User
    content: Optional[str]
    timestamp: str
    edited_timestamp: Optional[str]
    is_tts: bool
    mentions_everyone: bool
    mentioned: Optional[list]
    mentioned_roles: Optional[list]
    mentioned_channels: Optional[list]
    attachments: Optional[list]
    embeds: Optional[list]
    reactions: Optional[list]
    nonce: str
    is_pinned: bool
    webhook_id: Optional[int]
    message_type: int
    

# Needed so the code doesnt throw a circular import 
from .gateway import event_loop
class Bot():
    
    def __init__(self, *args):
        self.event_handlers = {}
        self.intents = []
        for i, intent in enumerate(args):
            self.intents.append(intent)
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
