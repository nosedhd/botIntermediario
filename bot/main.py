from __future__ import annotations

import logging

import discord

from .config import Settings
from .discord_bot import RelayDiscordClient
from .handler import MessageForwarder
from .n8n_client import N8NWebhookClient


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def main() -> None:
    settings = Settings.from_env()
    settings.validate()
    configure_logging(settings.log_level)

    intents = discord.Intents.default()
    intents.message_content = True

    async def runner() -> None:
        async with N8NWebhookClient(
            webhook_url=settings.n8n_webhook_url,
            timeout_seconds=settings.http_timeout_seconds,
        ) as webhook_client:
            forwarder = MessageForwarder(
                webhook_client=webhook_client,
                message_prefix=settings.message_prefix,
            )
            client = RelayDiscordClient(forwarder=forwarder, intents=intents)
            await client.start(settings.discord_bot_token)

    import asyncio

    asyncio.run(runner())


if __name__ == "__main__":
    main()
