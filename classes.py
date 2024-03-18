from .http_handler import send_request_post_json

class User:
    def __init__(self, id: int, username: str, display_name: str, discriminator: str) -> None:
        self.id = int(id)
        self.username = username
        self.display_name = display_name
        self.discriminator = discriminator


class Message:
    def __init__(self, id: int, channel_id: int, guild_id, author: User, content: str) -> None:
        self.id = int(id)
        self.channel_id = int(channel_id)
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
        print('got here')
        send_request_post_json(f'/channels/{self.channel_id}/messages', message)
