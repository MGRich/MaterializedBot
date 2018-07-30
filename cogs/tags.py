import discord, json
from discord.ext import commands

class Tags:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['update'])
    async def add(self, ctx, tag, string, *, strcont):
        """Adds/updates a LOCAL tag.
        Dobule quotes sadly do not work.
        <tag> <tag string>""" 
        tag = tag.lower()
        existed = False
        tstr = string + " " + strcont
        if tstr[-1] == " ":
            tstr = tstr[:-1]
        tgs = json.load(open('tags.json'))
        try:
            tgs['private'][str(ctx.guild.id)]
        except:
            tgs['private'][str(ctx.guild.id)] = {}
        try:
            tgs['private'][str(ctx.guild.id)][tag]
            existed = True
        except: 
            pass
        if existed:
            if ctx.message.author.id != tgs['private'][str(ctx.guild.id)][tag]['owner']:
                return await ctx.send("You do not own this tag, thus you cannot update it.")
        tgl = {tag: {'owner': ctx.message.author.id, 'str': tstr}}
        tgs['private'][str(ctx.guild.id)].update(tgl)
        json.dump(tgs, open('tags.json', 'w'), sort_keys=True, indent=2)
        await ctx.send(f"Tag `{tag}` successfully made (or updated)!")

    @commands.command(aliases=['updatep'])
    async def addp(self, ctx, tag, string, *, strcont):
        """Adds/updates a PUBLIC tag.
        Dobule quotes sadly do not work.
        <tag> <tag string>""" 
        tag = tag.lower()
        existed = False
        tstr = string + " " + strcont
        if tstr[-1] == " ":
            tstr = tstr[:-1]
        tgs = json.load(open('tags.json'))
        try:
            tgs['public']
        except:
            tgs['public'] = {} #too rare, shouldnt happen
        try:
            tgs['public'][tag]
            existed = True
        except: 
            pass
        if existed:
            if ctx.message.author.id != tgs['public'][tag]['owner']:
                return await ctx.send("You do not own this tag, thus you cannot update it.")
        tgl = {tag: {'owner': ctx.message.author.id, 'str': tstr}}
        tgs['public'].update(tgl)
        json.dump(tgs, open('tags.json', 'w'), sort_keys=True, indent=2)
        await ctx.send(f"Tag `{tag}` successfully made (or updated)!")

    
    @commands.command()
    async def tag(self, ctx, tag):
        """Displays a tag.
        Local tags override public tags.
        <tag>""" 
        tag = tag.lower()
        tgs = json.load(open('tags.json'))
        try:
            tg = tgs['private'][str(ctx.guild.id)][tag]
        except:
            try:
                tg = tgs['public'][tag]
            except:
                return await ctx.send(f"No {tag} found in tags.")
        await ctx.send(tg['str'])

    @commands.command()
    async def tagp(self, ctx, tag):
        """Displays a PUBLIC tag, overriding local tags.
        <tag>""" 
        tag = tag.lower()
        tgs = json.load(open('tags.json'))
        try:
            tg = tgs['public'][tag]
        except:
            return await ctx.send(f"No {tag} found in tags.")
        await ctx.send(tg['str'])


    @commands.command()
    async def delete(self, ctx, tag):
        """Deletes a LOCAL tag.
        <tag>""" 
        tag = tag.lower()
        existed = False
        tgs = json.load(open('tags.json'))
        try:
            tgs['private'][str(ctx.guild.id)][tag]
            existed = True
        except:
            tgs['private'][str(ctx.guild.id)] = {}
        if existed:
            if ctx.message.author.id != tgs['private'][str(ctx.guild.id)][tag]['owner']:
                return await ctx.send("You do not own this tag, thus you cannot delete it.")
            else:
                def check(m):
                    return m.content.startswith('y') and m.channel == ctx.message.channel and m.author.id == tgs['private'][str(ctx.guild.id)][tag]['owner']
                await ctx.send(f"Are you sure you want to delete tag `{tag}`?")
                await self.bot.wait_for('message', check=check)
                del tgs['private'][str(ctx.guild.id)][tag]
                json.dump(tgs, open('tags.json', 'w'), sort_keys=True, indent=2)
                await ctx.send(f"Deleted tag `{tag}`.")
        else:
            await ctx.send("Tag does not exist.")

    @commands.command()
    async def deletep(self, ctx, tag):
        """Deletes a PUBLIC tag.
        <tag>""" 
        tag = tag.lower()
        existed = False
        tgs = json.load(open('tags.json'))
        try:
            tgs['public']
        except:
            tgs['public'] = {} #too rare, shouldnt happen
        try:
            tgs['public'][tag]
            existed = True
        except: 
            pass
        if existed:
            if ctx.message.author.id != tgs['public'][tag]['owner']:
                return await ctx.send("You do not own this tag, thus you cannot delete it.")
            else:
                def check(m):
                    return m.content.startswith('y') and m.channel == ctx.message.channel and m.author.id == tgs['public'][tag]['owner']
                await ctx.send(f"Are you sure you want to delete tag `{tag}`?")
                await self.bot.wait_for('message', check=check)
                del tgs['public'][tag]
                json.dump(tgs, open('tags.json', 'w'), sort_keys=True, indent=2)
                await ctx.send(f"Deleted tag `{tag}`.")
        else:
            await ctx.send("Tag does not exist.")

    @commands.command()
    async def owner(self, ctx, tag):
        """Displays who owns a tag.
        Local tags override public tags.
        <tag>""" 
        prv, pub = False, False
        tag = tag.lower()
        tgs = json.load(open('tags.json'))
        try:
            owpr = tgs['private'][str(ctx.guild.id)][tag]['owner']
            prv = True
        except:
            pass
        try:
            owpu = tgs['public'][tag]['owner']
            pub = True
        except:
            pass
        if prv:
            usr = await self.bot.get_user_info(owpr)
            await ctx.send(f"The owner of the private tag `{tag}` is {usr.name}#{usr.discriminator}.")
        if pub:
            usr = await self.bot.get_user_info(owpu)
            await ctx.send(f"The owner of the public tag `{tag}` is {usr.name}#{usr.discriminator}.")
        if not prv and not pub:
            await ctx.send("That tag does not exist.")  

def setup(bot):
    bot.add_cog(Tags(bot))