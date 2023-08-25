import data
import logging
from bot import client

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("features: Feature has been activated: 'member_count'")
    from . import task


async def update_member_count():
    if not _active:
        return False

    _logger.debug("features/member_count: Running member count updater task...")

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue
        if data.member_count_channel_id_get(guild_id) == None:
            continue

        try:
            members_count_channel = client.get_channel(
                data.member_count_channel_id_get(guild_id)
            )
            guild = members_count_channel.guild
            name = "Total members: " + str(guild.member_count)
            await members_count_channel.edit(name=name)
            _logger.debug(
                f"features/member_count: « {guild.member_count} » "
                + f"members are in '{str(guild)}' ({guild.id})"
            )
        except:
            _logger.exception(
                "features/member_count: Failed to update member count for "
                + f"guild ({guild_id})"
            )
