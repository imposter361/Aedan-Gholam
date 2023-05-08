import nextcord
from bot import *


# Update member count every 11 minutes
@tasks.loop(minutes=11)
async def member_count():
    members_count_channel = client.get_channel(int(MEMBER_COUNT_CH_ID))
    name = "Total members: " + str(members_count_channel.guild.member_count)
    await members_count_channel.edit(name=name)
    print(f'« {members_count_channel.guild.member_count} » people are in the house')
    logging.info(f'« {members_count_channel.guild.member_count} » people are in the house')


def setup_MemberCount(bot):
    bot.event(member_count)