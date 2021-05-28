import discord
from discord.ext import commands
import requests
import json
from disputils import BotEmbedPaginator


class Sale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["onsale", "on-sale"])
    async def on_sale(self, context):
        sale_list = []
        data = requests.get("https://api.pubsub-api.dev/onsale/")
        data_json = data.json()
        for i in range(len(data_json)):
            if data_json[i]["on_sale"] == "True":
                sale_list.append(data_json[i])
            else:
                continue
        discord_embeds = []
        try:
            await context.send(
                        f"{context.author.mention}"
            )
            for pubsub in range(len(sale_list)):
                discord_embeds.append(
                    discord.Embed(
                        title=sale_list[pubsub]["name"],
                        description="Currently on sale from: "
                        + sale_list[pubsub]["last_on_sale"]
                        + " for the price of "
                        + sale_list[pubsub]["price"],
                        color=0x115599,
                    ).set_image(url=sale_list[pubsub]["image"])
                )
            paginator = BotEmbedPaginator(context, discord_embeds)
            await paginator.run()
        except:
            print("Something went wrong here!")


def setup(bot):
    bot.add_cog(Sale(bot))
