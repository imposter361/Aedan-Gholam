import logging
from bot import client
from nextcord import Message
from version import VERSION

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'gholametam'")


async def gholametam(message: Message):
    if not _active:
        return False

    lower_message = str(message.content).lower()
    if "gholam" in lower_message or "غلام" in lower_message:
        if message.author != client.user:
            await message.reply(f"Gholametam v{VERSION}")
            return True
    return False
