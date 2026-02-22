from __future__ import annotations

import discord
import typing

if typing.TYPE_CHECKING:
    from src.discord_bot.bot import DiscordBot


class AnonMSGButton(discord.ui.View):
    def __init__(
        self, bot: DiscordBot, channel: discord.TextChannel | discord.Thread, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.bot: DiscordBot = bot
        self.channel: discord.TextChannel | discord.Thread = channel

    @discord.ui.button(label="Message", style=discord.ButtonStyle.primary)
    async def message_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(AnonMSGForm(bot=self.bot, channel=self.channel))


class AnonMSGForm(discord.ui.Modal, title="Send Anonymous Message"):
    message = discord.ui.TextInput(
        label="Your Message",
        style=discord.TextStyle.paragraph,
        placeholder="Type your anonymous message here...",
        required=True,
        max_length=2000,
    )

    def __init__(
        self, bot: DiscordBot, channel: discord.TextChannel | discord.Thread, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.bot: DiscordBot = bot
        self.channel: discord.TextChannel | discord.Thread = channel

    async def on_submit(self, interaction: discord.Interaction):
        get_channel = await self.bot.get_discord_channel(self.channel.id)
        if get_channel:
            await get_channel.send(embed=self.message_embed(self.message.value))
            await self.bot.log_decodead_message(
                user=interaction.user, channel=get_channel, message=self.message.value
            )

        embed = discord.Embed(
            title="Anonymous Message Sent",
            description=f"{self.message.value}",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    def message_embed(self, message_content: str) -> discord.Embed:
        # Placeholder for any message formatting or sanitization if needed.
        embed = discord.Embed(
            description=message_content,
            color=discord.Color.random(),
        )
        return embed
