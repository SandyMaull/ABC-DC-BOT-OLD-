import discord
from discord.ext import commands
import sys
import traceback
import json
from ext.db_module import fetch

def checkdata(guild_id):
    regis_db = fetch.one(guild_id, "config", 'name', 'REGISTER')
    regis_data = json.loads(regis_db)
    if regis_data['value'] == 'TRUE':
        return True
    else:
        return False

class Help_Register(commands.Cog):
    """Cog for the help command."""

    def __init__(self, bot):
        self.bot = bot
        self.prefix = "-"
        self.bot_cogs = self.bot.cogs

    async def cog_check(self, ctx):
        return ctx.prefix == self.prefix

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            pass
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    @commands.command(name="regishelp", aliases=["rh"])
    async def help(self, ctx):

        if ctx.prefix != '-':
            return
        
        if checkdata(ctx.guild.id) != True:
            await ctx.reply("Fitur register pada bot ini sedang dimatikan oleh developer.", delete_after=7)
            return

        try:
            cog = self.bot_cogs["Register"]
        except KeyError:
            query_error_embed = discord.Embed(
                title="Query Error. Perhaps you mean:",
                description=f"{', '.join(self.bot_cogs.keys())}.",
                color=discord.Color.red(),
            )
            return await ctx.send(embed=query_error_embed)

        cog_help_embed = discord.Embed(
            title=f"Bot Commands",
            color=discord.Color.blue(),
        )

        for command in cog.get_commands():

            command_aliases = (
                f"{', '.join(command.aliases)}" if len(command.aliases) > 0 else "None"
            )
            cog_help_embed.add_field(
                name=(f"-{command.name} , {command_aliases}")
                if (command_aliases != "None")
                else (f"-{command.name}"),
                value=f"`{command.help}`",
                inline=False,
            )

        cog_help_embed.add_field(
            name="Developer:", value="Anti Bang Cat Guild", inline=False
        )
        await ctx.send(embed=cog_help_embed)


def setup(bot):
    bot.add_cog(Help_Register(bot))
