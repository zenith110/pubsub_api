import discord
from discord.ext import commands
import requests
import json
from disputils import BotEmbedPaginator


class NotOnSale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["no-sale", "not-on-sale", "nosale"])
    async def not_on_sale(self, context):
        not_on_sale_list = []
        data = requests.get("https://api.pubsub-api.dev/onsale/")
        data_json = data.json()
        for i in range(len(data_json)):
            if data_json[i]["on_sale"] == "False":
                not_on_sale_list.append(data_json[i])
            else:
                continue
        discord_embeds = []
        try:
            for pubsub in range(len(not_on_sale_list)):
                discord_embeds.append(
                    discord.Embed(
                        title=not_on_sale_list[pubsub]["name"],
                        description="Last seen on sale on: "
                        + not_on_sale_list[pubsub]["last_on_sale"]
                        + " for the price of "
                        + not_on_sale_list[pubsub]["price"],
                        color=0x115599,
                    ).set_image(url=not_on_sale_list[pubsub]["image"])
                )
            paginator = BotEmbedPaginator(context, discord_embeds)
            await paginator.run()
        except:
            print("Something went wrong here!")


def setup(bot):
    bot.add_cog(NotOnSale(bot))
