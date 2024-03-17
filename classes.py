import asyncio
import datetime
import platform

class User:
    def __init__(self, id: int, username: str, display_name: str, discriminator: str) -> None:
        self.id = id
        self.username = username
        self.display_name = display_name
        self.discriminator = discriminator

class Message:
    def __init__(self, id: int, channel_id: int, author: User, content: str) -> None:
        self.id = id
        self.channel_id = channel_id
        self.author = author
        self.content = content
