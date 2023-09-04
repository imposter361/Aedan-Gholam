import data.migrations as migrations
import json
import logging
import os
from datetime import datetime

_logger = logging.getLogger("main")


_DATA_VERSION = 1
_DATA_FILE = "data/data.json"

_data = {"data-version": _DATA_VERSION}


if "_data_migration_checked" not in dir():  # Run once
    global _data_migration_checked
    _data_migration_checked = False


def _init():
    if not os.path.exists(_DATA_FILE):
        _logger.debug(f"data: Data file does not exist. Creating {_DATA_FILE}")
        with open(_DATA_FILE, "w") as file:
            file.write(json.dumps(_data))


def _load():
    _logger.debug(f"data: Loading data from {_DATA_FILE}")
    with open(_DATA_FILE) as file:
        global _data
        _data = json.load(file)


def _save():
    _logger.debug(f"data: Saving data to {_DATA_FILE}")
    with open(_DATA_FILE, "w") as file:
        file.write(json.dumps(_data, indent=4, sort_keys=True))


_init()


async def check_for_data_migrations():
    _logger.debug("data: Checking for available data migrations.")
    await migrations.apply_available_migrations(_DATA_FILE, _DATA_VERSION)
    _logger.debug("data: Data migration check has been finished.")
    _load()
    global _data_migration_checked
    _data_migration_checked = True


def backup():
    if not is_ready():
        return

    _logger.info("data: Backing up data file...")
    if not os.path.exists("./data/backups/"):
        os.makedirs("./data/backups/")
    datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"data/backups/data_{datetime_str}_layer_{_DATA_VERSION}.json"
    with open(path, "w") as file:
        file.write(json.dumps(_data, indent=4, sort_keys=True))
    _logger.info(f"data: Backup is ready. Saved to: {path}")


def is_ready():
    return _data_migration_checked


def get_subscriptions():
    if not is_ready():
        return {}

    subscriptions = {}
    servers: dict = _data.get("servers")
    if not servers:
        return subscriptions
    for server_id in servers.keys():
        subscriptions[int(server_id)] = servers[server_id]["active"]
    return subscriptions


def configs_get(guild_id):
    if not is_ready():
        return "Please try again later."
    return server_get(guild_id)


def dst_role_id_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("dst_role_id")


