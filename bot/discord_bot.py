from __future__ import annotations

import discord

from .handler import MessageForwarder


class RelayDiscordClient(discord.Client):
    def __init__(self, forwarder: MessageForwarder, **kwargs):
        super().__init__(**kwargs)
        self.forwarder = forwarder


    async def on_ready(self) -> None:
        print(f"Logged in as {self.user} ({self.user.id})")


    async def on_message(self, message: discord.Message) -> None:
        if self.user and message.author.id == self.user.id:
            return
        await self.forwarder.process_message(message)
