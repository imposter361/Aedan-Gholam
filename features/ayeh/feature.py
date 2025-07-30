import json
import logging
from features._shared.helper import aiohttp_get

_logger = logging.getLogger("main")


if "_active" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'ayeh'")


async def get_ayeh_text(number: int):
    result = None
    try:
        url = f"http://api.alquran.cloud/v1/ayah/{number}/editions/quran-uthmani,fa.makarem"
        response = await aiohttp_get(url)
        response_json = json.loads(str(response, encoding="utf-8"))
        text_ayeh = response_json["data"][0]["text"]
        sureh = response_json["data"][0]["surah"]["name"]
        number_ayeh = response_json["data"][0]["numberInSurah"]
        tranlate = response_json["data"][1]["text"]
        text = f"{sureh}  آیه: {number_ayeh}\n\n{text_ayeh}\n\n{tranlate}\n:rose: :rose: :rose: :rose: :rose: :rose: :rose: :rose: "
        result = text

    except Exception as e:
        _logger.exception("features/ayeh: Failed to get an ayeh.")
        if str(e).split()[-1]=="404":
            return "404"
    return result