def dst_role_id_set(guild_id, role_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["dst_role_id"] = role_id
        _save()
        return role_id
    except Exception as e:
        _logger.exception(
            f"data: Failed to set DST role id ({role_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def epic_games_channel_id_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("epic_games_channel_id")


def epic_games_channel_id_set(guild_id, channel_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["epic_games_channel_id"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data: Failed to set epic_games_channel_id"
            + f"channel id ({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def epic_games_names_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    games = server.get("epic_games")
    if games:
        return games
    return []


def epic_games_names_set(guild_id, games):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["epic_games"] = games
        _save()
        return games
    except Exception as e:
        _logger.exception(
            f"data: Failed to set free games names ({games}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def free_games_role_id_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("free_games_role_id")


def free_games_role_id_set(guild_id, role_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["free_games_role_id"] = role_id
        _save()
        return role_id
    except Exception as e:
        _logger.exception(
            f"data: Failed to set free games role id ({role_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def klei_links_channel_id_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("klei_links_channel_id")


def klei_links_channel_id_set(guild_id, channel_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["klei_links_channel_id"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data: Failed to set klei_links_channel_id"
            + f"channel id ({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def klei_links_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    links = server.get("klei_links")
    if links:
        return links
    return []


def klei_links_set(guild_id, links):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["klei_links"] = links
        _save()
        return links
    except Exception as e:
        _logger.exception(
            f"data: Failed to set klei links ({links}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def member_count_channel_id_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("member_count_channel_id")


def member_count_channel_id_set(guild_id, channel_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["member_count_channel_id"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data: Failed to set member count channel id "
            + f"({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def server_add(name, id):
    if not is_ready():
        return "Please try again later."

    server = server_get(id)
    if server:
        return "The server is already registered."

    if not _data.get("servers"):
        _data["servers"] = {}

    _data["servers"][str(id)] = {
        "name": name,
        "active": True,
    }
    _save()
    return id


def server_edit(id, active):
    if not is_ready():
        return "Please try again later."

    server = server_get(id)
    if not server:
        return "No server found with this id."

    server["active"] = active
    _save()
    return id


def server_get(guild_id):
    if not is_ready():
        return "Please try again later."

    servers: dict = _data.get("servers")
    if not servers:
        return None
    return servers.get(str(guild_id))


def server_remove(id):
    if not is_ready():
        return "Please try again later."

    server = server_get(id)
    if not server:
        return "No server found with this id."

    _data["servers"].pop(str(id))
    _save()
    return id


def setrole_emoji_role_pair_remove(guild_id, channel_id, message_id, emoji_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        if not server.get("set_role_by_reaction_messages"):
            return 'This message is not marked as a "set role by reaction" message.'

        setrole_messages = server["set_role_by_reaction_messages"]
        target_message_key = str(channel_id) + "/" + str(message_id)

        if not setrole_messages.get(target_message_key):
            return 'This message is not marked as a "set role by reaction" message.'

        if not setrole_messages[target_message_key].get("emoji_role_dict"):
            return "This emoji-role pair does not exist."

        emoji_role_dict = setrole_messages[target_message_key]["emoji_role_dict"]
        if not emoji_role_dict.get(str(emoji_id)):
            return "This emoji-role pair does not exist."

        emoji_role_dict.pop(str(emoji_id))
        _save()
        return emoji_id
    except Exception as e:
        _logger.exception(
            f"data: Failed to remove emoji-role pair with emoji id of "
            + f"({emoji_role_dict}) for message ({message_id}) in guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def setrole_emoji_role_pair_set(guild_id, channel_id, message_id, emoji_id, role_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        if not server.get("set_role_by_reaction_messages"):
            server["set_role_by_reaction_messages"] = {}

        setrole_messages = server["set_role_by_reaction_messages"]
        target_message_key = str(channel_id) + "/" + str(message_id)

        if not setrole_messages.get(target_message_key):
            setrole_messages[target_message_key] = {}

        if not setrole_messages[target_message_key].get("emoji_role_dict"):
            setrole_messages[target_message_key]["emoji_role_dict"] = {}

        emoji_role_dict = setrole_messages[target_message_key]["emoji_role_dict"]
        if emoji_role_dict.get(str(emoji_id)):
            if emoji_role_dict[str(emoji_id)] == role_id:
                return "This emoji-role pair already exists."

        emoji_role_dict[str(emoji_id)] = role_id
        _save()
        return emoji_id
    except Exception as e:
        _logger.exception(
            f"data: Failed to pair emoji ({emoji_id}) and role ({role_id}) "
            + f"for message ({message_id}) in guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def setrole_message_id_remove(guild_id, channel_id, message_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        if not server.get("set_role_by_reaction_messages"):
            return 'This message is not marked as a "set role by reaction" message.'

        setrole_messages = server["set_role_by_reaction_messages"]
        target_message_key = str(channel_id) + "/" + str(message_id)

        if not setrole_messages.get(target_message_key):
            return 'This message is not marked as a "set role by reaction" message.'

        setrole_messages.pop(target_message_key)
        _save()
        return message_id
    except Exception as e:
        _logger.exception(
            "data: Failed to remove set-role message id "
            + f"({message_id}) in channel ({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def setrole_messages_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("set_role_by_reaction_messages")


def welcome_channel_id_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("welcome_channel_id")


def welcome_channel_id_set(guild_id, channel_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["welcome_channel_id"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data: Failed to set welcome_channel_id "
            + f"({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def welcome_message_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("welcome_message")


def welcome_message_set(guild_id, message):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        server["welcome_message"] = message
        _save()
        return message
    except Exception as e:
        _logger.exception(
            "data: Failed to set welcome_message "
            + f"({message}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def yt_last_video_id_set(guild_id, yt_channel_id, yt_channel_name, video_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        if not server.get("yt_notif_rules"):
            return "The server has no Youtube notification rules defined."

        rules = server["yt_notif_rules"]
        yt_channel_id = str(yt_channel_id)

        if yt_channel_id not in rules:
            return "The server has no rules defined for this Youtube channel."

        if rules[yt_channel_id].get("name") != yt_channel_name:
            rules[yt_channel_id]["name"] = yt_channel_name
            _save()
        if rules[yt_channel_id]["last_video_id"] == video_id:
            return "Unchanged."
        else:
            rules[yt_channel_id]["last_video_id"] = video_id
            _save()
            return video_id

    except Exception as e:
        _logger.exception(
            f"data: Failed to set last youtube video id ({video_id}) "
            + f"for yt_channel_id ({yt_channel_id}), yt_channel_name ({yt_channel_name}), "
            + f"in guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def yt_notif_rule_add(
    guild_id,
    yt_channel_id,
    yt_channel_name,
    discord_channel_id,
    last_video_id,
    custom_message=None,
):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        if not server.get("yt_notif_rules"):
            server["yt_notif_rules"] = {}

        rules = server["yt_notif_rules"]
        yt_channel_id = str(yt_channel_id)

        if yt_channel_id in rules:
            if rules[yt_channel_id].get("name") != yt_channel_name:
                rules[yt_channel_id]["name"] = yt_channel_name
                _save()
            if (
                rules[yt_channel_id]["discord_channel_id"] == discord_channel_id
                and rules[yt_channel_id].get("custom_text_message") == custom_message
            ):
                return "This rule already exists."
            else:
                rules[yt_channel_id]["discord_channel_id"] = discord_channel_id
                rules[yt_channel_id]["custom_text_message"] = custom_message
                _save()
                return "Updated."

        rules[yt_channel_id] = {
            "name": yt_channel_name,
            "discord_channel_id": discord_channel_id,
            "last_video_id": last_video_id,
            "custom_text_message": custom_message,
        }
        _save()
        return yt_channel_id
    except Exception as e:
        _logger.exception(
            "data: Failed to add youtube notification rule with these parameters: "
            + f"yt_channel_id ({yt_channel_id}), yt_channel_name ({yt_channel_name}), "
            + f"discord_channel_id ({discord_channel_id}), last_video_id ({last_video_id}), "
            + f"custom_message ({custom_message}) "
            + f"in guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def yt_notif_rule_remove(guild_id, yt_channel_id):
    if not is_ready():
        return "Please try again later."

    try:
        server = server_get(guild_id)
        if not server:
            return "No server found with this id."

        if not server.get("yt_notif_rules"):
            server["yt_notif_rules"] = {}

        rules = server["yt_notif_rules"]
        yt_channel_id = str(yt_channel_id)

        if yt_channel_id not in rules:
            return "No rule is set for this Youtube channel."

        server["yt_notif_rules"].pop(yt_channel_id)
        _save()
        return yt_channel_id
    except Exception as e:
        _logger.exception(
            "data: Failed to remove youtube notification rule of yt_channel_id "
            + f"({yt_channel_id}) from guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def yt_notif_rules_get(guild_id):
    if not is_ready():
        return "Please try again later."

    server = server_get(guild_id)
    if not server:
        return None
    return server.get("yt_notif_rules")
