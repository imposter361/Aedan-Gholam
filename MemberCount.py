import nextcord
from bot import *


# Update member count every 11 minutes
@tasks.loop(minutes=11)
async def member_count():
    members_count_channel = client.get_channel(int(MEMBER_COUNT_CH))
    name = "Total members: " + str(members_count_channel.guild.member_count)
    await members_count_channel.edit(name=name)
    print(f'Total members is now {name}')
    logging.info(f'Total members is now {name}')


def setup_MemberCount(bot):
    bot.event(member_count)