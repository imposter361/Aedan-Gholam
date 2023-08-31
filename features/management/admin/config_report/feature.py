import nextcord
from bot import client
from datetime import datetime


def generate_refined_config_text(input, guild_id):
    guild = client.get_guild(guild_id)
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    result = f"{input['name']}\n"
    result = result + time + "\n\n"

    if input.get("welcome_channel_id"):
        welcome_channel = client.get_channel(input["welcome_channel_id"])
        if welcome_channel:
            result = (
                result
                + f"Welcome channel: {welcome_channel.name} ({welcome_channel.id})\n"
            )

    if input.get("welcome_message"):
        result = result + f"Custom welcome message: \"{input['welcome_message']}\"\n"
    result = result + "\n"

    if input.get("member_count_channel_id"):
        member_count_channel = client.get_channel(input["member_count_channel_id"])
        if member_count_channel:
            result = (
                result
                + f"Member count channel: {member_count_channel.name} ({member_count_channel.id})\n\n"
            )

    if input.get("epic_games_channel_id"):
        epic_games_channel = client.get_channel(input["epic_games_channel_id"])
        if epic_games_channel:
            result = (
                result
                + f"Epic games channel: {epic_games_channel.name} ({epic_games_channel.id})\n"
            )

    if input.get("free_games_role_id"):
        free_game_role = nextcord.utils.get(guild.roles, id=input["free_games_role_id"])
        if free_game_role:
            result = (
                result
                + f"Free games role: {free_game_role.name} ({free_game_role.id})\n"
            )
    result = result + "\n"

    if input.get("klei_links_channel_id"):
        klei_links_channel = client.get_channel(input["klei_links_channel_id"])
        if klei_links_channel:
            result = (
                result
                + f"Klei links channel: {klei_links_channel.name} ({klei_links_channel.id})\n"
            )

    if input.get("dst_role_id"):
        dst_role = nextcord.utils.get(guild.roles, id=input["dst_role_id"])
        if dst_role:
            result = result + f"DST role: {dst_role.name} ({dst_role.id})\n"
    result = result + "\n"

    if input.get("set_role_by_reaction_messages"):
        rule_number = 0
        for key in input["set_role_by_reaction_messages"].keys():
            rule_number = rule_number + 1
            result = (
                result
                + f"Set role message link {rule_number}: https://discord.com/channels/{guild_id}/{key}\n"
            )
            emoji_role_dict = input["set_role_by_reaction_messages"][key].get(
                "emoji_role_dict"
            )
            if not emoji_role_dict:
                continue
            result = result + f"Set role message rules {rule_number}:\n"
            for emoji_id in emoji_role_dict:
                emoji_name = None
                if len(emoji_id) <= 2:
                    emoji_name = emoji_id
                else:
                    emoji_name = nextcord.utils.get(guild.emojis, id=int(emoji_id)).name
                role = nextcord.utils.get(guild.roles, id=emoji_role_dict[emoji_id])
                result = result + f"    {emoji_name} --> {role.name}\n"
            result = result + "\n"

    if input.get("yt_notif_rules"):
        rule_number = 0
        for key in input["yt_notif_rules"].keys():
            rule_number = rule_number + 1
            youtube_channel_name = input["yt_notif_rules"][key]["name"]
            discord_channel_name = client.get_channel(
                input["yt_notif_rules"][key]["discord_channel_id"]
            ).name

            result = (
                result
                + f"Youtube channels rule {rule_number}:\n"
                + f"    Youtube channel name: {youtube_channel_name}\n"
                + f"    Discord channel name: {discord_channel_name}\n"
            )
            custom_message = input["yt_notif_rules"][key].get("custom_text_message")
            if custom_message:
                result = result + f"    Custom message: {custom_message}\n"
            result = result + "\n"

    return result
