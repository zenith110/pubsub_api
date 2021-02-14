from os import error
import discord
from discord.ext import commands
import json
import os


class Help(commands.Cog):
    """
    Creates the instance of admin including its fields
    @bot - the bot itself
    @last_member - last member to use this
    return - nothing
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    """  
    Fetches a city's weather forecast from the input      
    @self - self obj
    @context - how we'll send messages
    @*args - arguments following the command
    return - nothing
    """

    @commands.command(aliases=["help", "commands"])
    async def HelpSystem(self, context: discord.ext.commands.context.Context):
        await context.send(
            f"{context.author.mention}, here is our current list of commands\n"
            + "```!pubsub - for getting specific pubsub data\n!no-sale - for subs not on sale\n!onsale - for all subs currently on sale!\nSpecial thanks for pubsub-api.dev for providing pubsub data\n"
            + "\nUse !pubsub help for getting what subs we have available!\nGithub repo is here -> https://github.com/zenith110/pubsub_api```"
        )


"""
setup for the command
"""


def setup(bot):
    bot.add_cog(Help(bot))
