import logging
from bot import client
from data import get_member_count_channel_id, get_subscriptions


if "_acive" not in dir():
    global _active
    _active = False


def is_active():
    return _active


def activate():
    global _active
    _active = True
    from . import task


async def update_member_count():
    if not _active:
        return False

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
            print(
                f"« {members_count_channel.guild.member_count} » people are in {str(members_count_channel.guild)}"
            )
            logging.info(
                f"« {members_count_channel.guild.member_count} » people are in {str(members_count_channel.guild)}"
            )
        except Exception as e:
            print(e)
