# TsuserverDR, server software for Danganronpa Online based on tsuserver3,
# which is server software for Attorney Online.
#
# Copyright (C) 2016 argoneus <argoneuscze@gmail.com> (original tsuserver3)
#           (C) 2018-22 Chrezm/Iuvee <thechrezm@gmail.com> (further additions)
#           (C) 2022 Tricky Leifa (further additions)
#           (C) 2025 Yuzuru (further additions)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import discord
from discord import app_commands
from discord.ext import commands


@app_commands.guild_only()
class BasicCommands(
    commands.GroupCog, group_name="basic_commands", description="Basic commands for the bot."
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.log_bot(f"{self.__class__.__name__} cog file loaded.")

    @app_commands.command(name="ping", description="Check Bot's latency")
    async def ping(self, interaction: discord.Interaction) -> None:
        if not await self.bot.perms_check(interaction=interaction, perms_level=0):
            await interaction.response.send_message(
                embed=self.bot.missing_perms_embed(interaction), ephemeral=True, delete_after=10
            )
            return

        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="Pong!", description=f"Latency is {latency}ms", color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Show Bot information")
    async def info(self, interaction: discord.Interaction) -> None:
        if not await self.bot.perms_check(interaction=interaction, perms_level=0):
            await interaction.response.send_message(
                embed=self.bot.missing_perms_embed(interaction), ephemeral=True, delete_after=10
            )
            return

        embed = discord.Embed(
            title=f"[{self.bot.user.display_name}'s Mirror World]",
            description="A /SlashCommand Only Discord Bot for Clickan Seventh's RP.",
            color=discord.Color.random(),
        )
        embed.add_field(name="Bot Creator", value="yuzurukyun", inline=True)
        embed.add_field(name="Bot Runtime", value=f"<t:{self.bot.bot_start_time}:R>", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fun_incident", description="Do this (in-game).")
    async def fun_incident(self, interaction: discord.Interaction) -> None:
        if not await self.bot.perms_check(interaction=interaction, perms_level=0):
            await interaction.response.send_message(
                embed=self.bot.missing_perms_embed(interaction), ephemeral=True, delete_after=10
            )
            return

        await interaction.response.send_message(
            "https://www.youtube.com/watch?v=2dbR2JZmlWo \nhttps://www.youtube.com/watch?v=-h5WrWncDZw"
        )

    @app_commands.command(
        name="set_bot_log_channel", description="Bot logging on a discord channel"
    )
    @app_commands.describe(target_channel="Channel ID for the bot logger channel")
    async def set_bot_log_channel(
        self, interaction: discord.Interaction, target_channel: discord.TextChannel | discord.Thread
    ) -> None:
        if not await self.bot.perms_check(interaction=interaction, perms_level=1):
            await interaction.response.send_message(
                embed=self.bot.missing_perms_embed(interaction), ephemeral=True, delete_after=10
            )
            return

        self.bot.bot_config.set_bot_logging_channel_id(channel_id=target_channel.id)
        self.bot.logging_channel_id = target_channel.id
        await interaction.response.send_message(
            "Set Bot Log Channel!", ephemeral=True, delete_after=10
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BasicCommands(bot=bot))
