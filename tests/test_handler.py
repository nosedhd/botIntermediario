from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from bot.handler import MessageForwarder


class FakeAuthor:
    def __init__(self, author_id: int, name: str, bot: bool):
        self.id = author_id
        self.name = name
        self.bot = bot


    def __str__(self) -> str:
        return self.name


class FakeMessage:
    def __init__(self, *, content: str, bot: bool = False):
        self.content = content
        self.author = FakeAuthor(123, "alice", bot)
        self.guild = SimpleNamespace(id=456)
        self.channel = SimpleNamespace(id=789)
        self.id = 101112
        self.created_at = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)


@pytest.mark.asyncio
async def test_ignores_bot_messages() -> None:
    webhook = AsyncMock()
    webhook.send_message = AsyncMock(return_value=True)
    forwarder = MessageForwarder(webhook_client=webhook, message_prefix="")

    result = await forwarder.process_message(FakeMessage(content="hola", bot=True))

    assert result is False
    webhook.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_ignores_messages_without_required_prefix() -> None:
    webhook = AsyncMock()
    webhook.send_message = AsyncMock(return_value=True)
    forwarder = MessageForwarder(webhook_client=webhook, message_prefix="!bot")

    result = await forwarder.process_message(FakeMessage(content="hola", bot=False))

    assert result is False
    webhook.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_sends_expected_payload_to_n8n() -> None:
    webhook = AsyncMock()
    webhook.send_message = AsyncMock(return_value=True)
    forwarder = MessageForwarder(webhook_client=webhook, message_prefix="!bot")

    message = FakeMessage(content="!bot hola", bot=False)
    result = await forwarder.process_message(message)

    assert result is True
    webhook.send_message.assert_awaited_once_with(
        {
            "content": "!bot hola",
            "author_id": "123",
            "author_name": "alice",
            "guild_id": "456",
            "channel_id": "789",
            "message_id": "101112",
            "timestamp": "2026-01-01T12:00:00+00:00",
        }
    )
