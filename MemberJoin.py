import nextcord
from bot import *


# send welcome message for new members:
@client.event
async def on_member_join(member):
    if str(member.guild.id) in SUBSCRIPTIONS and SUBSCRIPTIONS[str(member.guild.id)]:
        guild = member.guild
        channel = client.get_channel(int(WELCOME_CH))
        author_profile_pic = member.avatar
        embed = nextcord.Embed()
        embed.set_image(url=author_profile_pic)
        await channel.send(f"Salam {member.mention} be **{guild}** khosh oomadi!\n", embed=embed)
        logging.info(f"{member.mention} joined {guild}.")

def setup_on_member_join(bot):
    bot.event(on_member_join)