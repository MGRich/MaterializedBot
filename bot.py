import discord
from discord.ext import commands
import traceback, json, os, inspect, sys, re, aiohttp, asyncio
from pprint import pprint #as print
#from cogs.helprs import suggestions

stable = False
try:
    if sys.argv[1] == "stable":
        data = json.load(open("stable.json"))
    else:
        raise ValueError()
except:
    data = json.load(open("info.json"))
#pprint(data)

if data['stable']:
    stable = True

def prefix(bot, message):
    prf = data['prefix']
    try:
        prf.remove("")
    except:
        pass
    if not message.guild:
        prf.append("")
    else:
        if os.path.exists("config/{}/config.json".format(message.guild.id)):
            with open("config/{}/config.json".format(message.guild.id)) as cfg:
                con = json.load(cfg)
                try:
                    prf[0] = con['prefix']
                except:
                    pass
    return commands.when_mentioned_or(*prf)(bot, message)

def ownerch():
    return commands.check(lambda ctx: any(x in [data['owners'], ctx.guild.owner.id] for x in [ctx.message.author.id, ctx.guild.owner.id]))

def ownerbt():
    return commands.check(lambda ctx: ctx.message.author.id == 214550163841220609)


#fetch cogs
cgs = []
for x in os.listdir("cogs"):
    if os.path.isfile("cogs/" + x):
        cgs.append("cogs.{}".format(x[:-3]))

bot = commands.Bot(command_prefix=prefix, description="A general bot meant for any type of server.")
blocks = json.load(open("blocks.json"))
bot.remove_command('help')

if __name__ == '__main__':
        for cog in cgs:
            try:
                bot.load_extension(cog)
            except:
                print("Failed to load {}.\n".format(cog))
                traceback.print_exc()
                print("")

async def process_commands(msg):
    #this is just a simple check to normally process a command with processing normal blocks
    #print(blocks['blocks'])
    #print(msg.author.id)
    if msg.author.id == 214550163841220609:
        return await bot.process_commands(msg)
    if msg.author.id in blocks['blocks']:
        try:
            await msg.author.send('You are blocked from using the bot. If you have any complains, please contact RMGRich by PMing the stable bot (which may be this one).')
        except:
            pass
        return
    return await bot.process_commands(msg)

@bot.command(pass_context=True, hidden=True)
@ownerbt()
async def block(ctx, member:discord.Member):
    blocks['blocks'].append(member.id)
    json.dump(blocks, open("blocks.json", "w"))

@bot.command(pass_context=True, hidden=True)
@ownerbt()
async def unblock(ctx, member:discord.Member):
    try:
        blocks['blocks'].remove(member.id)
    except:
        return
    json.dump(blocks, open("blocks.json", "w"))

@bot.event
async def on_ready():
    print(f'\n\nin as: {bot.user.name} - {bot.user.id}\non version: {discord.__version__}\n')
    #while True:
    #    try:
    await bot.change_presence(activity=discord.Activity(name=f"Version {data['version']}! | {data['prefix'][0]}help", type=0))
    #    except Exception as e:
     #       #print(type(e).__name__)
      #      if type(e).__name__ == "ConnectionClosed":
       #         pass
        #    else:
         #       traceback.print_exc()
        #asyncio.sleep(120)

