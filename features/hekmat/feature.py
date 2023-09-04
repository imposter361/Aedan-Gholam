import aiohttp
import json
import logging
import re

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'hekmat'")


async def get_hekmat_text(number: int):
    hekmat = None
    raw_response = None

    async with aiohttp.ClientSession() as session:
        url = f"https://alimaktab.ir/json/wisdom/?n={number}"
        async with session.get(url) as response:
            if response.status != 200:
                return None
            raw_response = await response.content.read()

    response_json = json.loads(str(raw_response, encoding="utf-8"))

    arabic = response_json["main"]
    farsi = response_json["ansarian"]
    hekmat = "حکمت " + str(number) + ": " + arabic + "\n\n" + farsi
    hekmat = hekmat.replace("[", "").replace("]", "")

    def remove_html(text):
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    hekmat = remove_html(hekmat)
    hekmat = hekmat.replace("&raquo;", "»")
    hekmat = hekmat.replace("&laquo;", "«")

    return hekmat