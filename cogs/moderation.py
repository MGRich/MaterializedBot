import discord
from discord.ext import commands
from asyncio import sleep
import traceback, json
#import ..util.suggestions

data = json.load(open("info.json"))

#def admin(ctx):
#    ams = [data['owners'], ctx.guild.owner.id]
 #   try:
  #      if os.path.exists("config/{}/config.json".format(ctx.guild.id)):
   #         with open("config/{}/config.json".format(ctx.guild.id)) as cfg:
    #            con = json.load(cfg)
     #           ams = con['admins']
    #except:
     #   ams = [data['owners'], ctx.guild.owner.id]
    #for x in ams:
     #   str(x) = x
      #  if x[1] == "r":
       #     if kannaa


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason):
        """Bans a user. 
        <member> [reason]"""
        #if len(args) == 0:
        #    await ctx.send("Please list a valid to ban.")
        #    return
        #try:
        #    memb = ctx.message.raw_mentions[0]
        #except:
        #    memb = int(args[0])
        memb = member
        if memb == ctx.message.author:
            return await ctx.send("Just leave the server and never come back?")
        #print(member)
        reasn = reason + " - Ban by {}".format(ctx.message.author)
        try:
            try:
                usrm = await memb.send("You were banned from {} for reason: {}".format(ctx.guild.name, reasn))
            except:
                pass
            await ctx.guild.ban(memb, reason=reasn, delete_message_days=0)
        except discord.Forbidden:           
            try:
                await usrm.edit(content="Disregard message, error occured.")
            except:
                pass
            return await ctx.send("I don't seem to have the correct permissions to do so.")
        except Exception as e:            
            try:
                await usrm.edit(content="Disregard message, error occured.")
            except:
                pass
            traceback.print_exc()
            return await ctx.send("Unknown error occured: `{}`".format(e))       
        await ctx.send("User successfully banned.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *, reason):
        """Kicks a user.
        <member> [reason]"""
        #if len(args) == 0:
        #    await ctx.send("Please list a valid to ban.")
        #    return
        #try:
        #    memb = ctx.message.raw_mentions[0]
        #except:
        #    memb = int(args[0])
        memb = member
        if memb == ctx.message.author:
            return await ctx.send("Just leave the server?")
        #print(member)
        reasn = reason + " - Kick by {}".format(ctx.message.author)
        try:
            try:
                usrm = await memb.send("You were kicked from {} for reason: {}".format(ctx.guild.name, reasn))
            except:
                pass
            await ctx.guild.kick(memb)
        except discord.Forbidden:
            try:
                await usrm.edit(content="Disregard message, error occured.")
            except:
                pass
            return await ctx.send("I don't seem to have the correct permissions to do so.")
        except Exception as e:
            try:
                await usrm.edit(content="Disregard message, error occured.")
            except:
                pass
            traceback.print_exc()
            return await ctx.send("Unknown error occured: `{}`".format(e))
        await ctx.send("User successfully kicked.")

    #@commands.command()
    #async def test(self, ctx):
        #g = ctx.guild
        #c = ctx.channel
        #print(f"{repr(g)}, {repr(c)}")
        #self.bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, count=1000, member: discord.Member=None):
        """Purges messages.
        [count] [member]"""
        if count > 1000:
            return await ctx.send("Too many messages.")
        count += 1
        if member:
            if ctx.message.author != member:
                count -= 1
        def check(msg):
            if member:
                return msg.author == member
            return True
        await ctx.channel.purge(limit=count, check=check)
        msg = await ctx.send(f"Purged {count-1} messages!")
        await sleep(3)
        await msg.delete()

    #@commands.command()
    #@commands.bot_has_permissions(manage_messages=True)
    #async def cleanup(self, ctx, count=100):
    #    if count > 100:
    #        return await ctx.send("Too many messages.")
     #   count += 1
      #  if member:
       #     if ctx.message.author != member:
        #        count -= 1
        #def check(msg):
         #   if member:
          #      return msg.author == member
           # return True
    #    await ctx.channel.purge(limit=count, check=check)
     #   msg = await ctx.send(f"Purged {count-1} messages!")
      #  await sleep(3)
       # await msg.delete()
        
    #@commands.command()
    #@commands.guild_only()
    #@commands.has_permissions()

def setup(bot):
    bot.add_cog(Moderation(bot))

    