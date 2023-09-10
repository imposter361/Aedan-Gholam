import logging
from features._shared.helper import aiohttp_get

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'hafez'")


async def get_hafez_poem_text():
    result = None
    try:
        url = "https://c.ganjoor.net/beyt-xml.php?n=1&a=1&p=2"
        response = await aiohttp_get(url)

        xml = response
        mesra_1 = xml.split(b"<m1>")[1].split(b"</m1>")[0].decode("utf-8")
        mesra_2 = xml.split(b"<m2>")[1].split(b"</m2>")[0].decode("utf-8")
        poet = xml.split(b"<poet>")[1].split(b"</poet>")[0].decode("utf-8")
        poem_url = xml.split(b"<url>")[1].split(b"</url>")[0].decode("utf-8")
        emoji = "🖊️"
        result = f"{mesra_1}\n{mesra_2}\n\n{emoji} [{poet}]({poem_url})"
    except:
        _logger.exception("features/hafez: Failed to get a poem by Hafez.")

    return result
