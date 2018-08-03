import discord, traceback, time
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import random
from cogs.helprs.suggestions import suggestions
from datetime import datetime

class Fun:
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    async def quote(self, ctx, mid: int, memb: discord.Member=None):
        try:
            if memb:
                try:
                    msg = await memb.get_message(mid)
                except:
                    msg = await ctx.channel.get_message(mid)
            else:
                msg = await ctx.channel.get_message(mid)
        except discord.NotFound:
            return await ctx.send("Message not found. (this is pretty broken, so it's gonna appear a lot.)")
        e = discord.Embed(description=msg.content, timestamp=msg.created_at)
        if msg.edited_at:
            tm = msg.edited_at#.replace(tzinfo=timezone.utc).astimezone(tz=None)
            e.set_footer(text=f"Edited {tm.strftime('%D')} at {tm.strftime('%I:%M %p')} UTC")
        e.set_author(name=msg.author.display_name, icon_url=msg.author.avatar_url_as(static_format='png'))
        if len(msg.author.roles) > 0:
            e.colour = msg.author.roles[-1].colour
        await ctx.send(embed=e)

    @commands.command(aliases=['fquote'])
    async def fakequote(self, ctx, memb: discord.Member, *, cont):
        e = discord.Embed(description=cont, timestamp=datetime.utcnow())
        e.set_author(name=memb.display_name, icon_url=memb.avatar_url_as(static_format='png'))
        if len(memb.roles) > 0:
            e.colour = memb.roles[-1].colour
        await ctx.send(embed=e)

    @commands.command()
    async def clap(self, ctx, *, text):
        await ctx.send('👏'.join(text.split(" ")))


def setup(bot):
    bot.add_cog(Fun(bot))
