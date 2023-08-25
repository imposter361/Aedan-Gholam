import logging
import random
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


responses = [
    f"Yes sir! v{VERSION}",
    f"Jooooon?! v{VERSION}",
    f"ما الأمر؟! v{VERSION}",
    f"Gholametam v{VERSION}",
    f"Command me! v{VERSION}",
    f"Amri basheh? v{VERSION}",
    f"أنا بخدمتکم! v{VERSION}",
    f"Keyli nokarim v{VERSION}",
    f"Dar khedmatam v{VERSION}",
    f"Kheyli chakeram v{VERSION}",
    f"در خدمت‌گزاری حاضرم! v{VERSION}",
]


async def gholametam(message: Message):
    if not _active:
        return False

    if message.author.bot:
        return

    lower_message = str(message.content).lower()
    if "gholam" in lower_message or "غلام" in lower_message:
        if message.author != client.user:
            index = random.randrange(0, len(responses))
            responses = responses[index]
            await message.reply(responses)
            return True
    return False
