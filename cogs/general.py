import discord
from discord.ext import commands


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f"``{self.clean_prefix}{command.qualified_name} {command.signature}``"


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self) -> None:
        self.bot.help_command = self._original_help_command

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        """
        Pong! Send the bot's latency
        """

        await self.bot.send_pretty(
            ctx, f"pong! {str(round(self.bot.latency * 1000))}ms"
        )

    @commands.command()
    async def source(self, ctx: commands.Context) -> None:
        """
        Get the source code for the bot
        """

        await self.bot.send_pretty(ctx, "https://github.com/Skycloudd/kybot")

    @commands.command()
    async def prefix(self, ctx: commands.Context):
        """Get the bot's prefixes"""

        prefixes = await self.bot.get_prefix(ctx.message)
        prefixes.pop(1)
        output = ", ".join(prefixes)

        await self.bot.send_pretty(ctx, f"My prefixes are {output}")

    @commands.command()
    async def serverinfo(self, ctx: commands.Context, guild: discord.Guild = None):
        """Get information about the server you are in"""
        if not guild:
            guild = ctx.message.guild
        else:
            guild = self.bot.get_guild(int(guild))

        if guild.owner is not None:
            if guild.owner.color.value == 0:
                color = 16777210
            else:
                color = guild.owner.color
        else:
            color = 16777210

        # emojiList = " ".join([str(emoji) for emoji in guild.emojis])

        if guild.is_icon_animated():
            serverIcon = guild.icon_url_as(format="gif")
        else:
            serverIcon = guild.icon_url_as(format="png")

        embed = discord.Embed(
            title=guild.name,
            color=color,
            timestamp=ctx.message.created_at,
        )

        if guild.premium_subscription_count == 0:
            pass
        else:
            boosts = "boosts" if guild.premium_subscription_count > 1 else "boost"

            embed.add_field(
                name="Amount of boosts:",
                value=f"{guild.premium_subscription_count} {boosts}",
                inline=True,
            )

        if guild.premium_subscribers:
            boosters = " ".join([i.mention for i in guild.premium_subscribers])
            embed.add_field(name="Boosted by:", value=boosters, inline=True)

        embed.set_thumbnail(url=serverIcon)
        embed.set_image(url=guild.splash_url_as(format="png"))
        embed.add_field(name="Created on", value=guild.created_at.date(), inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        # embed.add_field(name="Emojis", value=emojiList, inline=True) # too long possibly TODO: fix
        if guild.owner is not None:
            embed.add_field(name="Owner", value=guild.owner.mention, inline=True)

        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
