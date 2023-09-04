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


async def update_all_member_counts():
    if not _active:
        return False

    subscriptions = data.get_subscriptions()
    for guild_id in subscriptions:
        if not subscriptions[guild_id]:
            continue

        await _update_member_count_for_guild(guild_id)


async def update_member_count_for_guild(target_guild_id: int):
    if not _active:
        return False

    subscriptions = data.get_subscriptions()
    if not subscriptions.get(target_guild_id):
        return

    await _update_member_count_for_guild(target_guild_id)


async def _update_member_count_for_guild(target_guild_id: int):
    member_count_channel_id = data.member_count_channel_id_get(target_guild_id)
    if not member_count_channel_id:
        return

    try:
        member_count_channel = client.get_channel(member_count_channel_id)
        guild = member_count_channel.guild
        updated_name = "Total members: " + str(guild.member_count)
        if member_count_channel.name != updated_name:
            await member_count_channel.edit(name=updated_name)
            _logger.debug(
                f"features/member_count: Updated: « {guild.member_count} » "
                + f"members are in '{str(guild)}' ({guild.id})"
            )
    except:
        _logger.exception(
            "features/member_count: Failed to update member count for "
            + f"guild ({target_guild_id})"
        )
