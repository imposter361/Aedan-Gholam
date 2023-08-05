from bot import client
from version import VERSION


if "_acive" not in dir():
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True


async def gholametam(message):
    if not _active:
        return False

    lower_message = str(message.content).lower()
    if ("gholam") in lower_message:
        if message.author != client.user:
            await message.reply(f"Gholametam v{VERSION}")
            return True
    return False
