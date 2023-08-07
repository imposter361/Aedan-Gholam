import logging
from bot import client
from data import get_member_count_channel_id, get_subscriptions

_logger = logging.getLogger("main")


if "_acive" not in dir():  # Run once
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    _logger.debug("Feature has been activated: 'member_count'")
    from . import task


async def update_member_count():
    if not _active:
        return False

    _logger.debug("Running member count updater task...")

    subscriptions = get_subscriptions()
    for guild_id in subscriptions:
        if subscriptions[guild_id] == False:
            continue
        if get_member_count_channel_id(guild_id) == None:
            continue

        try:
            members_count_channel = client.get_channel(
                get_member_count_channel_id(guild_id)
            )
            name = "Total members: " + str(members_count_channel.guild.member_count)
            await members_count_channel.edit(name=name)
            _logger.debug(
                f"« {members_count_channel.guild.member_count} » members are in '{str(members_count_channel.guild)}' "
                + f"({members_count_channel.guild.id})"
            )
        except:
            _logger.exception()
