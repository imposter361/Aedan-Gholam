import json
import logging
import os

_logger = logging.getLogger("main")


_DATA_FILE = "data/data.json"
_data = None


def _init():
    if not os.path.exists(_DATA_FILE):
        _logger.debug(
            f"data_interface: Data file does not exist. Creating {_DATA_FILE}"
        )
        with open(_DATA_FILE, "w") as file:
            file.write(json.dumps([]))


def _load():
    _logger.debug(f"data_interface: Loading data from {_DATA_FILE}")
    with open(_DATA_FILE) as file:
        global _data
        _data = json.load(file)


def _save():
    _logger.debug(f"data_interface: Saving data to {_DATA_FILE}")
    with open(_DATA_FILE, "w") as file:
        file.write(json.dumps(_data, indent=4))


_init()
_load()


def get_subscriptions():
    servers = {}
    for item in _data:
        servers[item["server_id"]] = item["active"]
    return servers


def get_server_index(guild_id):
    index = 0
    while index < len(_data):
        if _data[index]["server_id"] == guild_id:
            return index
        index = index + 1
    return -1


def add_server(name, id):
    if get_server_index(id) >= 0:
        return "The server is already registered."
    _data.append(
        {
            "name": name,
            "server_id": id,
            "active": True,
        }
    )
    _save()
    return id


def edit_server(id, active):
    index = get_server_index(id)
    if index == -1:
        return "No server found with this id."
    _data[index]["active"] = active
    _save()
    return id


def remove_server(id):
    index = get_server_index(id)
    if index == -1:
        return "No server found with this id."
    _data.pop(index)
    _save()
    return id


