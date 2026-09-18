from __future__ import annotations

from datetime import timezone
from typing import Any


class MessageForwarder:
    def __init__(self, webhook_client: Any, message_prefix: str = ""):
        self.webhook_client = webhook_client
        self.message_prefix = message_prefix


    def should_process_message(self, message: Any) -> bool:
        if getattr(message.author, "bot", False):
            return False
        if self.message_prefix and not message.content.startswith(self.message_prefix):
            return False
        return True


    def build_payload(self, message: Any) -> dict[str, str]:
        created_at = message.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        return {
            "content": message.content,
            "author_id": str(message.author.id),
            "author_name": str(message.author),
            "guild_id": str(message.guild.id) if message.guild else "",
            "channel_id": str(message.channel.id),
            "message_id": str(message.id),
            "timestamp": created_at.isoformat(),
        }


    async def process_message(self, message: Any) -> bool:
        if not self.should_process_message(message):
            return False
        return await self.webhook_client.send_message(self.build_payload(message))
