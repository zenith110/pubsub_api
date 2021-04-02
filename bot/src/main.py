from dotenv import load_dotenv
from os.path import join, dirname
import os
from discord import utils
import discord
from discord.ext import commands


def command_loader():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            file_directory = os.path.join("./cogs", filename)
            with open(file_directory, "r") as python_file:
                bot.load_extension(f"cogs.{filename[:-3]}")
            print("[<3] Loaded ", filename)


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
"""
store values in global variables
"""
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = commands.Bot("!")
bot.remove_command("help")
print("[!] Awakening PubSub, standby...")
print("=" * 40)
command_loader()


@bot.event
async def on_connect():
    print("[*] Client sucessfully connected to Discord")


@bot.event
async def on_ready():
    print("\n[*] Established bot onto server")
    print("-" * 40)

    """
    Changes the discord status to the current release
    """
    await bot.change_presence(activity=discord.Game(name="Finding Pubsub deals"))


bot.run(BOT_TOKEN)
