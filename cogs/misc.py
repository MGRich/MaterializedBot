import discord, json, traceback
from discord.ext import commands
from cogs.helprs.SimplePaginator import SimplePaginator as pag
from cogs.helprs.suggestions import suggestions

help = json.load(open('help.json'))

class Help:
    def __init__(self, bot):
        self.bot = bot
    
    def prs(self, cat, cmd = None):
        if not cat:
            elist = []
            for x in help:
                e = discord.Embed(title=help[x]['name'], colour=discord.Colour(json.load(open('info.json'))['color']))
                fls = [help[x]['value'], ""]
                for y in help[x]['commands']:
                    fln = help[x]['commands'][y].split("\n")[0]
                    fls.append(f"`{y}`: {fln}")
                fls = "\n".join(fls)
                e.description = fls
                elist.append(e)
                e.set_footer(text="Use \"help category\" for more info on a category. Follow it up with a command in the category to get info on a command.")
            return elist
        ctt = help[cat]
        e = discord.Embed(title=ctt['name'])
        lns = [f"{ctt['value']}", ""]
        for x in ctt['commands']:
            fln = ctt['commands'][x].split("\n")[0]
            lns.append(f"`{x}`: {fln}")
        e.description = "\n".join(lns)
        if cmd:
            e.description = f"`{cmd}`\n\n" + ctt['commands'][cmd]
        e.colour = discord.Colour(json.load(open('info.json'))['color'])
        e.set_footer(text="Use \"help category\" for more info on a category. Follow it up with a command in the category to get info on a command.")
        return e

class Miscellaneous:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def refhelp(self, ctx):
        help = json.load(open('help.json'))
        help #shut the fuck up pylint
        await ctx.send("cool and good")

    @commands.command()
    async def help(self, ctx, *args):
        #all for now
        args = list(args)
        for y, x in enumerate(args):
            args[y] = x.lower()
        try:
            if len(args) == 1:
                emb = Help.prs(self, args[0])
            elif len(args) == 2:
                emb = Help.prs(self, args[0], args[1])
            elif len(args) == 0:
                return await pag(extras=Help.prs(self, None)).paginate(ctx)
            await ctx.send(embed=emb)
        except:
            await ctx.send("That is not a valid category/command.")

    @commands.command()
    async def suggest(self, ctx, *args):
        """Suggests an idea.
        "type" can be IMGGal, simple, moderation, fun, or general.
        If none of such is given, general will be used.
        [type] <suggestion>""" 
        args = list(args)
        if any(s == args[0].lower() for s in ['imggal', 'simple', 'moderation', 'fun', 'general']):
            typ = args.pop(0)
        else:
            typ = 'general'
        if len(args) == 0:
            return await ctx.send("Please give a suggestion.")
        sug = ' '.join(args)
        try:
            await suggestions.add("dummy", self.bot, ctx, typ, None, discord.Embed(description=sug))
        except:
            return await ctx.send("An error occured.")
        await ctx.send("Sent!")

    #@commands.command()
    #async def sloli(self, ctx, *img):
    #    """sends a loli to rich cause lolicon
    #    <image link or upload>"""
     #   return await ctx.send("im sorry but no more for now lmfao")
      #  if len(img) != 0:
       #     img = img[0]
        #else:
         #   img = ctx.message.attachments[0].url
        #check for valid image
    #    if not any(img.lower().endswith(x) for x in ['.png', '.jpg', '.jpeg', '.webp', '.gif']):
     #       return await ctx.send("Please give a valid image.")
      #  e = discord.Embed(title="Loli", colour=discord.Colour(0xF9C2F0))
       # try:
        #    await suggestions.add("dummy", self.bot, ctx, "loli", img, e, False)
    #    except:
     #       traceback.print_exc()
      #      return await ctx.send("An error occured.")
       # await ctx.send("Loli sent.")

    @commands.command()
    async def bugrep(self, ctx, *bug):
        """sends a loli to rich cause lolicon
        <image link or upload>"""
        e = discord.Embed(title="BUG REPORT", colour=discord.Colour(0xF04747))
        try:
            bug = ' '.join(bug)
        except:
            return await ctx.send("Please list a bug.")
        try:
            await suggestions.add("dummy", self.bot, ctx, "bugrep", None, e, False, bug)
        except: 
            traceback.print_exc()
            return await ctx.send("An error occured.")
        await ctx.send("Bug report sent.")

    #@commands.command()
    #async def er(self, ctx):
     #   a = 5
     #     await ctx.send(a + "hi")

    @commands.command(aliases=['getme', 'about'])
    async def info(self, ctx):
        inf = json.load(open('info.json'))
        tup = (("Version", inf['version']), ("Info", "This is just a general purpose bot for any type of server."), ("Owner", "RMGRich#8192"), ("Servers", len(self.bot.guilds)), ("Support Server", "[Join here.](https://discord.gg/4Wpsswq)"), ("Invite Links", "[Stable]({})\n[Developer]({})".format(discord.utils.oauth_url("464546343797391371"), discord.utils.oauth_url("465942405611257866"))))
        #("Members", len(list(self.bot.get_all_members)))
        e = discord.Embed(title="Info", colour=discord.Colour(inf['color']))
        e.set_footer(text="Made using discord.py.", icon_url="https://cdn.discordapp.com/icons/336642139381301249/3aa641b21acded468308a37eef43d7b3.webp")
        for x in tup:
            e.add_field(name=x[0], value=x[1], inline=True) #not sure if i wanna do inline or not
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))