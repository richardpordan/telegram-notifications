"""Tests for AsyncTelegramClient."""

import os

import pytest
from dotenv import load_dotenv

from telegram_notifications import AsyncTelegramClient
from telegram_notifications.logger import setup_logger

load_dotenv()

logger = setup_logger(__name__)

BOT_API_KEY = os.getenv("BOT_API_KEY", "test-token")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID", "123456789")


# --- Unit tests (mocked) ---


@pytest.fixture
def client() -> AsyncTelegramClient:
    return AsyncTelegramClient(token=BOT_API_KEY)


@pytest.mark.asyncio
async def test_get_updates():
    """Calls the real Telegram API.

    Requires BOT_API_KEY in .env.

    """
    bot = AsyncTelegramClient(token=BOT_API_KEY)
    updates = await bot.get_updates()
    logger.info("Real get_updates returned %d update(s)", len(updates))
    assert isinstance(updates, list)


@pytest.mark.asyncio
async def test_send_message():
    """Sends a real message.

    Requires BOT_API_KEY and TARGET_CHAT_ID in .env.

    """
    bot = AsyncTelegramClient(token=BOT_API_KEY)
    result = await bot.send_message(
        text="Integration test.",
        chat_id=TARGET_CHAT_ID,
    )
    logger.info("Real send_message result: %s", result)
    assert result is True
