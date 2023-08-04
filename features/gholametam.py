from bot import client
from version import VERSION


def gholametam(message):
    lower_message = str(message.content).lower()
    if ("gholam") in lower_message:
        if message.author != client.user:
            return f"Gholametam v{VERSION}"
    return None
