from __future__ import annotations

import discord
import typing

from discord import app_commands
from discord.ext import commands

from src.discord_bot.modals.decodead import AnonMSGButton

if typing.TYPE_CHECKING:
    from src.discord_bot.bot import DiscordBot


@app_commands.guild_only()
class DecoDead(commands.GroupCog, group_name="decodead", description="DECODEAD Commands"):
    def __init__(self, bot: DiscordBot):
        self.bot: DiscordBot = bot

    # -- Commands / Events -- #

    @app_commands.command(
        name="set_anon_message",
        description="Set an anonymous message modal for a specific channel.",
    )
    @app_commands.describe(
        channel="The channel to set the anonymous message modal for.",
    )
    async def set_anon_message(
        self, interaction: discord.Interaction, channel: discord.TextChannel | discord.Thread
    ) -> None:
        if not await self.bot.perms_check(interaction=interaction, perms_level=1):
            await interaction.response.send_message(
                embed=self.bot.missing_perms_embed(interaction), ephemeral=True, delete_after=10
            )
            return

        embed: discord.Embed = discord.Embed(
            title="Message Anonymously",
            description="Pressing the button will allow you to send an anonymous message to designated channel.",
            color=discord.Color.random(),
        )

        button_view = AnonMSGButton(bot=self.bot, channel=channel)
        await interaction.response.send_message(embed=embed, view=button_view)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log_bot(f"{self.__class__.__name__} cog file loaded.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DecoDead(bot=bot))
