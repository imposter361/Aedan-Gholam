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
    f"Yes sir!",
    f"Jooooon?!",
    f"ما الأمر؟!",
    f"Gholametam",
    f"Command me!",
    f"Amri basheh?",
    f"أنا بخدمتکم!",
    f"Dar khedmatam",
    f"Kheyli nokarim",
    f"Kheyli chakeram",
    f"در خدمت‌گزاری حاضرم!",
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
            response = responses[index] + f" V {VERSION}"
            await message.reply(response)
            return True
    return False
