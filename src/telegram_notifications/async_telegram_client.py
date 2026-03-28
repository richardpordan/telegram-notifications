"""Telegram API Client for sending notifications."""

import httpx

from .logger import setup_logger

logger = setup_logger(__name__)


class MessageDeliveryError(Exception):
    """Send message endpoint request not returned ok."""

    pass


class AsyncTelegramClient:
    """A client for interacting with the Telegram Bot API.

    Provides async methods for retrieving updates and sending messages
    via the Telegram Bot API using httpx.

    Attributes:
        BASE_URL (str): Template string for constructing Telegram API endpoint
            URLs.
        token (str): The Telegram Bot API token used to authenticate requests.

    Example:
        >>> client = TelegramClient(token="your-bot-token")
        >>> await client.send_message(text="Hello!", chat_id="123456789")

    """

    BASE_URL = "https://api.telegram.org/bot{token}/{method}"

    def __init__(self, token: str):
        """Initialise the TelegramClient with a bot token.

        Args:
            token (str): The Telegram Bot API token, obtained
                from `@BotFather`.

        """
        self.token = token

    def _url(self, method: str) -> str:
        """Construct the full API URL for a given Telegram method.

        Args:
            method (str): The Telegram API method name (e.g. `sendMessage`).

        Returns:
            str: The fully constructed API endpoint URL as a string.

        """
        return self.BASE_URL.format(token=self.token, method=method)

    async def get_updates(self) -> list[dict]:
        """Retrieve pending updates from the Telegram Bot API.

        Fetches all queued updates (e.g. incoming messages) sent to the bot
        since the last acknowledged update. Useful for discovering chat IDs.

        Returns:
            list[dict]: A list of update objects as dicts. Each update contains
            a message with sender info, chat ID, and message text.
            Returns an empty list if there are no pending updates.

        Raises:
            httpx.HTTPStatusError: If the API returns a 4xx or 5xx response.
            httpx.RequestError: If a network error occurs during the request.

        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self._url("getUpdates"))
            response.raise_for_status()
            logger.debug("get_updates: %s", response.status_code)
            data = response.json()

            return data.get("result", [])

    async def send_message(
        self,
        text: str,
        chat_id: str,
    ) -> bool | None:
        """Send a text message to a specified Telegram chat.

        Args:
            text (str): The message content to send. Must be non-empty and no
                longer than 4096 characters.
            chat_id (str): The unique identifier of the target chat or username
                of the target channel (e.g. `"123456789"` or `"@mychannel"`).

        Returns:
            bool | None: The value of the response dict's item with key 'ok'
                or None.

        Raises:
            httpx.HTTPStatusError: If the API returns a 4xx or 5xx response.
            httpx.RequestError: If a network error occurs during the request.

        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._url("sendMessage"),
                json={"chat_id": chat_id, "text": text},
            )
            logger.debug("get_updates: %s", response.status_code)
            response.raise_for_status()
            json_response = response.json()
            if not json_response.get("ok", None):
                raise MessageDeliveryError(
                    "Something went wrong. Message not sent.",
                )

            return json_response.get("ok")
