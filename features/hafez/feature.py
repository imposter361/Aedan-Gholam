import aiohttp
import logging

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
    poem = None
    raw_response = None

    async with aiohttp.ClientSession() as session:
        url = "https://c.ganjoor.net/beyt-xml.php?n=1&a=1&p=2"
        async with session.get(url) as response:
            if response.status != 200:
                return None
            raw_response = await response.content.read()

    xml = raw_response
    m1 = xml.split(b"<m1>")[1].split(b"</m1>")[0].decode("utf-8")
    m2 = xml.split(b"<m2>")[1].split(b"</m2>")[0].decode("utf-8")
    poet = xml.split(b"<poet>")[1].split(b"</poet>")[0].decode("utf-8")
    total_poem = xml.split(b"<url>")[1].split(b"</url>")[0].decode("utf-8")
    up = "🖊️"
    poem = f"{m1}\n{m2}\n\n{up} [{poet}]({total_poem})"

    return poem
