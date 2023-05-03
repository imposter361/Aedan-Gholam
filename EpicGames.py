from bot import *

# Run the task every 12 hours
@tasks.loop(hours=12)  
async def check_discounts():
    await client.wait_until_ready()
    channel = client.get_channel(int(EPIC_CHANNEL))
    # Make a request to the Epic Games
    response = requests.get(f'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US&' \
                            f'spaceId=1af6c7f8a3624b1788eaf23175fdd16f&' \
                            f'redirectUrl=https%3A%2F%2Fwww.epicgames.com%2Fstore%2Fen-US%2F&' \
                            f'key=da1563f4abe7480fb43364b7d30d9a7b&' \
                            f'promoId=freegames')
    response_json = response.json()

    # Find all the games that are currently free
    for game in response_json['data']['Catalog']['searchStore']['elements']:
        if game['price']['totalPrice']['discountPrice'] == 0:
            try:
                end_date = datetime.strptime(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                if game['productSlug'] and ['title']:
                    end_date_str = end_date.strftime('%b %d, %Y')
                    game_name = game['title']
                    game_link = f"https://launcher.store.epicgames.com/en-US/p/{game['productSlug']}"
                    with open(GAMES_FILE, "a+") as file:
                        file.seek(0)
                        sent_games = [line.strip() for line in file.readlines()]
                        file.close()
                    if game_name not in sent_games:
                        message = "The following game is currently available for free on the Epic Games Store:\n"
                        await channel.send(f"<@&1101090907752771595>\n {message}\n<:epic_icon:1101097658153713774> **{game_name}** - (ends {end_date_str})\n{game_link}\n")
                        with open(GAMES_FILE, "a") as file:
                            file.write(game_name + "\n")
            except Exception as e:
                print(str(e) + " - There is a broken Epic game link") # log

def setup_check_discounts(bot):
    bot.event(check_discounts)