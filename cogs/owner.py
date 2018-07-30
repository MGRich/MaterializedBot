import discord, json, inspect, os, traceback, contextlib, io, sys
from discord.ext import commands

data = json.load(open("info.json"))
blocks = json.load(open("blocks.json"))

def ownerch():
    return commands.check(lambda ctx: any(x in [data['owners'], ctx.guild.owner.id] for x in [ctx.message.author.id, ctx.guild.owner.id]))

def ownerbt():
    return commands.check(lambda ctx: ctx.message.author.id == 214550163841220609)

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, hidden=True)
    @ownerbt()
    async def unload(self, ctx, *cogs):
        err = False
        cogs = list(cogs)
        cgs = []
        for x in os.listdir("cogs"):
            if os.path.isfile("cogs/" + x):
                cgs.append("cogs.{}".format(x[:-3]))
        mcgs = cgs
        for cg in cogs:
            if "cogs." + cg not in cgs:
                cogs.remove(cg)
        if len(cogs) != 0:
            for x, y in enumerate(cogs):
                cogs[x] = "cogs." + y
            mcgs = cogs
        for cog in mcgs:
            try:
                print(f"attempt to unload {cog}")
                self.bot.unload_extension(cog)
                print(f"unloaded {cog}")
            except Exception:
                self.bot.unload_extension(cog)
                await ctx.send("Failed to load {}. Check console for details.".format(cog))
                print("-----START {}".format(cog))
                traceback.print_exc()
                print("-----END   {}".format(cog))
                err = True
        if not err:
            await ctx.send("All unloaded successfully.")

    @commands.command(pass_context=True, hidden=True)
    @ownerbt()
    async def block(self, ctx, member:discord.Member):
        blocks['blocks'].append(member.id)
        json.dump(blocks, open("blocks.json", "w"))

    @commands.command(pass_context=True, hidden=True)
    @ownerbt()
    async def unblock(self, ctx, member:discord.Member):
        try:
            blocks['blocks'].remove(member.id)
        except:
            return
        json.dump(blocks, open("blocks.json", "w"))

def setup(bot):
    bot.add_cog(Owner(bot))
