import data
import features
import logging
import nextcord
import pytube
from .helper import handle_command_exception
from bot import client, ADMINS, HOME_GUILDS
from nextcord import Interaction, Permissions, SlashOption, Embed
from typing import Optional

_logger = logging.getLogger("main")


# help
@client.slash_command(
    name="help",
    description="Display help message",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def help(interaction: Interaction):
    try:
        _logger.info(
            "commands/management: Command 'help' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
        )
        help_message = (
            "Salam, AedanGholam dar khedmate shomast.\n\n"
            "`/settings`: Baraye set kardan tanzimate bot az in command estefade konid.\n"
            "`/set welcome channel id`: in option baraye set kardane id text channel marboot be payam haye khosh amad gooyi mibashad.\n"
            "`/embed`: baraye neveshtan yek payam dar embed ast ke mitavan az rang haye mokhtalef estefade kard."
        )
        await interaction.send(help_message)
    except:
        await handle_command_exception("help", interaction)


@client.slash_command(
    name="add_server",
    description="Grant permission to a new discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def add_server(interaction: Interaction, id: str = SlashOption(required=True)):
    try:
        _logger.info(
            "commands/management: Command 'add_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id}"
        )
        if interaction.user.id not in ADMINS:
            _logger.debug(
                "commands/management: User does not have permission to use command 'add_server' "
                + f"user: '{interaction.user.name}' ({interaction.user.id}) "
                + f"guild: '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction.send(
                "You don't have enough permissions to use this command.", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        server_id = int(id)
        target_guild = client.get_guild(server_id)
        if target_guild is None:
            _logger.debug(f"commands/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.server_add(str(target_guild), server_id)
        if result == server_id:
            _logger.info(
                f"commands/management: Server '{target_guild.name}' ({target_guild.id}) "
                + "has been registered and activated."
            )
            await interaction_response.edit(
                f"Server **{target_guild}** has been registered and activated.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception("add_server", interaction, interaction_response)


@client.slash_command(
    name="edit_server",
    description="Edit permissions of a discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def edit_server(
    interaction: Interaction,
    id: str = SlashOption(required=True),
    active: bool = SlashOption(required=True),
):
    try:
        _logger.info(
            "commands/management: Command 'edit_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id} active:{active}"
        )
        if interaction.user.id not in ADMINS:
            _logger.debug(
                "commands/management: User does not have permission to use command 'edit_server' "
                + f"user: '{interaction.user.name}' ({interaction.user.id}) "
                + f"guild: '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction.send(
                "You don't have enough permissions to use this command.", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        server_id = int(id)
        target_guild = client.get_guild(server_id)
        if target_guild is None:
            _logger.debug(f"commands/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.server_edit(server_id, active)
        if result == server_id:
            active_status = "activated" if active else "deactivated"
            _logger.info(
                f"commands/management: Server '{target_guild.name}' ({target_guild.id}) "
                + f"has been {active_status}."
            )
            await interaction_response.edit(
                f"Server **{target_guild}** has been **{active_status}**.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception("edit_server", interaction, interaction_response)


@client.slash_command(
    name="remove_server",
    description="Remove permission from a discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def remove_server(interaction: Interaction, id: str = SlashOption(required=True)):
    try:
        _logger.info(
            "commands/management: Command 'remove_server' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: id:{id}"
        )
        if interaction.user.id not in ADMINS:
            _logger.debug(
                "commands/management: User does not have permission to use command 'remove_server' "
                + f"user: '{interaction.user.name}' ({interaction.user.id}) "
                + f"guild: '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction.send(
                "You don't have enough permissions to use this command.", ephemeral=True
            )
            return

        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        server_id = int(id)
        target_guild = client.get_guild(server_id)
        if target_guild is None:
            _logger.debug(f"commands/management: Server with id: {id} does not exist.")
            await interaction_response.edit("Server with this id does not exist.")
            return

        result = data.server_remove(server_id)
        if result == server_id:
            _logger.info(
                f"commands/management: Server '{target_guild.name}' ({target_guild.id}) "
                + "has been removed."
            )
            await interaction_response.edit(
                f"Server **{target_guild}** has been removed.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception(
            "remove_server", interaction, interaction_response
        )


@client.slash_command(
    name="customize",
    description="customize bot settings.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def customize(
    interaction: Interaction,
    customize: str = SlashOption(
        name="customize",
        required=True,
        choices=[
            "welcome message",
        ],
    ),
    message: str = SlashOption(
        required=True,
        description="Available variables: {username} and {servername}, **Bold**",
    ),
):
    print(message)
    # try:
    _logger.info(
        "commands/management: Command 'customize' was called by "
        + f"'{interaction.user.name}' ({interaction.user.id}) "
        + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: customize:{customize} message:{message}"
    )
    interaction_response = await interaction.send("Please wait...", ephemeral=True)
    if customize == "welcome message":
        try:
            if message != None:
                result = data.welcome_message_set(interaction.guild_id, message)
                if result == None:
                    _logger.info(
                        "commands/management: Welcome message has been unset "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Welcome message has been unset.",
                    )
                else:
                    await interaction_response.edit("Welcome message has been set.")
                return

            channel_id = int(id)
            channel = client.get_channel(channel_id)
            if interaction.guild_id != channel.guild.id:
                _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                await interaction_response.edit(
                    "Invalid channel ID.",
                )
                return

            result = data.welcome_message_set(interaction.guild_id, channel_id)
            if result == channel_id:
                _logger.info(
                    f"commands/management: Welcome message has been set to {id} "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Welcome channel has been set.",
                )
            else:
                await interaction_response.edit(str(result))
        except:
            _logger.exception(
                f"commands/management: Failed to set welcome message ({id}) "
                + f"in guild ({interaction.guild_id})"
            )
            await interaction_response.edit("Operation failed.")


@client.slash_command(
    name="settings",
    description="Change bot settings.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def settings(
    interaction: Interaction,
    setting: str = SlashOption(
        name="setting",
        required=True,
        choices=[
            "Set DST role id",
            "Set epic games channel id",
            "Set free game role id",
            "Set klei links channel id",
            "Set member count channel id",
            "Set welcome channel id",
        ],
    ),
    id: str = SlashOption(required=True),
):
    try:
        _logger.info(
            "commands/management: Command 'settings' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: setting:{setting} id:{id}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)
        if setting == "Set welcome channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.welcome_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: Welcome channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "Welcome channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return

                result = data.welcome_channel_id_set(interaction.guild_id, channel_id)
                if result == channel_id:
                    _logger.info(
                        f"commands/management: Welcome channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Welcome channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set welcome channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set epic games channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.epic_games_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: epic games channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "epic games channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.epic_games_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"commands/management: epic games channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "epic games channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set epic games channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set klei links channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.klei_links_channel_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: klei links channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "klei links channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.klei_links_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"commands/management: klei links channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "klei links channel has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set klei links channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set free game role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.free_games_role_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: Free game role id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "Free game role has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                role_id = int(id)
                result = data.free_games_role_id_set(interaction.guild_id, role_id)
                if result == role_id:
                    _logger.info(
                        f"commands/management: Free game role id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "Free game role has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set free game role id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set DST role id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.dst_role_id_set(interaction.guild_id, None)
                    if result == None:
                        _logger.info(
                            "commands/management: DST role id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "DST role has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                role_id = int(id)
                result = data.dst_role_id_set(interaction.guild_id, role_id)
                if result == role_id:
                    _logger.info(
                        f"commands/management: DST role id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "DST role has been set.",
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set DST role id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")

        if setting == "Set member count channel id":
            try:
                if id.lower() in ["none", "null", "0", "-"]:
                    result = data.member_count_channel_id_set(
                        interaction.guild_id, None
                    )
                    if result == None:
                        _logger.info(
                            "commands/management: Member count channel id has been unset "
                            + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                        )
                        await interaction_response.edit(
                            "member count channel has been unset.",
                        )
                    else:
                        await interaction_response.edit(str(result))
                    return

                channel_id = int(id)
                channel = client.get_channel(channel_id)
                if interaction.guild_id != channel.guild.id:
                    _logger.debug(f"commands/management: Channel id ({id}) is invalid.")
                    await interaction_response.edit(
                        "Invalid channel ID.",
                    )
                    return
                result = data.member_count_channel_id_set(
                    interaction.guild_id, channel_id
                )
                if result == channel_id:
                    _logger.info(
                        f"commands/management: Member count channel id has been set to {id} "
                        + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                    )
                    await interaction_response.edit(
                        "member count channel has been set.",
                    )
                    # Update member count for the first time
                    await features.member_count.update_member_count_for_guild(
                        interaction.guild_id
                    )
                else:
                    await interaction_response.edit(str(result))
            except:
                _logger.exception(
                    f"commands/management: Failed to set member count channel id ({id}) "
                    + f"in guild ({interaction.guild_id})"
                )
                await interaction_response.edit("Operation failed.")
    except:
        await handle_command_exception("settings", interaction, interaction_response)


def process_discord_message_link(link: str):
    message_guild_id = None
    message_channel_id = None
    message_id = None
    try:
        link_parts = link.removeprefix("https://discord.com/channels/").split("/")
        if len(link_parts) == 3:
            message_guild_id = int(link_parts[0])
            message_channel_id = int(link_parts[1])
            message_id = int(link_parts[2])

        if not message_guild_id or not message_channel_id or not message_id:
            return None

        return {
            "guild_id": message_guild_id,
            "channel_id": message_channel_id,
            "message_id": message_id,
        }
    except:
        return None


@client.slash_command(
    name="set_role_emoji",
    description="Choose an emoji to assign a role",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def set_role_emoji(
    interaction: Interaction,
    message_link: str = SlashOption(name="message_link", required=True),
    emoji_name: str = SlashOption(
        name="emoji_name",
        description="CaSe sEnSiTiVe!",
        required=True,
    ),
    role_name: str = SlashOption(
        name="role_name", description="CaSe sEnSiTiVe!", required=False
    ),
):
    try:
        _logger.info(
            "commands/management: Command 'set_role_emoji' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: "
            + f"message_link:{message_link} emoji_name:{emoji_name} role_name:{role_name}"
        )
        interaction_response = await interaction.send(
            f"Please wait ...", ephemeral=True
        )

        link_parts = process_discord_message_link(message_link)
        if not link_parts:
            await interaction_response.edit("Please enter a valid link of a message.")
            return

        if interaction.guild_id != link_parts["guild_id"]:
            await interaction_response.edit("Message link must be from this server!")
            return

        target_message = None
        try:
            target_message = await client.get_channel(
                link_parts["channel_id"]
            ).fetch_message(link_parts["message_id"])
        except:
            pass
        if not target_message:
            await interaction_response.edit("Please enter a valid link of a message.")
            return

        target_emoji = None
        target_emoji_id = None
        if ":" in emoji_name:  # handle custom emojis like: <:custom_emoji:123456123456>
            emoji_name = emoji_name.split(":")[1]
            target_emoji = nextcord.utils.get(interaction.guild.emojis, name=emoji_name)
            if not target_emoji:
                await interaction_response.edit("Invalid emoji.")
                return
            target_emoji_id = target_emoji.id
        elif len(emoji_name) > 2:  # handle custom emojis like: 'custom_emoji'
            target_emoji = nextcord.utils.get(interaction.guild.emojis, name=emoji_name)
            if not target_emoji:
                await interaction_response.edit("Invalid emoji.")
                return
            target_emoji_id = target_emoji.id
        else:
            target_emoji_id = emoji_name
            target_emoji = target_emoji_id

        if not role_name:  # remove emoji-role pair
            result = data.setrole_emoji_role_pair_remove(
                interaction.guild_id,
                link_parts["channel_id"],
                link_parts["message_id"],
                target_emoji_id,
            )
            if result == target_emoji_id:
                _logger.info(
                    f"commands/management: Emoji ({emoji_name}) and role ({role_name}) unpaired "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Emoji-role pair was removed from this message."
                )
                await target_message.clear_reaction(target_emoji)
                _logger.debug(
                    f"commands/management: All reactions of Emoji ({emoji_name}) have been removed "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                return
            else:
                await interaction_response.edit(result)
                return

        else:  # set emoji-role
            target_role = None
            if "<@&" in role_name:
                role_id = role_name.split("&")[1].replace(">", "")
                target_role = nextcord.utils.get(
                    interaction.guild.roles, id=int(role_id)
                )
            else:
                target_role = nextcord.utils.get(
                    interaction.guild.roles, name=role_name
                )

            if not target_role:
                await interaction_response.edit("Invalid role.")
                return

            result = data.setrole_emoji_role_pair_set(
                interaction.guild_id,
                link_parts["channel_id"],
                link_parts["message_id"],
                target_emoji_id,
                target_role.id,
            )
            if result == target_emoji_id:
                _logger.info(
                    f"commands/management: Emoji ({emoji_name}) and role ({role_name}) paired "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Emoji and role have been paired for this message."
                )
                await target_message.add_reaction(target_emoji)
                _logger.debug(
                    f"commands/management: Added a reaction with Emoji ({emoji_name}) to the target message "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                return
            elif result == "This emoji-role pair already exists.":
                await interaction_response.edit(result)
                await target_message.add_reaction(target_emoji)
                _logger.debug(
                    f"commands/management: Added a reaction with Emoji ({emoji_name}) to the target message "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                return
            else:
                await interaction_response.edit(result)
    except:
        await handle_command_exception(
            "set_role_emoji", interaction, interaction_response
        )


@client.slash_command(
    name="remove_role_message",
    description="Unmark a message as a 'set role by reaction' message",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def remove_role_message(
    interaction: Interaction,
    message_link: str = SlashOption(name="message_link", required=True),
):
    try:
        _logger.info(
            "commands/management: Command 'remove_role_message' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: message_link:{message_link}"
        )
        interaction_response = await interaction.send(
            f"Please wait ...", ephemeral=True
        )

        link_parts = process_discord_message_link(message_link)
        if not link_parts:
            await interaction_response.edit("Please enter a valid link of a message.")
            return

        if interaction.guild_id != link_parts["guild_id"]:
            await interaction_response.edit("Message link must be from this server!")
            return

        result = data.setrole_message_id_remove(
            interaction.guild_id, link_parts["channel_id"], link_parts["message_id"]
        )

        if result == link_parts["message_id"]:
            _logger.info(
                f"commands/management: Message ({link_parts['message_id']}) has been unset as set-role message "
                + f"in '{interaction.guild.name}' ({interaction.guild_id})"
            )
            try:
                target_channel = client.get_channel(link_parts["channel_id"])
                target_message = await target_channel.fetch_message(
                    link_parts["message_id"]
                )
                await target_message.clear_reactions()
                _logger.debug(
                    f"commands/management: All emojis related to the message ({link_parts['message_id']}) "
                    + f"have been removed in '{interaction.guild.name}' ({interaction.guild_id})"
                )
            except:
                pass
            await interaction_response.edit(
                "Done. This message is no longer a 'set role by reaction' message"
            )
            return
        await interaction_response.edit(result)
    except:
        await handle_command_exception(
            "remove_role_message", interaction, interaction_response
        )


# Delete messages
@client.slash_command(
    name="delete",
    description="Delete as many messages as you want",
    default_member_permissions=8,
)
async def delete(
    interaction: Interaction, number: Optional[int] = SlashOption(required=True)
):
    try:
        _logger.info(
            "commands/management: Command 'delete' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: number:{number}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)
        if number <= 0:
            await interaction_response.edit(f"{number} is not allowed")
            return

        await interaction.channel.purge(limit=number)

        report = ""
        if number == 1:
            report = f"{number} message has been deleted."
        else:
            report = f"{number} messages have been deleted."

        _logger.info(
            f"commands/management: {report} Guild: '{interaction.guild.name}' ({interaction.guild_id})"
            + f"Channel: '{interaction.channel.name}' ({interaction.channel_id})"
        )
        await interaction_response.edit(f"{report}")

    except:
        await handle_command_exception("delete", interaction, interaction_response)


@client.slash_command(
    name="youtube",
    description="Send new youtube videos in a channel.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def youtube_notification_set(
    interaction: Interaction,
    link: str = SlashOption(
        required=True, description="A video link from the target youtube channel"
    ),
    channel_id: str = SlashOption(
        required=False,
        description="Target Discord channel id to publish new youtube videos.",
    ),
    custom_message: str = SlashOption(
        required=False,
        description="Use '\\n' for new line. Leave empty to use the default message.",
    ),
):
    try:
        _logger.info(
            "commands/management: Command 'youtube' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) "
            + f"args: link:{link} channel_id:{channel_id}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        if not features.youtube_notify.is_active():
            await interaction_response.edit(
                "Sorry! This feature is unavailable at the moment...",
            )
            return

        if not channel_id:
            channel_id = interaction.channel_id

        channel_id = int(channel_id)
        channel = client.get_channel(channel_id)
        if interaction.guild_id != channel.guild.id:
            _logger.debug(
                "commands/management: Invalid discord channel "
                + "or the specified channel belongs to another guild "
                + f"channel_id: {channel_id}"
            )
            await interaction_response.edit(
                "Invalid channel ID.",
            )
            return

        video = pytube.YouTube(link)
        last_channel_video = features.youtube_notify.get_last_video_of_youtube_channel(
            video.channel_id
        )

        result = data.yt_notif_rule_add(
            interaction.guild_id,
            video.channel_id,
            video.author,
            channel_id,
            last_channel_video["id"],
            custom_message,
        )
        if result == video.channel_id or result == "Updated.":
            _logger.info(
                f"commands/management: {video.author}'s new youtube videos "
                + f"will be posted on '{channel.name}' ({channel.id})"
            )
            await interaction_response.edit(
                f"Done. **{video.author}** new videos will be posted on **{channel.name}**.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception("youtube", interaction, interaction_response)


@client.slash_command(
    name="youtube_remove",
    description="Remove a previously set notification rule.",
    default_member_permissions=Permissions(administrator=True),
    dm_permission=False,
)
async def youtube_notification_remove(
    interaction: Interaction,
    link: str = SlashOption(
        required=True, description="A video link from the target youtube channel"
    ),
):
    try:
        _logger.info(
            "commands/management: Command 'youtube_remove' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: link:{link}"
        )
        interaction_response = await interaction.send("Please wait...", ephemeral=True)

        if not features.youtube_notify.is_active():
            await interaction_response.edit(
                "Sorry! This feature is unavailable at the moment...",
            )
            return

        video = pytube.YouTube(link)

        result = data.yt_notif_rule_remove(interaction.guild_id, video.channel_id)
        if result == video.channel_id:
            _logger.info(
                f"commands/management: {video.author}'s new youtube videos will no longer "
                + f"be posted on '{interaction.guild.name}' ({interaction.guild_id})"
            )
            await interaction_response.edit(
                f"You will no longer receive new videos from **{video.author}**.",
            )
        else:
            await interaction_response.edit(str(result))
    except:
        await handle_command_exception(
            "youtube_remove", interaction, interaction_response
        )
