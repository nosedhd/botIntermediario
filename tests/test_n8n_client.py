from __future__ import annotations

import asyncio

import aiohttp
import pytest

from bot.n8n_client import N8NWebhookClient


class _Response:
    def __init__(self, status: int = 200, text: str = "ok"):
        self.status = status
        self._text = text


    async def text(self) -> str:
        return self._text


class _ContextManager:
    def __init__(self, response: _Response):
        self.response = response


    async def __aenter__(self) -> _Response:
        return self.response


    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None


class _Session:
    def __init__(self, behavior):
        self._behavior = behavior


    def post(self, *_args, **_kwargs):
        return self._behavior()


@pytest.mark.asyncio
async def test_handles_http_errors() -> None:
    def behavior():
        raise aiohttp.ClientError("boom")

    session = _Session(behavior)

    async with N8NWebhookClient("https://example.com", session=session) as client:
        result = await client.send_message({"content": "hola"})

    assert result is False


@pytest.mark.asyncio
async def test_handles_timeouts() -> None:
    def behavior():
        raise asyncio.TimeoutError

    session = _Session(behavior)

    async with N8NWebhookClient("https://example.com", session=session) as client:
        result = await client.send_message({"content": "hola"})

    assert result is False


@pytest.mark.asyncio
async def test_returns_false_for_non_2xx_status() -> None:
    def behavior():
        return _ContextManager(_Response(status=500, text="error"))

    session = _Session(behavior)

    async with N8NWebhookClient("https://example.com", session=session) as client:
        result = await client.send_message({"content": "hola"})

    assert result is False