@bot.event
async def on_raw_reaction_add(payload):
    #print(payload, payload.user_id, payload.channel_id, payload.message_id)
    if not stable:
        return
    if not payload.emoji.name in ['✅', '❌']:
        return
    if not payload.user_id in data['owners']:
        return
    #print('passed owner')
    if not payload.channel_id in [465318267410710551, 465315532602605568, 465315567331704832, 465315853194231810, 465315940813504514, 465314187527323649]:
        return
    #print('passed channel')
    dat = json.load(open("suggestions.json"))
    #print(payload.message_id in dat['list'])
    if not payload.message_id in dat['list']:
        #print('did not pass message')
        return
    dat['list'].remove(payload.message_id)
    #print('passed message')
    #finna get to the gOOoOOOOOOODD 
    sta = payload.emoji.name
    if sta == '✅':
        sta = True
    elif sta == '❌':
        sta = False
    #srv = bot.get_guild(payload.guild_id)
    chl = bot.get_channel(payload.channel_id)
    msg = await chl.get_message(payload.message_id)
    emb = msg.embeds[0]
    id = emb.footer.text
    idd = dat.pop(id, None)
    memb = await bot.get_user_info(idd['author'])
    ids = []
    for x, y in idd.items():
        ids.append("{0}: {1}".format(x.title(), y))
    ids = '\n'.join(ids)
    #handle message
    out = bot.get_channel(465598663540998144)
    if sta == True:
        try:
            await memb.send(f"Your {idd['type']} request has been approved!\nInfo:\n```\n{ids}\n```\n(You may not understand what any of this means, but that's OK.)")
        except:
            pass
        await out.send(f"accepted\n```\n{ids}\n```")
    else:
        try:
            await memb.send(f"Your {idd['type']} request has been denied.\nInfo:\n```\n{ids}\n```\n(You may not understand what any of this means, but that's OK.)")
        except:
            pass
        await out.send(f"denied\n```\n{ids}\n```")
    #handle type specific stuff
    if sta == True:
        if idd['type'] == "imggal-img":
            async with aiohttp.ClientSession() as session:
                for x in idd['image']:
                    nm = os.path.join("imggal", idd['imggal'], os.path.split(x)[1])
                    if os.path.exists(nm):
                        typ = x.split('.')[-1]
                        z = 1
                        while True:
                            nm = os.path.join("imggal", idd['imggal'], os.path.split(str(z) + "." + typ)[1])
                            if os.path.exists(os.path.join("imggal", idd['imggal'], os.path.split(str(z) +  "." + typ)[1])):
                                z += 1
                            else:
                                break
                    #print(nm)
                    async with session.get(x) as resp:
                        with open(nm, 'wb') as fle:
                            while True:
                                chunk = await resp.content.read(1024)
                                if not chunk:
                                    break
                                fle.write(chunk)
        elif idd['type'] == "imggal":
            os.mkdir(f"imggal//{idd['imggal']}")
    #finalize
    await msg.delete()
    json.dump(dat, open("suggestions.json", "w"), sort_keys=True, indent=2)

@bot.event
async def on_message(msg):
    #print(type(msg.channel))
    if msg.content.startswith("r/"):
        await msg.channel.send(f"https://reddit.com/{msg.content.split()[0]}")
    if not stable:
        return await process_commands(msg)
    if (type(msg.channel) == discord.channel.DMChannel) and (msg.author.id != 464546343797391371):
        out = bot.get_channel(465702754925412363)
        e = discord.Embed(title="DM Sent", description=msg.content)
        if msg.author.avatar != None:
            e.set_thumbnail(url="https://cdn.discordapp.com/avatars/{0.id}/{0.avatar}.png?size=128".format(msg.author))
        e.set_author(name="{0.name}#{0.discriminator}".format(msg.author))
        e.set_footer(text=str(msg.author.id))
        att = []
        if any(s in msg.content.lower() for s in ["rich", "rmg", "rmgrich"]):
            e.colour = discord.Colour(0xF12067)
            att.append("<@214550163841220609>")
        if len(msg.attachments) != 0:
            for x in msg.attachments:
                att.append(x.url)
            att.append("attachments sent")
        else:
            if len(att) == 0:
                att = ""
        att = '\n'.join(att)
        return await out.send(att, embed=e)
    if msg.author.id != 214550163841220609:
        return await process_commands(msg)
    if msg.channel.id != 465702754925412363:
        return await process_commands(msg)
    try:
        msgc = msg.content
        msgc = msgc.split(' ', 1)
        id = int(msgc[0])
        con = msgc[1]
        memb = await bot.get_user_info(id)
        try:
            await memb.send(f"From RMGRich:\n\n{con}")
        except:
            traceback.print_exc()
            return await msg.channel.send("rip didnt FUNCTIONE")
        #await msg.channel.send("yes good")
    except:
        return await process_commands(msg)


