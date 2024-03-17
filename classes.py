import asyncio
import datetime
import platform

from .http_handler import send_request_post

class User:
    def __init__(self, id: int, username: str, display_name: str, discriminator: str) -> None:
        self.id = id
        self.username = username
        self.display_name = display_name
        self.discriminator = discriminator


class Message:
    def __init__(self, id: int, channel_id: int, guild_id: int, author: User, content: str) -> None:
        self.id = id
        self.channel_id = channel_id
        self.author = author
        self.content = content
        self.guild_id = guild_id

    def reply(self, message):
        message = {
            "content": f"{message}",
            "message_reference": {
                "message_id": int(self.id),
                "channel_id": int(self.channel_id),
                "guild_id": int(self.guild_id)
            }
        }
        send_request_post(f'/channels/{self.channel_id}/messages', message)
