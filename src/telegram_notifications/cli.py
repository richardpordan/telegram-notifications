"""Exposes CLI tools."""

import asyncio
import os

import typer
from dotenv import load_dotenv

from .async_telegram_client import AsyncTelegramClient as Bot

load_dotenv()

app = typer.Typer()


class MissingApiKeyError(Exception):
    """Raised when the BOT_API_KEY environment variable is not set."""


class MissingChatIdError(Exception):
    """Raised when the TARGET_CHAT_ID environment variable is not set."""


def get_bot():
    """Instantiate and return a Bot client using the BOT_API_KEY env variable.

    Returns:
        Bot (telegram_notifications.AsyncTelegramClient):
            A configured AsyncTelegramClient instance.

    Raises:
        MissingApiKeyError: If BOT_API_KEY is not set in the environment.

    """
    bot_api_key = os.getenv("BOT_API_KEY", None)
    if bot_api_key is None:
        raise MissingApiKeyError(
            "No BOT_API_KEY environment variable.",
        )
    return Bot(bot_api_key)


@app.command()
def get_updates() -> None:
    """Fetch and display pending updates from the Telegram Bot API."""
    bot = get_bot()
    result = asyncio.run(bot.get_updates())
    typer.echo(result)


@app.command()
def send_message(text: str, target_chat_id: str) -> None:
    """Send a message to the configured target chat.

    Args:
        text (str): The message text to send.
        target_chat_id (str): The target telegram chat id.

    Raises:
        MissingChatIdError: If TARGET_CHAT_ID is not set in the environment.

    """
    bot = get_bot()
    response = asyncio.run(
        bot.send_message(chat_id=target_chat_id, text=text),
    )
    if response is not True:
        typer.Exit(code=1)


if __name__ == "__main__":
    app()
