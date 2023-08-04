import data
import logging
import requests
from bot import client
from datetime import datetime
from nextcord.ext import tasks


# Run the task every 12 hours
@tasks.loop(hours=12)
async def check_discounts():
    await client.wait_until_ready()
    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue
        if data.get_free_games_channel_id(guild_id) == None:
            continue

        try:
            channel = client.get_channel(data.get_free_games_channel_id(guild_id))

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
                        game["promotions"]["promotionalOffers"][0]["promotionalOffers"][
                            0
                        ]["endDate"],
                        "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    if not (slug and game["title"]):
                        continue
                    end_date_str = end_date.strftime("%b %d, %Y")
                    game_name = game["title"]
                    game_link = f"https://launcher.store.epicgames.com/en-US/p/{slug}"

                    sent_games = data.get_epic_games_names(guild_id)
                    if game_name not in sent_games:
                        message = "The following game is currently available for free on the Epic Games Store:\n"
                        role_id = data.get_free_games_role_id(guild_id)
                        if role_id:
                            await channel.send(
                                f"<@&{role_id}>\n{message}\n<:epic_icon:1101097658153713774> **{game_name}** - (ends {end_date_str})\n{game_link}\n"
                            )
                        else:
                            await channel.send(
                                f"{message}\n<:epic_icon:1101097658153713774> **{game_name}** - (ends {end_date_str})\n{game_link}\n"
                            )
                        sent_games.append(game_name)
                        data.set_epic_games_names(guild_id, sent_games)

                except Exception as e:
                    print(str(e) + " - There is a broken Epic game link")
                    logging.error(str(e) + " - There is a broken Epic game link")

        except Exception as e:
            print(e)
