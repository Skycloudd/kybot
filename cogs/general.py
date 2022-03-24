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
    async def prefix(self, ctx):
        """Get the bot's prefixes"""

        prefixes = await self.bot.get_prefix(ctx.message)
        prefixes.pop(1)
        output = ", ".join(prefixes)

        await self.bot.send_pretty(ctx, f"My prefixes are {output}")


def setup(bot):
    bot.add_cog(General(bot))
