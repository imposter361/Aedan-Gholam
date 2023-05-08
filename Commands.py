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


# Delete messages
@client.slash_command(name = "delete",description = "Delete how many messages you want", default_member_permissions = 8)
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

#about Aedan Team
@client.slash_command(name= "team", description = "About Aedan Team")
async def team(interaction: Interaction):
    try:
        team = "<:Aedan_logo:1103676392606007356> Bunch of friends gathered together as a team:\n\nEhsan 👨‍💻\nHossein(Moz) 💃\nBagher 🫰\nHossein(Defalcator) 🪡\nAli 🪃\nSina 🧻\n"
        await interaction.response.send_message(team)
    except Exception as e:
        print(str(e) + "Exception happend in team.")
        logging.error(str(e) + "Exception happend in team.")

#about Adean Gholam
@client.slash_command(name= "about", description = "About Gholam")
async def about(interaction: Interaction):
    try:
        Ali = client.get_user(620593942559326265)
        guild_name = client.get_guild(899023632204980324)
        about = f"Gholamam v{Bot_version} az **{guild_name}**\nSaakhte daste aghamoon {Ali.mention} kheyli chakerim."
        await interaction.response.send_message(about)
    except Exception as e:
        print(str(e) + "Exception happend in about.")
        logging.error(str(e) + "Exception happend in about.")


#Hekmat
@client.slash_command(name= "hekmat", description = "Yek Hekmat az Nahj al-balagha")
async def hekmat(interaction: Interaction):
    number = random.randrange(1,481)
    try:
        url = f"https://alimaktab.ir/json/wisdom/?n={number}"
        response = requests.get(url)
        response_json = response.json()

        arabic =response_json['main']
        farsi = response_json['ansarian']
        hekmat = "حکمت " + str(number) + ": " + arabic + "\n\n" + farsi
        new_string = hekmat.replace("[", "").replace("]", "")

        def remove_html(text):
            clean = re.compile('<.*?>')
            return re.sub(clean, '', text)

        clean_text = remove_html(new_string)

        await interaction.response.send_message(clean_text)

    except Exception as e:
        print(str(e) + "Exception happend in hekmat.")
        logging.error(str(e) + "Exception happend in hekmat.")


#play command
voice_clients=[]
next_and_previous_requests = []
@client.slash_command(name = "play", description= "Select a singer or bot plays random.")
async def play(interaction: Interaction, query: Optional[str] = SlashOption(required=False)):
    if interaction.user.voice is None:
        await interaction.send("You need to be in a voice channel to use this command.", ephemeral= True)
        return
    voice_channel = interaction.user.voice.channel
    if voice_channel is not None:
        interaction_response = await interaction.send("Queuing...")
        # create playlist
        playlist = []
        with open("Tracks.txt", "r") as file:
            for line in file.readlines():
                index = random.randint(0, len(playlist))
                playlist.insert(index , line.strip())

        # apply user query to the playlist
        if query is not None:
            playlist2 = []
            for link in playlist:
                if query.lower() in str(link).lower():
                    playlist2.append(link)
            playlist = playlist2

        try:
            voice_client = await voice_channel.connect()
            voice_clients.append(voice_client)
            next_and_previous_requests.append({"guild_id" : voice_client.guild.id , "next" : False, "previous" : False})
            index = 0
            while index <= len(playlist)-1:
                audio_source = FFmpegPCMAudio(playlist[index])
                voice_client.play(audio_source)
                command = f"ffprobe -i {playlist[index]} -show_entries format=duration -v quiet"
                duration = subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').split("\n")[1].split("=")[1].split(".")[0]
                embed = nextcord.Embed(description = playlist[index] + " - " + str(int(int(duration) / 60)) + ":" + "{:02d}".format(int(duration) % 60))
                await interaction_response.edit(f"Playing track {index+1} of {len(playlist)}", embed = embed)
                while voice_client.is_playing():
                    for request in next_and_previous_requests:
                        if request["guild_id"] == voice_client.guild.id:
                            if request["next"] == True:
                                voice_client.stop()
                                request["next"] = False
                                break
                            if request["previous"] == True:
                                voice_client.stop()
                                request["previous"] = False
                                index -= 2
                                break
                    await asyncio.sleep(1)
                index += 1
                if index < 0:
                    index = 0
            await voice_client.disconnect()
            await interaction_response.edit(f"End of the playlist {index} of {len(playlist)}", embed = None)
        except Exception as e:
            print(e)
        finally:
            for request in next_and_previous_requests:
                if request["guild_id"] == voice_client.guild.id:
                    next_and_previous_requests.remove(request)
                    break
            for item in voice_clients:
                if item.guild.id == voice_client.guild.id:
                    voice_clients.remove(item)
                    break

    else:
        await interaction.send("You need to be in a voice channel to use this command.", ephemeral= True)



@client.slash_command()
async def next(interaction: Interaction):
    if interaction.user.voice is None:
        await interaction.send("Bot needs to be in a voice channel to use this command.", ephemeral= True)
        return
    for next_request in next_and_previous_requests:
        if next_request["guild_id"] == interaction.guild_id:
            next_request["next"] = True
            answer = await interaction.send("Skipped")
            await asyncio.sleep(5)
            await answer.delete()
            return
    await interaction.send("You can't skip nothing idiot", ephemeral= True)



@client.slash_command()
async def previous(interaction: Interaction):
    if interaction.user.voice is None:
        await interaction.send("Bot needs to be in a voice channel to use this command.", ephemeral= True)
        return
    for request in next_and_previous_requests:
        if request["guild_id"] == interaction.guild_id:
            request["previous"] = True
            answer = await interaction.send("Here we go again!")
            await asyncio.sleep(5)
            await answer.delete()
            return
    await interaction.send("You can't return nothing idiot", ephemeral= True)


#Stop command
@client.slash_command()
async def stop(interaction: Interaction):
    if interaction.user.voice is None:
        await interaction.send("Bot needs to be in a voice channel to use this command.", ephemeral= True)
        return
    for voice_client in voice_clients:
        if voice_client.guild.id == interaction.guild_id:
            await voice_client.disconnect()
            await interaction.send("Stopped")

def setup_Commands(bot):
    bot.event(hafez)
    bot.event(delete)
    bot.event(team)
    bot.event(about)
    bot.event(play)
    bot.event(stop)