import discord

allowed_channel_ids = [*****************] # origin channel/channels (use , to add more)
special_channel_id = ******************  # destination channel

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.user:  
            return
        
        # Ignore messages sent to bot's private message channel
        if isinstance(message.channel, discord.abc.PrivateChannel):  
            return

        if message.channel.id in allowed_channel_ids:
            channel = self.get_channel(special_channel_id)
            await channel.send(f'* {message.author.display_name} in {message.channel.name}: {message.content}')
            #add{message.guild.name} for server name

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
#your bot's TOKEN goes here
client.run('Your-TOKEN')
