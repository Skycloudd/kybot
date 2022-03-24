import os

import discord
import git
from discord.ext import commands


async def is_bot_owner(ctx: commands.Context) -> bool:
    return (
        await ctx.bot.is_owner(ctx.author)
        or ctx.author.id in ctx.bot.settings["owners"]
    )


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    @commands.check(is_bot_owner)
    async def logs(self, ctx: commands.Context) -> None:
        """
        Send the log file
        """

        file = discord.File("discord.log")
        await ctx.send(file=file)

    @commands.command(aliases=["forceexit", "forcequit"])
    @commands.check(is_bot_owner)
    async def exit(self, ctx: commands.Context) -> None:
        """
        Close the bot
        """

        await ctx.send("goodbye cruel world 😔👋")
        self.bot.logger.info("goodbye cruel world 😔👋")
        await self.bot.session.close()
        await self.bot.close()

    @commands.command()
    @commands.check(is_bot_owner)
    async def pull(self, ctx: commands.Context) -> None:
        """
        Pull updates from git
        """

        g = git.cmd.Git(os.getcwd())
        try:
            await self.bot.send_pretty(ctx, f"```bash\n{g.pull()}\n```")
        except git.exc.GitCommandError as e:
            await self.bot.send_pretty(ctx, f"```bash\n{e}\n```")

    @commands.command()
    @commands.check(is_bot_owner)
    async def echo(self, ctx: commands.Context, *, message: str) -> None:
        """
        Echo a message back
        """

        await self.bot.send_pretty(ctx, message)

    @commands.command(name="reload", usage="<extension>")
    @commands.check(is_bot_owner)
    async def _reload(self, ctx: commands.Context, ext: str) -> None:
        """
        Reload an extension
        """

        try:
            self.bot.reload_extension(f"cogs.{ext}")
            await self.bot.send_pretty(ctx, f"The extension {ext} was reloaded.")
        except commands.ExtensionError as e:
            await self.bot.send_pretty(ctx, f"```\n{e}\n```")

    @commands.command(name="load", usage="<extension>")
    @commands.check(is_bot_owner)
    async def _load(self, ctx: commands.Context, ext: str) -> None:
        """
        Load an extension
        """

        try:
            self.bot.load_extension(f"cogs.{ext}")
            await self.bot.send_pretty(ctx, f"The extension {ext} was loaded.")
        except commands.ExtensionError as e:
            await self.bot.send_pretty(ctx, f"```\n{e}\n```")

    @commands.command(name="unload", usage="<extension>")
    @commands.check(is_bot_owner)
    async def _unload(self, ctx: commands.Context, ext: str) -> None:
        """
        Unload an extension
        """
        try:
            self.bot.unload_extension(f"cogs.{ext}")
            await self.bot.send_pretty(ctx, f"The extension {ext} was unloaded.")
        except commands.ExtensionError as e:
            await self.bot.send_pretty(ctx, f"```\n{e}\n```")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Admin(bot))
