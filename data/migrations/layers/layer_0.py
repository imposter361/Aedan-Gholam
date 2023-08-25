import json
import logging
import nextcord
from bot import client

_logger = logging.getLogger("main")


async def apply_layer_0(data_file):
    _logger.info("data/migrations/layer_0: Applying migration.")

    with open(data_file, "r") as file:
        data = json.load(file)

    # Base form
    new_data = {"data-version": 1, "servers": {}}

    for server in data:
        _logger.info(
            f"data/migrations/layer_0: Migrating guild {server['server_id']} '{server['name']}'"
        )
        # Populate servers fixed properties (IDs, names and active status)
        new_data["servers"][str(server["server_id"])] = {
            "name": server["name"],
            "active": server["active"],
        }

        # Bring unmodified parts of servers' data
        new_server = new_data["servers"][str(server["server_id"])]

        if server.get("dst_role_id"):
            new_server["dst_role_id"] = server["dst_role_id"]

        if server.get("epic_games"):
            new_server["epic_games"] = server["epic_games"]

        if server.get("epic_games_channel_id"):
            new_server["epic_games_channel_id"] = server["epic_games_channel_id"]

        if server.get("free_games_role_id"):
            new_server["free_games_role_id"] = server["free_games_role_id"]

        if server.get("klei_links"):
            new_server["klei_links"] = server["klei_links"]

        if server.get("klei_links_channel_id"):
            new_server["klei_links_channel_id"] = server["klei_links_channel_id"]

        if server.get("member_count_channel_id"):
            new_server["member_count_channel_id"] = server["member_count_channel_id"]

        if server.get("welcome_channel_id"):
            new_server["welcome_channel_id"] = server["welcome_channel_id"]

        if server.get("welcome_message"):
            new_server["welcome_message"] = server["welcome_message"]

        if server.get("yt_notif_rules"):
            new_server["yt_notif_rules"] = server["yt_notif_rules"]

        # Populate modified parts of servers' data
        # set-role messages
        if not server.get("set_role_message_id") or not server.get("set_role_emoji"):
            continue

        message_id = server["set_role_message_id"]
        guild_id = server["server_id"]

        guild = None
        try:
            guild = client.get_guild(guild_id)
        except:
            pass
        if not guild:
            _logger.warning(
                f"data/migrations/layer_0: Migrating guild {server['server_id']} "
                + "-> Unable to migrate set-role message."
            )
            continue

        # Find channel id of the set-role message (look channels one by one)
        setrole_message_key = None
        for channel in guild.channels:
            message = None
            try:
                message = await channel.fetch_message(message_id)
            except:
                pass
            if not message:
                continue
            setrole_message_key = str(channel.id) + "/" + str(message_id)
            new_server["set_role_by_reaction_messages"] = {
                setrole_message_key: {"emoji_role_dict": {}}
            }
            break

        if not setrole_message_key:
            _logger.warning(
                f"data/migrations/layer_0: Migrating guild {server['server_id']} "
                + "-> Unable to migrate set-role message."
            )
            continue

        # emoji-role pairs
        new_emoji_role_dict = new_server["set_role_by_reaction_messages"][
            setrole_message_key
        ]["emoji_role_dict"]
        for key in server["set_role_emoji"]:
            emoji_id = None
            if len(key) <= 2:
                emoji_id = key
            else:
                emoji = None
                try:
                    emoji = nextcord.utils.get(guild.emojis, name=key)
                except:
                    pass
                if not emoji:
                    _logger.warning(
                        f"data/migrations/layer_0: Migrating guild {server['server_id']} "
                        + f"-> Unable to migrate emoji-role pair with emoji '{key}'"
                    )
                    continue
                emoji_id = emoji.id

            role = None
            try:
                role = nextcord.utils.get(
                    guild.roles, name=server["set_role_emoji"][key]
                )
            except:
                pass
            if not role:
                _logger.warning(
                        f"data/migrations/layer_0: Migrating guild {server['server_id']} "
                        + f"-> Unable to migrate emoji-role pair with role '{server['set_role_emoji'][key]}'"
                    )
                continue

            new_emoji_role_dict[emoji_id] = role.id

    # update the file
    with open(data_file, "w") as file:
        file.write(json.dumps(new_data, indent=4, sort_keys=True))

    _logger.info("data/migrations/layer_0: Migration has been applied.")
