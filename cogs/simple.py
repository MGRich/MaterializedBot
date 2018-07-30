import discord
from discord.ext import commands
import os, json

class Simple:
    """Simple commands and other basic stuff."""
    def __init__(self, bot):
        self.bot = bot

    #@commands.command(name="tes")
    #async def _help(self, ctx, *args):
    #    """Displays this command.
    #   [category] [command]"""
    #   e = discord.Embed()
    #    args = list(args)
    #    if len(args) <= 1:
    #       args[0] == args[0].lower
    #        e.title = "Category: {}".format(args[0].title())
    #        if len(args) == 2:
    ##            args[1] = "_" + args[1].lower()
    #            if args[0] == "simple":
    #                desc = eval("{}.__doc__".format(args[1]))
    #            else:
    #                desc = eval("{}.{}.__doc__".format(args[0], args[1]))
    #            await ctx.send(desc.split('\n'))
     #           return
     #   await ctx.send(args)

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx, prefix=None):
        """Sets/displays a custom prefix.
        If prefix is "default", it will revert back to normal. 
        <prefix>"""
        id = str(ctx.guild.id)
        prfd = False
        if prefix == None:
            pref = "m!"
            if os.path.exists("config/{}/config.json".format(id)):
                with open("config/{}/config.json".format(id)) as cfg:
                    con = json.load(cfg)
                    pref = con['prefix']
            return await ctx.send("The prefix here is `{0}`. Use `{0}prefix` to change it.".format(pref))
        prf = prefix
        os.chdir("config")
        if not os.path.isdir(id):
            os.mkdir(id)
        os.chdir(id)
        if prf == "default":
            prfd = True
        if not os.path.isfile('config.json'):
            with open('config.json', 'w+') as cfg:
                if prfd:
                    cfg.write(json.dumps({'prefix': prf}))
                else:
                    cfg.write(json.dumps({'prefix': prf}))
        else:
            with open('config.json', 'r+') as cfg:
                con = json.load(cfg)
                con['prefix'] = prf
                if prfd:
                    con.pop('prefix')
                cfg.truncate(0)
                cfg.seek(0) #just in case
                cfg.write(json.dumps(con))
        if prfd:
            await ctx.send("Prefix back to default.")
        else:
            await ctx.send("Prefix set to `{}`.".format(prf))
        os.chdir("../..")
    
    #@commands.command()
    #async def getme(self, ctx):
    #    """Sends the link to get me."""
    #    await ctx.send("Get the stable me with {}.\nGet the dev version of me with {}.".format(discord.utils.oauth_url("464546343797391371"), discord.utils.oauth_url("465942405611257866")))

    #@commands.command()
    #async def test(self, ctx):
    #    await ctx.send(ctx.message.attachments[0].url)

    @commands.command()
    async def ping(self, ctx):
        resp = await ctx.send('Pong! Loading...')
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(content=f'Pong! That took {1000*diff.total_seconds():.1f}ms.')

    

def setup(bot):
    bot.add_cog(Simple(bot))