import data
import logging
import requests
from bot import client
from datetime import datetime

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'epic_games'")
    from . import task


# Check for free games on epic games then send them in the chat.
async def check_free_games_for_all_guilds():
    if not _active:
        return False

    free_games = None

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        channel_id = data.epic_games_channel_id_get(guild_id)
        if not channel_id:
            continue

        if not free_games:
            free_games = _get_free_games_links()

        await _send_free_games_for_guild(guild_id, channel_id, free_games)


async def check_free_games_for_guild(guild_id: int):
    if not _active:
        return

    subscriptions = data.get_subscriptions()
    if not subscriptions.get(guild_id):
        return

    channel_id = data.epic_games_channel_id_get(guild_id)
    if not channel_id:
        return

    free_games = _get_free_games_links()
    await _send_free_games_for_guild(guild_id, channel_id, free_games)


def _get_free_games_links():
    _logger.debug("features/epic_games: Getting Epic Games' free games list...")
    free_games = []
    try:
        # Make a request to the Epic Games
        response = requests.get(
            f"https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US&"
            f"spaceId=1af6c7f8a3624b1788eaf23175fdd16f&"
            f"redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fstore%2Fen-US%2F&"
            f"key=da1563f4abe7480fb43364b7d30d9a7b&"
            f"promoId=freegames"
        )
        response_json = response.json()

        # Find all the games that are currently free
        for game in response_json["data"]["Catalog"]["searchStore"]["elements"]:
            if game["price"]["totalPrice"]["discountPrice"] != 0:
                continue

            try:
                slug = None
                try:
                    slug = game["productSlug"]
                except Exception:
                    pass
                try:
                    slug = game["catalogNs"]["mappings"][0]["pageSlug"]
                except Exception:
                    pass

                if not game["promotions"]:
                    continue

                if not game["promotions"]["promotionalOffers"]:
                    continue

                end_date = datetime.strptime(
                    game["promotions"]["promotionalOffers"][0]["promotionalOffers"][0][
                        "endDate"
                    ],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                )

                if not slug or not game["title"]:
                    continue

                end_date_str = end_date.strftime("%b %d, %Y")
                game_name = game["title"]
                game_link = f"https://launcher.store.epicgames.com/en-US/p/{slug}"

                free_games.append(
                    {"name": game_name, "end_date": end_date_str, "url": game_link}
                )

            except Exception as e:
                _logger.debug(
                    "features/epic_games: There is a broken Epic Games link: " + str(e)
                )

    except:
        _logger.exception(
            "features/epic_games: Failed to get free games list from Epic Games."
        )

    return free_games


async def _send_free_games_for_guild(guild_id, channel_id, free_games):
    try:
        channel = client.get_channel(channel_id)
        if not channel:
            _logger.debug(
                "features/epic_games: Failed to get channel with id of: "
                + f"{channel_id} in guild: {guild_id}"
            )
            return

        sent_games = data.epic_games_names_get(guild_id)

        for game in free_games:
            if game["name"] in sent_games:
                continue

            message = "The following game is currently available for free on the Epic Games Store:\n"
            role_id = data.free_games_role_id_get(guild_id)
            role_mention = ""
            if role_id:
                role_mention = f"<@&{role_id}>\n"
            await channel.send(
                f"{role_mention}{message}\n<:epic_icon:1101097658153713774> **{game['name']}** - (ends {game['end_date']})\n{game['url']}\n"
            )
            sent_games.append(game["name"])
            data.epic_games_names_set(guild_id, sent_games)
    except:
        _logger.exception(
            f"features/epic_games: Failed to send free Epic games ({free_games}) "
            + f"to the respective channel ({channel_id}) at guild ({guild_id})"
        )
