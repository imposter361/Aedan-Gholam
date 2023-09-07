import data
import features
import logging
import nextcord
from .feature import is_active
from commands.helper import handle_command_exception
from bot import client
from nextcord import Interaction, Permissions, SlashOption

_logger = logging.getLogger("main")


def _process_discord_message_link(link: str):
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
            "features/management: Command 'set_role_emoji' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: "
            + f"message_link:{message_link} emoji_name:{emoji_name} role_name:{role_name}"
        )
        if not is_active() or not features.set_role.is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        interaction_response = await interaction.send(f"Please wait...", ephemeral=True)

        link_parts = _process_discord_message_link(message_link)
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
                    f"features/management: Emoji ({emoji_name}) and role ({role_name}) unpaired "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Emoji-role pair was removed from this message."
                )
                await target_message.clear_reaction(target_emoji)
                _logger.debug(
                    f"features/management: All reactions of Emoji ({emoji_name}) have been removed "
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
                    f"features/management: Emoji ({emoji_name}) and role ({role_name}) paired "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                await interaction_response.edit(
                    "Emoji and role have been paired for this message."
                )
                await target_message.add_reaction(target_emoji)
                _logger.debug(
                    f"features/management: Added a reaction with Emoji ({emoji_name}) to the target message "
                    + f"in '{interaction.guild.name}' ({interaction.guild_id})"
                )
                return
            elif result == "This emoji-role pair already exists.":
                await interaction_response.edit(result)
                await target_message.add_reaction(target_emoji)
                _logger.debug(
                    f"features/management: Added a reaction with Emoji ({emoji_name}) to the target message "
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
            "features/management: Command 'remove_role_message' was called by "
            + f"'{interaction.user.name}' ({interaction.user.id}) "
            + f"in '{interaction.guild.name}' ({interaction.guild_id}) args: message_link:{message_link}"
        )
        if not is_active() or not features.set_role.is_active():
            _logger.info(
                "features/management: This feature is not active. Command dismissed."
            )
            await interaction.send(
                f"Sorry! This feature is unavailable at the moment...", ephemeral=True
            )
            return

        interaction_response = await interaction.send(f"Please wait...", ephemeral=True)

        link_parts = _process_discord_message_link(message_link)
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
                f"features/management: Message ({link_parts['message_id']}) has been unset as set-role message "
                + f"in '{interaction.guild.name}' ({interaction.guild_id})"
            )
            try:
                target_channel = client.get_channel(link_parts["channel_id"])
                target_message = await target_channel.fetch_message(
                    link_parts["message_id"]
                )
                await target_message.clear_reactions()
                _logger.debug(
                    f"features/management: All emojis related to the message ({link_parts['message_id']}) "
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
