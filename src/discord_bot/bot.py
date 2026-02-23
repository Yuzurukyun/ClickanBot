from __future__ import annotations

import discord
from discord.ext import commands
from discord.utils import find

import time

from src.utils.constants import BotConfig
import src.discord_bot.cogs as cog_path


def bot_intents() -> discord.Intents:
    """
    This function returns the intents for the bot. If you want to add more intents, add it here.
    """
    intents = discord.Intents.all()
    return intents


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=None, intents=bot_intents())  # Ensure no prefix is made.
        self.bot_start_time: int = 0
        self.bot_config: BotConfig = BotConfig
        self.token: str = BotConfig.get_discord_token()

        self.setup_events()
        self.bot_admin_role_name: str = "Bot Admin"
        self.logging_channel_id: int | None = BotConfig.get_bot_logging_channel_id()

    async def init(self) -> None:
        self.log_bot("Initialising discord bot...")
        try:
            await self.load_cogs()
            await self.start(token=self.token)
        except Exception as e:
            print(repr(e))
            raise e

    # == Mandatory Events == #

    def setup_events(self) -> None:
        """Sets up event listeners."""

        @self.event
        async def on_ready() -> None:
            self.log_bot(f"logged on as {self.user}!")
            self.bot_start_time = round(time.time())
            await self.change_presence(
                activity=discord.Activity(
                    type=1,
                    name="DECODEAD Bot",
                    url="https://twitch.tv/twitch",
                )
            )

            await self.tree.sync()
            await self.wait_until_ready()
            await self.create_mandatory_roles()

        @self.event
        async def on_message(message: discord.Message) -> None:
            # if this doesnt work maybe add "is not None"
            if message.author.bot or message.webhook_id:
                return  # This is so it doesn't echo eternally

            if not message.guild:
                await self.log_dm_message(user=message.author, message=message.content)

        @self.event
        async def on_interaction(interaction: discord.Interaction):
            if not interaction.guild:
                return

            # TODO: Send logs to the channel under different formatting. One from DMs and one from Guilds. Maybe do an all in one.
            if interaction.type == discord.InteractionType.application_command:
                await self.log_command_usage(
                    user=interaction.user, command_name=interaction.data["name"]
                )

    # == Utilities == #

    async def log_decodead_message(
        self, user: discord.User, channel: discord.TextChannel, message: str
    ) -> None:
        embed = discord.Embed(
            title="[DECODEAD] Message Received",
            description=f"**From:** {user.mention}\n**To Channel:** {channel.mention}\n**Message:** \n{message}",
        )
        await self.log_to_bot_channel(embed=embed)

    async def log_dm_message(self, user: discord.User, message: str) -> None:
        embed = discord.Embed(
            title="[DM] Message Received",
            description=f"**From:** {user.mention}\n**Message:** \n{message}",
        )
        await self.log_to_bot_channel(embed=embed)

    async def log_command_usage(self, user: discord.User, command_name: str) -> None:
        embed = discord.Embed(
            title="[Commands] Command Used",
            description=f"**User:** {user.mention}\n**Command:** {command_name}",
        )
        await self.log_to_bot_channel(embed=embed)

    async def log_to_bot_channel(self, embed: discord.Embed) -> None:
        if self.logging_channel_id:
            channel = self.get_channel(self.logging_channel_id)
            if channel:
                await channel.send(embed=embed)

    def log_bot(self, message: str) -> None:
        print(f"[DISCORD] {message}")

    async def load_cogs(self) -> None:
        import os
        import pathlib

        try:
            cog_dir = pathlib.Path(cog_path.__file__).parts
            cog_dir = cog_dir[0:-1]
            cog_dir = os.listdir("/".join(cog_dir))
            for cg in cog_dir:
                if cg.endswith(".py"):
                    if cg.lower() == "__init__.py":
                        continue

                    await self.load_extension(f"src.discord_bot.cogs.{pathlib.Path(cg).stem}")

        except Exception as e:
            raise e

    def missing_perms_embed(self, interaction: discord.Interaction) -> discord.Embed:
        embed = discord.Embed(
            title="[ Insufficient Permissions! ]",
            description=f"You have no access to this command, {interaction.user.mention}!",
            color=discord.Color.random(),
        )
        return embed

    async def perms_check(self, interaction: discord.Interaction, perms_level: int) -> bool:
        """Check if the user has the required permissions.
        Args:
            interaction (discord.Interaction): The interaction object.
            perms_level (int): The required permission level. 0 = Everyone, 1 = Bot Admin, 2 = Server Owner.
        Returns:
            bool: True if the user has the required permissions, False otherwise.
        """
        user_perms_level: int = 0
        user_roles = [_user_roles.name.lower() for _user_roles in interaction.user.roles]
        if self.bot_admin_role_name.lower() in user_roles:
            user_perms_level = 1
        if interaction.user.id == interaction.guild.owner_id:  # Checks if Owner.
            user_perms_level = 2

        if user_perms_level >= perms_level:  # Checks the perms level.
            return True
        return False

    async def create_mandatory_roles(self) -> None:
        for guild in self.guilds:
            try:
                guild_roles = [_guild_roles.name.lower() for _guild_roles in guild.roles]
                if self.bot_admin_role_name.lower() not in guild_roles:
                    admin_role = await guild.create_role(
                        name=self.bot_admin_role_name,
                        colour=discord.Colour.yellow(),
                        mentionable=True,
                    )
                    self.log_bot(f"Created {admin_role.name} role for Guild ID: {guild}.")
            except discord.Forbidden:
                self.log_bot(
                    "No permissions to create Mandatory Roles. Please create a role named 'Bot Admin' and 'Bot Game Master' manually."
                )
            except Exception as e:
                self.log_bot(str(e))

    async def get_discord_channel(
        self, channel_id: int
    ) -> discord.TextChannel | discord.Thread | None:
        obj = self.get_channel(channel_id)
        return obj if obj is not None else await self.fetch_channel(channel_id)

    async def get_discord_member(
        self, user_id: str | int, guild_id: str | int = None
    ) -> discord.Member:
        if not guild_id:
            guild = self.get_guild(guild_id)
        else:
            guild = self.guilds[0]
        return find(lambda m: m.id == user_id, guild.members)
