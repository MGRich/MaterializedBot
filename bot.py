import discord, traceback, json, os, sys, asyncio, aiohttp, contextlib, io, inspect
from discord.ext import commands

data = json.load(open("info.json"))
#print(data)

stable = data['stable']


def ownerbt():
    return commands.check(lambda ctx: ctx.message.author.id == 214550163841220609)


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

cgs = []
for x in os.listdir("cogs"):
    if os.path.isfile("cogs/" + x):
        cgs.append("cogs.{}".format(x[:-3]))

bot = commands.Bot(command_prefix=prefix, description="A general bot meant for any type of server.")
blocks = json.load(open("blocks.json"))
bot.remove_command('help')


@bot.command(name="eval")
@ownerbt()
async def _eval(ctx, *, evl: str):
    t = None
    env = {
        'bot': bot,
        'ctx': ctx
    }
    @contextlib.contextmanager
    def stdoutIO(stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = io.StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old
    env.update(globals())
    e = discord.Embed(title="EVAL", colour=discord.Color(0x71CD40), description="Execution was successful!")
    #e.add_field(name="Input", value=f"```py\n{evl}```")
    try:
        with stdoutIO() as s:
            t = exec(evl, env)
            if inspect.isawaitable(t):
                t = await t
            t = s.getvalue()
    except:
        e.description = f"It failed to run."
        e.colour = discord.Colour(0xFF0000)
        t = traceback.format_exc()
        t = t.replace("cliri", ".")
    e.description = e.description + f"\n```py\n{t}```"
    try:
        await ctx.send(embed=e)
    except discord.HTTPException:
        await ctx.send("It worked (probably), but the output was too big.")

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
    q = []
    msg = await ctx.send("Reloading cogs..\n```diff\n! Awaiting edits..```")
    old = tuple(bot.extensions)
    if len(old) != len(mcgs):
        old = mcgs
    #print(old)
    for cog in old:
        bot.unload_extension(cog)
        q.append(f"\n- {cog}")
    await msg.edit(content=msg.content[:-21] + ''.join(q) + "```")
    q = []
    count = 0
    for cog in mcgs:
        count += 1
        #print(len(q))
        try:
            bot.load_extension(cog)
            q.append(f"\n+ {cog}")
            #print(cog)
        except:
            bot.unload_extension(cog)
            q.append(msg.content.replace(f"\n! {cog}"))
            print("-----START {}".format(cog))
            traceback.print_exc()
            print("-----END   {}".format(cog))
            err = True
        finally:
            if (len(mcgs) == count) and (len(q) > 0):
                await msg.edit(content=msg.content[:-3] + ''.join(q) + "```")
                q = []
    if not err:
        await msg.edit(content=msg.content + "\nAll loaded successfully.")


async def process_commands(msg):
    if msg.author.id == 214550163841220609:
        return await bot.process_commands(msg)
    if msg.author.id in blocks['blocks']:
        try:
            await msg.author.send('You are blocked from using the bot. If you have any complains, please contact RMGRich by PMing the stable bot (which may be this one).')
        except:
            pass
        return
    return await bot.process_commands(msg)

@bot.event
async def on_ready():
    print(f'\n\nin as: {bot.user.name} - {bot.user.id}\non version: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Activity(name=f"Version {data['version']}! | {data['prefix'][0]}help", type=0))

@bot.event
async def on_raw_reaction_add(payload):
    if not stable:
        return
    if not payload.emoji.name in ['✅', '❌']:
        return
    if not payload.user_id in data['owners']:
        return
    if not payload.channel_id in [465318267410710551, 465315532602605568, 465315567331704832, 465315853194231810, 465315940813504514, 465314187527323649]:
        return
    dat = json.load(open("suggestions.json"))
    if not payload.message_id in dat['list']:
        return
    dat['list'].remove(payload.message_id)
    sta = payload.emoji.name
    if sta == '✅':
        sta = True
    elif sta == '❌':
        sta = False
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
                    async with session.get(x) as resp:
                        with open(nm, 'wb') as fle:
                            while True:
                                chunk = await resp.content.read(1024)
                                if not chunk:
                                    break
                                fle.write(chunk)
        elif idd['type'] == "imggal":
            os.mkdir(f"imggal//{idd['imggal']}")
    await msg.delete()
    json.dump(dat, open("suggestions.json", "w"), sort_keys=True, indent=2)

@bot.event
async def on_message(msg):
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
    except:
        return await process_commands(msg)

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

@bot.command()
@ownerbt()
async def updbot(ctx, force=None):
    console="py"
    await ctx.send("Unloading all cogs..")
    for x in tuple(bot.extensions):
        bot.unload_extension(x)
    await ctx.send("Logging off, check console for further progress..")
    #await bot.close()
    print("Logged out. Starting the git process..")
    if stable:
        br = "master"
    else:
        br = "dev"
    if force:
        br = "dev"
    os.system(f"git clone --single-branch -b {br} https://github.com/MGRich/MaterializedBot.git git")
    if stable:
        os.system("ren git\\bot.py git\\bot.pyw")
    print("Moving..")
    os.system("xcopy /e /y git .")
    print("Deleting..")
    os.system("rmdir /s /q git")
    print("Commence restart.")
    os.execv(sys.executable, [console])

@bot.command()
@ownerbt()
async def restart(ctx, console="py"):
    await ctx.send("Unloading all cogs..")
    for x in tuple(bot.extensions):
        bot.unload_extension(x)
    await ctx.send("Restarting..")
    #await bot.close()
    print("Commence restart.")
    os.execv(sys.executable, [console])

    

if __name__ == '__main__':
        for cog in cgs:
            try:
                bot.load_extension(cog)
            except:
                print("Failed to load {}.\n".format(cog))
                traceback.print_exc()
                print("")
        bot.run(data['token'], bot=True, reconnect=True)