def set_welcome_channel_id(guild_id, channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["welcome_channel_id"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data_interface: Failed to set welcome channel id "
            + f"({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_welcome_channel_id(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["welcome_channel_id"]
    except:
        _logger.debug(
            "data_interface: Could not find welcome_channel_id "
            + f"for guild_id:{guild_id}. Returning None"
        )
        return None


def set_welcome_message(guild_id, channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["welcome_message"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data_interface: Failed to set welcome message "
            + f"({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_welcome_message(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["welcome_message"]
    except:
        _logger.debug(
            "data_interface: Could not find welcome_message "
            + f"for guild_id:{guild_id}. Returning None"
        )
        return None


def set_free_games_channel_id(guild_id, channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["free_games_channel_id"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data_interface: Failed to set free games "
            + f"channel id ({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_free_games_channel_id(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["free_games_channel_id"]
    except:
        _logger.debug(
            "data_interface: Could not find free_games_channel_id "
            + f"for guild_id:{guild_id}. Returning None"
        )
        return None


def set_free_games_role_id(guild_id, role_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["free_games_role_id"] = role_id
        _save()
        return role_id
    except Exception as e:
        _logger.exception(
            f"data_interface: Failed to set free games role id ({role_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_free_games_role_id(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["free_games_role_id"]
    except:
        _logger.debug(
            "data_interface: Could not find free_games_role_id "
            + f"for guild_id:{guild_id}. Returning None"
        )
        return None


def set_dst_role_id(guild_id, role_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["dst_role_id"] = role_id
        _save()
        return role_id
    except Exception as e:
        _logger.exception(
            f"data_interface: Failed to set DST role id ({role_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_dst_role_id(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["dst_role_id"]
    except:
        _logger.debug(
            f"data_interface: Could not find dst_role_id for guild_id:{guild_id}. Returning None"
        )
        return None


def set_epic_games_names(guild_id, games):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["epic_games"] = games
        _save()
        return games
    except Exception as e:
        _logger.exception(
            f"data_interface: Failed to set free games names ({games}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_epic_games_names(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["epic_games"]
    except:
        _logger.debug(
            f"data_interface: Could not find epic_games for guild_id:{guild_id}. Returning None"
        )
        return []


def set_klei_links(guild_id, links):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["klei_links"] = links
        _save()
        return links
    except Exception as e:
        _logger.exception(
            f"data_interface: Failed to set klei links ({links}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_klei_links(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["klei_links"]
    except:
        _logger.debug(
            f"data_interface: Could not find klei_links for guild_id:{guild_id}. Returning None"
        )
        return []


def set_member_count_channel_id(guild_id, channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["member_count_channel_id"] = channel_id
        _save()
        return channel_id
    except Exception as e:
        _logger.exception(
            "data_interface: Failed to set member count channel id "
            + f"({channel_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_member_count_channel_id(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["member_count_channel_id"]
    except:
        _logger.debug(
            "data_interface: Could not find member_count_channel_id "
            + f"for guild_id:{guild_id}. Returning None"
        )
        return None


def set_role_message_id(guild_id, message_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["set_role_message_id"] = message_id
        _save()
        return message_id
    except Exception as e:
        _logger.exception(
            "data_interface: Failed to set set-role message id "
            + f"({message_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_role_message_id(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["set_role_message_id"]
    except:
        _logger.debug(
            "data_interface: Could not find set_role_message_id "
            + f"for guild_id:{guild_id}. Returning None"
        )
        return None


def set_role_emoji(guild_id, emoji_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."
        _data[index]["set_role_emoji"] = emoji_id
        _save()
        return emoji_id
    except Exception as e:
        _logger.exception(
            f"data_interface: Failed to set role emoji id ({emoji_id}) for guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_role_emoji(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["set_role_emoji"]
    except:
        _logger.debug(
            "data_interface: Could not find set_role_emoji for "
            + f"guild_id:{guild_id}. Returning None"
        )
        return None


def add_yt_notif_rule(
    guild_id,
    yt_channel_id,
    yt_channel_name,
    discord_channel_id,
    last_video_id,
    custom_message=None,
):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."

        if not _data[index].get("yt_notif_rules"):
            _data[index]["yt_notif_rules"] = {}

        rules = _data[index]["yt_notif_rules"]
        yt_channel_id = str(yt_channel_id)

        if yt_channel_id in rules:
            if rules[yt_channel_id].get("name") != yt_channel_name:
                rules[yt_channel_id]["name"] = yt_channel_name
                _save()
            if (
                rules[yt_channel_id]["discord_channel_id"] == discord_channel_id
                and rules[yt_channel_id]["custom_text_message"] == custom_message
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
            "data_interface: Failed to add youtube notification rule with these parameters: "
            + f"yt_channel_id ({yt_channel_id}), yt_channel_name ({yt_channel_name}), "
            + f"discord_channel_id ({discord_channel_id}), last_video_id ({last_video_id}), "
            + f"custom_message ({custom_message}) "
            + f"in guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def get_yt_notif_rules(guild_id):
    try:
        for item in _data:
            if item["server_id"] == guild_id:
                return item["yt_notif_rules"]
    except Exception:
        _logger.debug(
            "data_interface: Could not find yt_notif_rules for "
            + f"guild_id:{guild_id}. Returning None"
        )
        return None


def set_yt_last_video_id(guild_id, yt_channel_id, yt_channel_name, video_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."

        if not _data[index].get("yt_notif_rules"):
            return "The server has no Youtube notification rules defined."

        rules = _data[index]["yt_notif_rules"]
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
            f"data_interface: Failed to set last youtube video id ({video_id}) "
            + f"for yt_channel_id ({yt_channel_id}), yt_channel_name ({yt_channel_name}), "
            + f"in guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"


def remove_yt_notif_rule(guild_id, yt_channel_id):
    try:
        index = get_server_index(guild_id)
        if index == -1:
            return "No server found with this id."

        if not _data[index].get("yt_notif_rules"):
            _data[index]["yt_notif_rules"] = {}

        rules = _data[index]["yt_notif_rules"]
        yt_channel_id = str(yt_channel_id)

        if yt_channel_id not in rules:
            return "No rule is set for this Youtube channel."

        _data[index]["yt_notif_rules"].pop(yt_channel_id)
        _save()
        return yt_channel_id
    except Exception as e:
        _logger.exception(
            "data_interface: Failed to remove youtube notification rule of yt_channel_id "
            + f"({yt_channel_id}) from guild ({guild_id})"
        )
        return f"Error happened: {str(e)}"
