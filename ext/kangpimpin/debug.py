import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from table2ascii import table2ascii as t2a, PresetStyle
from ext.db_module import fetch
from ext.db_module import update
import json
import time
import os
import sys

def check_config(guild_id):
    debug_db = fetch.one(guild_id, "config", 'name', 'DEBUG')
    debug_data = json.loads(debug_db)
    if debug_data['value'] == 'TRUE':
        return True
    else:
        return False

def developer_check(guild_id):
    dev_db = fetch.all(guild_id, 'developer')
    dev_data = json.loads(dev_db)
    dev_id = []
    for i in range(len(dev_data)):
        dev_id.append(int(dev_data["{i}".format(i = i)]["dev_id"]))
    return dev_id

def history_check(guild_id):
    h_db = fetch.all(guild_id, 'history')
    h_data = json.loads(h_db)
    return h_data

class debug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def abc_hello(self, ctx):
        if check_config(ctx.guild.id):
            await ctx.reply('Hello <@{user}> ! \nHow r u today? \n'.format(user=ctx.author.id), mention_author=True)
        else:
            await ctx.reply("Fitur debug pada bot ini sedang dimatikan oleh developer.", delete_after=7)
    
    @commands.command()
    async def abc_ping(self, ctx):
        if check_config(ctx.guild.id):
            before = time.monotonic()
            message = await ctx.reply("Pong!")
            ping = (time.monotonic() - before) * 1000
            await message.edit(content=f"Pong!, avr Ping is `{int(ping)}ms` for last 1-5 second interval")
        else:
            await ctx.reply("Fitur debug pada bot ini sedang dimatikan oleh developer.", delete_after=7)

    @commands.command()
    async def history(self, ctx):
        if check_config(ctx.guild.id):
            data = history_check(ctx.guild.id)
            header_final = ['type', 'name', 'value']
            data_final = []
            for i in range(len(data)):
                try:
                    data_temp = ['{typed}'.format(typed = data['{i}'.format(i = i)]['type']), '{name}'.format(name = await ctx.guild.fetch_member(data['{i}'.format(i = i)]['name'])), '{value}'.format(value = data['{i}'.format(i = i)]['value'])]
                    data_final.append(data_temp)
                except:
                    data_temp = ['{typed}'.format(typed = data['{i}'.format(i = i)]['type']), 'NULL(Probably Exit Server or Delete Account)', '{value}'.format(value = data['{i}'.format(i = i)]['value'])]
                    data_final.append(data_temp)
            output_final = t2a(
                header=header_final,
                body=data_final,
                style=PresetStyle.ascii_minimalist
            )
            await ctx.reply(f"```\n{output_final}\n```")
        else:
            await ctx.reply("Fitur debug pada bot ini sedang dimatikan oleh developer.", delete_after=7)

    @commands.command()
    async def setting(self, ctx, *params):
        if ctx.author.id not in developer_check(ctx.guild.id):
            await ctx.reply("This Command Only for Developer!.", delete_after=7)
        else:
            if len(params) == 2:
                jsondata = fetch.all(ctx.guild.id, "config")
                fetchdata = json.loads(jsondata)
                settingname = params[0]
                for i in range(len(fetchdata)):
                    looping = '{i}'.format(i = i)
                    if settingname == fetchdata[looping]['name']:
                        if params[1] == 'ON':
                            if update.one("config", "name", settingname, "value", 'TRUE'):
                                await ctx.reply("Setting Update Successfully.")
                            else:
                                await ctx.reply("Setting Update Failed.")
                                print("Setting Update Failed, Check DB Connection!", delete_after=7)
                        elif params[1] == 'OFF':
                            if update.one("config", "name", settingname, "value", 'FALSE'):
                                await ctx.reply("Setting Update Successfully.")
                            else:
                                await ctx.reply("Setting Update Failed.")
                                print("Setting Update Failed, Check DB Connection!", delete_after=7)
                        else:
                                await ctx.reply("Parameter's Invalid.", delete_after=7)
                        notfounddata = False
                        break
                    else:
                        notfounddata = True
                        continue
                if notfounddata:
                    await ctx.reply("Data Setting for {data} is not found.".format(data = params[0]), delete_after=30)
            elif params[0] == 'LS_DEV':
                dev_data = developer_check(ctx.guild.id)
                dev_print = "**List Developer:**\n"
                for i in range(len(dev_data)):
                    dev_print += "{dev}\n".format(dev = await ctx.guild.fetch_member(dev_data[i]))
                await ctx.reply(dev_print)
                
            elif params[0] == 'TERM_BOT':
                async def callbackyes(interaction):
                    await ctx.send("....Okay, Im sorry for dissapointing you.", delete_after=3)
                    time.sleep(3)
                    sys.exit()

                async def callbackno(interaction):
                    await ctx.send("....Weird, Dont make me Nervous.")
                    return

                components = [[
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.gray, label="Yes", custom_id="yes"), callbackyes
                    ),
                    self.client.components_manager.add_callback(
                        Button(style=ButtonStyle.gray, label="No", custom_id="no"), callbackno
                    )
                ]]
                await ctx.reply(
                    "Are You Sure Admin? This will Terminate All Running Bot.",
                    components=components,
                    delete_after=15
                )
            else:
                await ctx.reply("Parameter's invalid.", delete_after=7)

def setup(client):
    client.add_cog(debug(client))