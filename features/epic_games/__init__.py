import data
import logging
import requests
from bot import client
from datetime import datetime


if "_acive" not in dir():
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    from . import task


# Check for free games on epic games then send them in the chat.
async def check_free_games():
    if not _active:
        return False

    free_games = None

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        channel_id = data.get_free_games_channel_id(guild_id)
        if not channel_id:
            continue

        if not free_games:
            free_games = _get_free_games_links()

        try:
            await _send_free_games_for_guild(guild_id, channel_id, free_games)
        except Exception as e:
            print(e)


def _get_free_games_links():
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
                print(str(e) + " - There is a broken Epic Games link")
                logging.error(str(e) + " - There is a broken Epic Games link")

    except Exception as e:
        print(e)

    return free_games


async def _send_free_games_for_guild(guild_id, channel_id, free_games):
    channel = client.get_channel(channel_id)
    sent_games = data.get_epic_games_names(guild_id)

    for game in free_games:
        if game["name"] in sent_games:
            continue

        message = "The following game is currently available for free on the Epic Games Store:\n"
        role_id = data.get_free_games_role_id(guild_id)
        role_mention = ""
        if role_id:
            role_mention = f"<@&{role_id}>\n"
        await channel.send(
            f"{role_mention}{message}\n<:epic_icon:1101097658153713774> **{game['name']}** - (ends {game['end_date']})\n{game['url']}\n"
        )
        sent_games.append(game["name"])
        data.set_epic_games_names(guild_id, sent_games)
