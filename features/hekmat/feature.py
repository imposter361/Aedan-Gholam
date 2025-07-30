import aiohttp
import logging
import re

_logger = logging.getLogger("main")


if "_active" not in dir():  # Run once
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
        url = f"https://alimaktab.ir/wp-json/content/v1/wisdom?n={number}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception()
                response_json = await resp.json()

        arabic = response_json["main"]
        farsi = response_json["translations"]["ansarian"]
        hekmat = "حکمت " + str(number) + ": " + arabic + "\n\n" + farsi
        new_string = hekmat.replace("[", "").replace("]", "")

        clean_text = remove_html(new_string)
        clean_text = clean_text.replace("&raquo;", "»")
        clean_text = clean_text.replace("&laquo;", "«")
        result = clean_text
    except:
        _logger.exception("features/hekmat: Failed to get a hekmat.")

    return result


def remove_html(text):
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)