#@bot.event
#async def on_message(msg):
#    #print(type(msg.channel)
#    if 464546343797391371 in msg.raw_mentions: 
#        if not msg.guild:
#            await msg.channel.send("You can simply type a command name in DMs.")
#            return
#        else:
#            if os.path.exists("config/{}/config.json".format(msg.guild.id)):
#                with open("config/{}/config.json".format(msg.guild.id)) as cfg:
#                    con = json.load(cfg)
#                    pref = con['prefix']
#            await msg.channel.send("My prefix here is {}. You can change it with `!prefix`.".format(pref))

@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return

        
    ignored = (commands.CommandNotFound, commands.UserInputError)
    error = getattr(error, 'original', error)
    
    if isinstance(error, ignored):
        return
    elif isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.')
    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.message.author.send(f'{ctx.command} can not be used in Private Messages.')
        except:
            pass
    elif isinstance(error, commands.BadArgument):
        return await ctx.send("remember you cant use double quote u dip")
    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(error)
    elif isinstance(error, commands.CheckFailure):
        return await ctx.send("You are not able to use this command.")
        
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


@bot.command(pass_context = True, hidden=True)
@ownerbt()
async def reload(ctx, *cogs):
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
            print(f"attempt to load {cog}")
            bot.unload_extension(cog)
            bot.load_extension(cog)
            print(f"loaded {cog}")
        except:
            bot.unload_extension(cog)
            await ctx.send("Failed to load {}. Check console for details.".format(cog))
            print("-----START {}".format(cog))
            traceback.print_exc()
            print("-----END   {}".format(cog))
            err = True
    if not err:
        await ctx.send("All loaded successfully.")

@bot.command(pass_context = True, hidden=True)
@ownerbt()
async def unload(ctx, *cogs):
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
            bot.unload_extension(cog)
            print(f"unloaded {cog}")
        except:
            bot.unload_extension(cog)
            await ctx.send("Failed to load {}. Check console for details.".format(cog))
            print("-----START {}".format(cog))
            traceback.print_exc()
            print("-----END   {}".format(cog))
            err = True
    if not err:
        await ctx.send("All unloaded successfully.")


@bot.command(pass_context=True, name="eval")
@ownerbt()
async def _eval(ctx, *args):
    """Command only Rich and the server owner can do."""
    evl = ' '.join(args)
    t = None
    env = {
        'bot': bot,
        'ctx': ctx
    }
    env.update(globals())
    e = discord.Embed(title="EVAL", colour=discord.Color(0x71CD40))
    e.add_field(name="Input", value="`" + evl + "`")
    try:
        t = str(eval(evl, env))
        if inspect.isawaitable(t):
            t = await t
    except Exception as err:
        e.description = "It failed to run."
        e.colour = discord.Colour(0xFF0000)
        t = str(err)
    e.add_field(name="Output", value="`" + t + "`")
    await ctx.send(embed=e)

#@bot.command(pass_context=True)
#@ownerch()
#async def test(ctx, member:discord.Member, *args):
#    await member.send(' '.join(args))


#@bot.command(pass_context = True)
#@ownerch()
    
#@bot.command(name="test")
#async def _help(ctx, *args):
#    """Displays this command.
#    [category] [command]"""
#    e = discord.Embed()
#    args = list(args)
#    if len(args) >= 1:
#        args[0] == args[0].lower
#        e.title = "Category: {}".format(args[0].title())
#        if len(args) == 2:
#            args[1] = "_" + args[1].lower()
#            desc = eval("{}.{}.__doc__".format(args[0], args[1]))
#            await ctx.send(desc.split('\n'))
#            return
#    await ctx.send(args)

bot.run(data['token'], bot=True, reconnect=True)