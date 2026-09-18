from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp


class N8NWebhookClient:
    def __init__(self, webhook_url: str, timeout_seconds: float = 15.0, session: aiohttp.ClientSession | None = None):
        self.webhook_url = webhook_url
        self.timeout_seconds = timeout_seconds
        self._session = session
        self._owns_session = session is None


    async def __aenter__(self) -> "N8NWebhookClient":
        if self._session is None:
            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self


    async def __aexit__(self, *_: Any) -> None:
        if self._owns_session and self._session:
            await self._session.close()


    async def send_message(self, payload: dict[str, str]) -> bool:
        if self._session is None:
            raise RuntimeError("N8NWebhookClient session is not initialized")

        try:
            async with self._session.post(self.webhook_url, json=payload) as response:
                if 200 <= response.status < 300:
                    logging.debug("Payload sent to n8n", extra={"status": response.status})
                    return True
                body = await response.text()
                logging.error(
                    "n8n webhook returned non-success status",
                    extra={"status": response.status, "response_body": body[:500]},
                )
                return False
        except asyncio.TimeoutError:
            logging.exception("Timeout sending payload to n8n")
            return False
        except aiohttp.ClientError:
            logging.exception("HTTP error sending payload to n8n")
            return False
