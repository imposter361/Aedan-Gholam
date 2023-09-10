import json
import logging
import re
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
    _logger.debug("features: Feature has been activated: 'hekmat'")


async def get_hekmat_text(number: int):
    result = None
    try:
        url = f"https://alimaktab.ir/json/wisdom/?n={number}"
        response = await aiohttp_get(url)
        response_json = json.loads(str(response, encoding="utf-8"))

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
        result = hekmat
    except:
        _logger.exception("features/hekmat: Failed to get a hekmat.")

    return result
