from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    discord_bot_token: str
    n8n_webhook_url: str
    message_prefix: str
    http_timeout_seconds: float
    log_level: str


    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            discord_bot_token=os.getenv("DISCORD_BOT_TOKEN", "").strip(),
            n8n_webhook_url=os.getenv("N8N_WEBHOOK_URL", "").strip(),
            message_prefix=os.getenv("MESSAGE_PREFIX", ""),
            http_timeout_seconds=float(os.getenv("HTTP_TIMEOUT_SECONDS", "15")),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


    def validate(self) -> None:
        missing = []
        if not self.discord_bot_token:
            missing.append("DISCORD_BOT_TOKEN")
        if not self.n8n_webhook_url:
            missing.append("N8N_WEBHOOK_URL")
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
