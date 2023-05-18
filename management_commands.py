from bot import client, ADMINS, HOME_GUILDS
import data
from nextcord import Interaction, Permissions, SlashOption


@client.slash_command(
    name="add_server",
    description="Grant permission to a new discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def add_server(interaction: Interaction, id: str = SlashOption(required=True)):
    if interaction.user.id not in ADMINS:
        await interaction.send(
            "You don't have enough permissions to use this command.", ephemeral=True
        )
        return

    interaction_response = await interaction.send("Please wait...", ephemeral=True)

    server_id = int(id)
    target_guild = client.get_guild(server_id)
    if target_guild is None:
        await interaction_response.edit("Server with this id does not exists.")
        return

    result = data.add_server(str(target_guild), server_id)
    if result == server_id:
        await interaction_response.edit(
            f"Server **{target_guild}** has been registered and activated.",
        )
    else:
        await interaction_response.edit(str(result))


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
    if interaction.user.id not in ADMINS:
        await interaction.send(
            "You don't have enough permissions to use this command.", ephemeral=True
        )
        return

    interaction_response = await interaction.send("Please wait...", ephemeral=True)

    server_id = int(id)
    target_guild = client.get_guild(server_id)
    if target_guild is None:
        await interaction_response.edit("Server with this id does not exists.")
        return

    result = data.edit_server(server_id, active)
    if result == server_id:
        active_status = "activated" if active else "deactivated"
        await interaction_response.edit(
            f"Server **{target_guild}** has been **{active_status}**.",
        )
    else:
        await interaction_response.edit(str(result))


@client.slash_command(
    name="remove_server",
    description="Remove permission from a discord server.",
    default_member_permissions=Permissions(administrator=True),
    guild_ids=HOME_GUILDS,
    dm_permission=False,
)
async def remove_server(interaction: Interaction, id: str = SlashOption(required=True)):
    if interaction.user.id not in ADMINS:
        await interaction.send(
            "You don't have enough permissions to use this command.", ephemeral=True
        )
        return

    interaction_response = await interaction.send("Please wait...", ephemeral=True)

    server_id = int(id)
    target_guild = client.get_guild(server_id)
    if target_guild is None:
        await interaction_response.edit("Server with this id does not exists.")
        return

    result = data.remove_server(server_id)
    if result == server_id:
        await interaction_response.edit(
            f"Server **{target_guild}** has been removed.",
        )
    else:
        await interaction_response.edit(str(result))


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
        choices=["set welcome channel id", "set role message id"],
    ),
    value: str = SlashOption(required=True)
):
    interaction_response = await interaction.send("Please wait...", ephemeral=True)
    if setting == "set welcome channel id":
        try:
            if value.lower() in ["none", "null", "0", "-"]:
                result = data.set_welcome_channel_id(
                    interaction.guild_id, None)
                if result == None:
                    await interaction_response.edit(
                        "Welcome channel has been unset.",
                    )
                else:
                    await interaction_response.edit(str(result))
                return

            message_id = int(value)
            result = data.set_welcome_channel_id(
                interaction.guild_id, message_id)
            if result == message_id:
                await interaction_response.edit(
                    "Welcome channel has been set.",
                )
            else:
                await interaction_response.edit(str(result))
        except Exception as e:
            print(e)
            await interaction_response.edit(str(e))

    # if setting == "set role message id":
    #     try:
    #         if value.lower() in ["none", "null", "0", "-"]:
    #             result = data.set_role_message_id(
    #                 interaction.guild_id, None)
    #             if result == None:
    #                 await interaction_response.edit(
    #                     "Role message has been unset."
    #                 ),
    #             else:
    #                 await interaction_response.edit(str(result))
    #             return

    #         message_id = int(value)
    #         result = data.set_role_message_id(interaction.guild_id, message_id)
    #         if result == message_id:
    #             await interaction_response.edit(
    #                 "Role message has been set.",
    #             )
    #         else:
    #             await interaction_response.edit(str(result))
    #     except Exception as e:
    #         print(e)
    #         await interaction_response.edit(str(e))
