import discord
from discord.ext import commands
import os  
from dotenv import load_dotenv
from typing import Optional
from utils import process_message_as_guess

load_dotenv()
bot = commands.Bot(command_prefix ="$", intents = discord.Intents.all())


@bot.event
async def on_ready():
    for FileName in os.listdir('./cmds'):    #自cmd資料夾中提取檔案名稱
        if FileName.endswith('.py'):    #若附檔名為.py
            await bot.load_extension(f'cmds.{FileName[:-3]}')    #加載該檔案
    channel = bot.get_channel(1236562259405443145)    #進入頻道
    if channel:
        await channel.send('轟隆一聲巨響，Bot閃亮登場✧*｡٩(ˊωˋ*)و✧*')
    print(">>Bot is Online<<")

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'Loaded')

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'Reloaded')

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'Unloaded')

@bot.event
async def on_message(message):
    processed_as_guess = await process_message_as_guess(bot, message)
    if not processed_as_guess:
        await bot.process_commands(message)

if  __name__ == "__main__":
    bot.run('TOKEN')

