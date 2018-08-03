import discord
from discord.ext import commands
import random, os, re, traceback, asyncio, json
from datetime import datetime
from cogs.helprs.suggestions import suggestions

#emb = 0xF2CEFE        

def Galerr(Exception):
    pass

class IMGGallery:

    def __init__(self, bot):
        self.bot = bot
    
    def modjsn(self, id, add, user):
        jsn = json.load(open('igl.json'))
        #id = id
        if user:
            ed = jsn['user']
        else:
            ed = jsn['channel']
        if add:
            ed.append(id)
        else:
            ed.remove(id)
        json.dump(jsn, open('igl.json', 'w'), sort_keys=True, indent=2)
   
    @commands.group(invoke_without_command=True)
    async def imggal(self, ctx, *args):
        """Initiates IMGGal.
        [imggal]"""
        #for x in open('igl.txt').read().split('\n'):
        #    if str(ctx.message.author.id) == x:
        #        return await ctx.send(f'{ctx.message.author.mention}, you already have an IMGGal session going on!')
        #with open('igl.txt', 'r+') as igl:
        #    lns = igl.readlines()
        #    lns.append(str(ctx.message.author.id))
        #    print(lns)
        #    igl.writelines(lns) 
        mjsn = json.load(open('igl.json'))
        if ctx.channel.id in mjsn['channel']:
            return await ctx.send(f'{ctx.message.author.mention}, there already is an IMGGal session going on in this channel!')
        elif ctx.message.author.id in mjsn['user']:
            return await ctx.send(f'{ctx.message.author.mention}, you already have an IMGGal session going on!')
        self.modjsn(ctx.channel.id, True, False)
        self.modjsn(ctx.message.author.id, True, True)
        imggali = os.listdir("imggal")
        imggali.remove("colors.json")
        if len(args) == 1:
            args = args[0].split()
        for x in imggali:
            if len(os.listdir(f"imggal/{x}")) == 0:
                imggali.remove(x)
        try:
            imggaln = args[0]
            #print(imggaln)
            #print("h")
            if not imggaln in imggali:
                if imggaln[0] == "-":
                    imggali.remove(imggaln[1:])
                if len(imggali) == 0:
                    imggali = os.listdir("imggal")        
                raise ValueError()
        except:
            imggaln = random.choice(imggali)
        #print(imggaln)
        img_list = os.listdir("imggal/" + imggaln)
        imgl = len(img_list)
        imggaln = imggaln.replace("_", " ")
        try:
            img = args[1]
            if not img in img_list:
                if img[0] == "-":
                    img_list.remove(img[1:])
                raise ValueError()
        except:
            if len(img_list) == 0:
                await ctx.invoke(self.imggal)
            img = random.choice(img_list)
            img_dir = os.path.join("imggal", imggaln, img)
            img = re.sub(r"[^a-zA-Z0-9.]","",img)
        if len(img) > 20:
            img = img[-20:]
        disp = imggaln.title()
        if not disp.endswith("s"):
            disp = disp + "s"
        disp = disp + "."
        with open("imggal/colors.json") as clrs:
            clls = json.load(clrs)
            try:
                clr = discord.Color(clls[imggaln])
            except:
                clr = discord.Color(random.randint(0, 16777215))
        embed = discord.Embed(title = disp.replace(".", ""), description = 'Showing 1 of {} {}\nRequested by {}.'.format(imgl, disp, ctx.message.author.name) + '\n```(React with:\n🔁 to reroll image\n❌ to disable\nand 🔀 to shuffle IMGGals.)```', color = clr)
        if ctx.message.author.avatar != None:
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=128".format(ctx.message.author))
        embed.set_image(url='attachment://{}'.format(img))
        embed.set_footer(text="This IMGGal will be unusable in 2 minutes.")
        embed.timestamp = datetime.utcnow()
        try:      
            reactionlist = ['🔁','❌','🔀']      
            def check(r, user):
                if user != ctx.message.author:
                    return False
                if r.emoji not in reactionlist:
                    return False
                else:
                    return True
            msg = await ctx.send(file=discord.File(img_dir, img), embed=embed)
            for x in reactionlist:
                await msg.add_reaction(x)
            choice = await self.bot.wait_for('reaction_add', check = check, timeout = 120.0)

            if (choice[0].emoji == '🔁'):
                await msg.delete()
                self.modjsn(ctx.message.author.id, False, True)
                self.modjsn(ctx.channel.id, False, False)
                return await ctx.invoke(self.imggal, "{0} -{1}".format(imggaln, img))

            if (choice[0].emoji == '❌'):
                await msg.clear_reactions()
                embed.set_footer(text="This IMGGal is disabled.")
                await msg.edit(embed=embed)
                self.modjsn(ctx.message.author.id, False, True)
                self.modjsn(ctx.channel.id, False, False)

            if (choice[0].emoji == '🔀'):
                await msg.delete()
                self.modjsn(ctx.message.author.id, False, True)
                self.modjsn(ctx.channel.id, False, False)
                return await ctx.invoke(self.imggal, "-{0}".format(imggaln))
                
        except asyncio.futures.TimeoutError:
            #await msg.delete()
            try:
                await msg.clear_reactions()
                embed.set_footer(text="This IMGGal is expired.")
                await msg.edit(embed=embed)
            except:
                pass
            #self.remname(ctx.message.author.id)
            self.modjsn(ctx.message.author.id, False, True)
            self.modjsn(ctx.channel.id, False, False)

    @imggal.command(name="list")
    async def _list(self, ctx):
        """Lists all the IMGGal choices."""
        lst = os.listdir("imggal")
        lst.remove("colors.json")
        for y, x in enumerate(lst):
            if len(os.listdir(os.path.join("imggal", x))) == 0:
                lst[y] = x + " (Empty)"
            else:
                lst[y] = x + " ({} images)".format(str(len(os.listdir(os.path.join("imggal", x)))))
        await ctx.send(f"List of current IMGGals:\n`{', '.join(lst)}`")

    @imggal.command()
    async def submit(self, ctx, imggal, *imgs):
        """Adds an image(s) to an IMGGal.
        <imggal> <image link(s) or upload>"""
        if len(imgs) != 0:
            img = list(imgs)
        else:
            img = []
            for x in ctx.message.attachments:
                img.append(x.url)
        if not imggal in os.listdir('imggal'):
            return await ctx.send("That is not a valid IMGGal.")
        #check for valid image
        for y in img:
            if not any(y.endswith(x) for x in ['.png', '.jpg', '.jpeg', '.webp', '.gif']):
                return await ctx.send("Please give a valid image.")
        if len(img) == 1:
            img = img[0]
        e = discord.Embed(title="IMGGal Gallary Addition")
        try:
            await suggestions.add("dummy", self.bot, ctx, "imggal-img", img, e, True, imggal)
        except:
            traceback.print_exc()
            return await ctx.send("An error occured.")
        await ctx.send("Submission sent.")

    @imggal.command()
    async def request(self, ctx, imggal, *color):
        """Requests for an IMGGal to be made.
        Color is best made an integer color or hex color prefixed with "0x".
        (e.x: color = 16777254 or color = 0xFFFFFF)
        <imggal request> [color]"""
        e = discord.Embed(title="IMGGal Addition")
        if len(color) != 0:
            try:
                color = int(color[0])
                e.colour == discord.Colour(color)
            except:
                pass
        try:
            await suggestions.add("dummy", self.bot, ctx, "imggal", None, e, True, imggal)
        except:
            traceback.print_exc()
            return await ctx.send("An error occured.")
        await ctx.send("Request sent.")


def setup(bot):
    bot.add_cog(IMGGallery(bot))
