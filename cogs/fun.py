import discord, traceback
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
from cogs.helprs.suggestions import suggestions

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="quotee", hidden=True)
    async def _quote(self, ctx, *args):
        """Quote a message.
        (message id) [server id]""" 
        args = list(args)
        #if len(args) == 0:
        #    await ctx.send("Please give me atleast a message and channel ID.")
        #    return
        #if len(args) == 1:
        #    args.append(ctx.guild.id)
        #msg = discord.Message()
        #await ctx.send(args)
        await ctx.send("how the fuck did you find this")

    @commands.cooldown(3,120,BucketType.user) 
    @commands.command()
    async def randping(self, ctx):
        """Pings a random user for your enjoyment."""
        while True:
            memb = random.choice(ctx.guild.members)
            if not memb.bot:
                break
        memb = memb.mention
        await ctx.send(memb)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def say(self, ctx, *, msg):
        """Says something through the bot.
        If no message is givin, the message that sent the command will be deleted.
        Must have manage messages permission.
        <message to say>"""
        await ctx.message.delete()
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Fun(bot))