from bot import *

#Hafez
@client.slash_command(name= "hafez", description = "Fall Migholi ?!")
async def hafez(interaction: Interaction):
    try:
        url = 'https://c.ganjoor.net/beyt-xml.php?n=1&a=1&p=2'
        response = requests.get(url)
        xml = response.content
        m1 = xml.split(b'<m1>')[1].split(b'</m1>')[0].decode('utf-8')
        m2 = xml.split(b'<m2>')[1].split(b'</m2>')[0].decode('utf-8')
        poet = xml.split(b'<poet>')[1].split(b'</poet>')[0].decode('utf-8')
        up = "🖊️"
        poem = f'{m1}\n{m2}\n\n{up} {poet}'
        await interaction.response.send_message(poem)

    except Exception as e:
        print(str(e) + "Exception happend in Fall giri.")
        logging.error(str(e) + "Exception happend in Fall giri.")
        await interaction.response.send_message(f'Bebakhshid saremoon sholooghe dobare test kon!', ephemeral= True)


# delete message
@client.slash_command(default_member_permissions = 8)
async def delete(interaction: Interaction, number: Optional[int] = SlashOption(required=True)):

    try:
        if number <= 0:
            await interaction.response.send_message(f'{number} is not allowed', ephemeral= True)
            return

        await interaction.channel.purge(limit= number)
        if number == 1:
            await interaction.response.send_message(f'{number} message deleted.', ephemeral= True)
            logging.warning(f'{number} message deleted.')
        else:
            await interaction.response.send_message(f'{number} messages have been deleted.', ephemeral= True)
            logging.warning(f'{number} messages have been deleted.')
            
    except Exception as e:
        print(str(e) + "Exception happend in message delete.")
        logging.error(str(e) + "Exception happend in message delete.")


def setup_Commands(bot):
    bot.event(hafez)
    bot.event(delete)