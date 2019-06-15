import discord
from discord import Embed
from discord.ext import commands
import os

class Moderation(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        @bot.command(name="sync")
        @commands.guild_only()
        @commands.bot_has_permissions(ban_members=True)
        @commands.has_permissions(ban_members=True)
        async def _sync(ctx):
            """Sync the bans."""
            banguild = bot.get_guild(int(os.getenv('banlistguild')))
            ban_list = await banguild.bans()
            banCount = 0
            banCountAll = len(ban_list)
            embed = discord.Embed(title="Sync in progress...", color=discord.Color.green(),
                description="0% complete! 👌")
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            #Causes lag in embed - embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/485934104156569600/happysuccess.gif")
            embed_message = await ctx.send(embed=embed)
            for BanEntry in ban_list:
                try:
                    await ctx.guild.ban(BanEntry.user, reason=f"WatchDog - Global Ban")
                except:
                    channel = bot.get_channel(int(os.getenv('botlogfail')))
                    await channel.send("**[Info]** Could not syncban the user `%s` (%s) in the guild `%s` (%s)" % (BanEntry.user.name, BanEntry.user.id, ctx.guild.name, ctx.guild.id))
                    print("**[Info]** Could not syncban the user `%s` (%s) in the guild `%s` (%s)" % (BanEntry.user.name, BanEntry.user.id, ctx.guild.name, ctx.guild.id))
                banCount += 1
                percentRaw = (banCount/banCountAll)*100
                percent = round(percentRaw, 1)
                percent0 = round(percentRaw, 0)
                if (percent0 == 25) or (percent0 == 50) or (percent0 == 75):
                    embed = discord.Embed(title="Sync in progress...", color=discord.Color.green(),
                        description="%s%% complete! 👌" % percent)
                    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
                    #Causes lag in embed - embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/485934104156569600/happysuccess.gif")
                    await embed_message.edit(embed=embed)
            embed = discord.Embed(title="Sync complete", color=discord.Color.green(),
                description="Synchronisation complete! 👌")
            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/485934104156569600/happysuccess.gif")
            await embed_message.edit(embed=embed)

        @bot.command(name="revsync", aliases=["reversesync"])
        @commands.guild_only()
        @commands.bot_has_permissions(ban_members=True)
        async def _revsync(ctx):
            """Sync bans from server to central, and other guilds."""
            ban_list = await ctx.guild.bans()
            banguild = bot.get_guild(int(os.getenv('banlistguild')))
            banguild_ban_list = await banguild.bans()
            mods = list(map(int, os.getenv("mods").split()))
            if ctx.author.id in mods:
                banCount = 0
                banCountAll = len(ban_list)
                embed = discord.Embed(title="Revsync in progress...", color=discord.Color.green(),
                    description="0% complete! 👌")
                embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                #Causes lag in embed - embed.set_image(url="https://cdn.discordapp.com/attachments/485619099481800714/485917795679338496/1521567278_980x.gif")
                embed_message = await ctx.send(embed=embed)

                for BanEntry in ban_list:
                    banned = False

                    for BanEntry2 in banguild_ban_list:
                        if BanEntry2.user.id == BanEntry.user.id:
                            banCount += 1
                            print(str(banCount) + "/" + str(banCountAll) + " User already banned, skipping - " + BanEntry.user.name)
                            ban_list_list = list(ban_list)
                            ban_list_list.remove(BanEntry)
                            ban_list = tuple(ban_list_list)
                            #Does the embed change
                            percentRaw = (banCount/banCountAll)*100
                            percent = round(percentRaw, 1)
                            percent0 = round(percentRaw, 0)
                            if (percent0 == 25) or (percent0 == 50) or (percent0 == 75):
                                embed = discord.Embed(title="Revsync in progress...", color=discord.Color.green(),
                                    description="%s%% complete! 👌" % percent)
                                embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                                await embed_message.edit(embed=embed)
                            banned = True
                            break
                    if banned == True:
                        continue
                    elif BanEntry.user == ctx.bot.user:
                        channel = bot.get_channel(int(os.getenv('botlogfail')))
                        await channel.send("**[Alert]** Someone tried to ban the bot during a revsync. Moderator: `%s` (%s) in the guild `%s` (%s)" % (ctx.author.name, ctx.author.id, guild.name, guild.id))
                        print("**[Alert]** Someone tried to ban the bot during a revsync. Moderator: `%s` (%s) in the guild `%s` (%s)" % (ctx.author.name, ctx.author.id, guild.name, guild.id))
                        
                        ban_list_list = list(ban_list)
                        ban_list_list.remove(BanEntry)
                        ban_list = tuple(ban_list_list)
                        continue
                    elif BanEntry.user.id in mods:
                        channel = bot.get_channel(int(os.getenv('botlogfail')))
                        await channel.send("**[Alert]** Someone tried to ban a Global Moderator during a revsync. Moderator: `%s` (%s) in the guild `%s` (%s)" % (ctx.author.name, ctx.author.id, guild.name, guild.id))
                        print("**[Alert]** Someone tried to ban a Global Moderator during a revsync. Moderator: `%s` (%s) in the guild `%s` (%s)" % (ctx.author.name, ctx.author.id, guild.name, guild.id))
                        
                        ban_list_list = list(ban_list)
                        ban_list_list.remove(BanEntry)
                        ban_list = tuple(ban_list_list)
                        continue
                    else:
                        banCount += 1
                        print(str(banCount) + "/" + str(banCountAll) + " User not banned, banning - " + BanEntry.user.name)
                        #checks other guilds
                        for guild in bot.guilds:
                            #checks if own guild, if it is, skip
                            if guild != ctx.guild:
                                #tries to ban
                                try:
                                    await guild.ban(BanEntry.user, reason=f"WatchDog - Global Ban")
                                except:
                                    channel = bot.get_channel(int(os.getenv('botlogfail')))
                                    await channel.send("**[Info]** Could not revsyncban the user `%s` (%s) in the guild `%s` (%s)" % (BanEntry.user.name, BanEntry.user.id, guild.name, guild.id))
                                    print("**[Info]** Could not revsyncban the user `%s` (%s) in the guild `%s` (%s)" % (BanEntry.user.name, BanEntry.user.id, guild.name, guild.id))
                        #Does the embed change
                        percentRaw = (banCount/banCountAll)*100
                        percent = round(percentRaw, 1)
                        percent0 = round(percentRaw, 0)
                        if (percent0 == 25) or (percent0 == 50) or (percent0 == 75):
                            embed = discord.Embed(title="Revsync in progress...", color=discord.Color.green(),
                                description="%s%% complete! 👌" % percent)
                            embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                            await embed_message.edit(embed=embed)
                        #Do this when done
                        #Sends a message in the botlog
                        channel = bot.get_channel(int(os.getenv('botlog')))
                        await channel.send(embed=Embed(color=discord.Color.red(), description="Moderator `%s` banned `%s` - (%s)" % (ctx.author.name, BanEntry.user.name, BanEntry.user.id)))
                        print(str(banCount) + "/" + str(banCountAll) + " Moderator `%s` banned `%s` - (%s)" % (ctx.author.name, BanEntry.user.name, BanEntry.user.id))
                        #Send public ban notif in public ban list
                        pblchannel = bot.get_channel(int(os.getenv('pbanlist')))
                        pblembed = discord.Embed(title="Account banned", color=discord.Color.red(),
                            description="`%s` has been globally banned" % BanEntry.user.id)
                        pblembed.set_footer(text="%s has been globally banned" % BanEntry.user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                        pblembed.set_thumbnail(url=BanEntry.user.avatar_url)
                        await pblchannel.send(embed=pblembed)
                        #Send private ban notif in private moderator ban list
                        prvchannel = bot.get_channel(int(os.getenv('prvbanlist')))
                        prvembed = discord.Embed(title="Account banned", color=discord.Color.red(),
                            description="`%s` has been globally banned" % BanEntry.user.id)
                        prvembed.add_field(name="Moderator", value="%s (`%s`)" % (ctx.author.name, ctx.author.id), inline=True)
                        prvembed.add_field(name="Name when banned", value="%s" % BanEntry.user, inline=True)
                        prvembed.add_field(name="In server", value="%s (`%s`)" % (ctx.guild.name, ctx.guild.id), inline=True)
                        prvembed.add_field(name="In channel", value="%s (`%s`)" % (ctx.channel.name, ctx.channel.id), inline=True)
                        prvembed.set_footer(text="%s has been globally banned" % BanEntry.user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                        prvembed.set_thumbnail(url=BanEntry.user.avatar_url)
                        await prvchannel.send(embed=prvembed)
                #send final embed, telling the ban was sucessful
                embed = discord.Embed(title="Revsync complete", color=discord.Color.green(),
                    description="Reverse synchronisation complete! %s accounts have been globally banned 👌" % len(ban_list))
                embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_image(url="https://cdn.discordapp.com/attachments/485619099481800714/485917795679338496/1521567278_980x.gif")
                await embed_message.edit(embed=embed)
            else:
                await ctx.send(embed=Embed(color=discord.Color.red(), description="You are not a Global Moderator! Shame!"))

        @bot.command(name="ban")
        async def _ban(ctx, user_id: int, *, reason = "No reason given"):
            """Bans a user globally."""
            mods = list(map(int, os.getenv("mods").split()))
            if ctx.author.id in mods:
                user = await ctx.bot.fetch_user(user_id)
                if user == ctx.bot.user:
                    await ctx.send(embed=Embed(color=discord.Color.red(), description="What are you trying to do? Shame!"))
                elif user.id in mods:
                    await ctx.send(embed=Embed(color=discord.Color.red(), description="You cannot ban a Global Moderator, sorry!"))
                else:
                    #Sends main embed
                    guild = []
                    guildCount = 0
                    guildCountAll = len(bot.guilds)
                    embed = discord.Embed(title="Account is being banned...", color=discord.Color.green(),
                        description="0% complete! 👌")
                    embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                    #Causes lag in embed - embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/475498849696219141/ban.gif")
                    embed_message = await ctx.send(embed=embed)
                    #Sends a message in the botlog
                    channel = bot.get_channel(int(os.getenv('botlog')))
                    await channel.send(embed=Embed(color=discord.Color.red(), description="Moderator `%s` banned `%s` - (%s)" % (ctx.author.name, user.name, user.id)))
                    print("Moderator `%s` banned `%s` - (%s)" % (ctx.author.name, user.name, user.id))
                    #checks guilds
                    for guild in bot.guilds:
                        #tries to ban
                        try:
                            await guild.ban(user, reason=f"WatchDog - Global Ban")
                        except:
                            channel = bot.get_channel(int(os.getenv('botlogfail')))
                            await channel.send("**[Info]** Could not ban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, guild.name, guild.id))
                            print("**[Info]** Could not ban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, guild.name, guild.id))
                        #Does the embed change
                        guildCount += 1
                        percentRaw = (guildCount/guildCountAll)*100
                        percent = round(percentRaw, 1)
                        percent0 = round(percentRaw, 0)
                        if (percent0 == 25) or (percent0 == 50) or (percent0 == 75):
                            embed = discord.Embed(title="Account is being banned...", color=discord.Color.green(),
                                description="%s%% complete! 👌" % percent)
                            embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                            #Causes lag in embed - embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/475498849696219141/ban.gif")
                            await embed_message.edit(embed=embed)
                    #Do this when done
                    #Send public ban notif in public ban list
                    pblchannel = bot.get_channel(int(os.getenv('pbanlist')))
                    pblembed = discord.Embed(title="Account banned", color=discord.Color.red(),
                        description="`%s` has been globally banned" % user.id)
                    pblembed.set_footer(text="%s has been globally banned" % user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                    pblembed.set_thumbnail(url=user.avatar_url)
                    await pblchannel.send(embed=pblembed)
                    #Send private ban notif in private moderator ban list
                    prvchannel = bot.get_channel(int(os.getenv('prvbanlist')))
                    prvembed = discord.Embed(title="Account banned", color=discord.Color.red(),
                        description="`%s` has been globally banned" % user.id)
                    prvembed.add_field(name="Moderator", value="%s (`%s`)" % (ctx.author.name, ctx.author.id), inline=True)
                    prvembed.add_field(name="Name when banned", value="%s" % user, inline=True)
                    prvembed.add_field(name="In server", value="%s (`%s`)" % (ctx.guild.name, ctx.guild.id), inline=True)
                    prvembed.add_field(name="In channel", value="%s (`%s`)" % (ctx.channel.name, ctx.channel.id), inline=True)
                    prvembed.set_footer(text="%s has been globally banned" % user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                    prvembed.set_thumbnail(url=user.avatar_url)
                    await prvchannel.send(embed=prvembed)
                    #send final embed, telling the ban was sucessful
                    embed = discord.Embed(title="Account banned", color=discord.Color.green(),
                        description="`%s` has been globally banned 👌" % user)
                    embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/475498849696219141/ban.gif")
                    await embed_message.edit(embed=embed)
            else:
                await ctx.send(embed=Embed(color=discord.Color.red(), description="You are not a Global Moderator! Shame!"))

        @bot.command(name="unban")
        async def _unban(ctx, user_id: int, *, reason = "No reason given"):
            """Unbans a user globally."""
            mods = list(map(int, os.getenv("mods").split()))
            if ctx.author.id in mods:
                #Sends main embed
                guildCount = 0
                guildCountAll = len(bot.guilds)
                user = await ctx.bot.fetch_user(user_id)
                embed = discord.Embed(title="Account is being unbanned...", color=discord.Color.green(),
                    description="0% complete! 👌")
                embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                #Causes lag in embed - embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/475498943178866689/unban.gif")
                embed_message = await ctx.send(embed=embed)
                #Sends a message in the botlog
                channel = bot.get_channel(int(os.getenv('botlog')))
                await channel.send(embed=Embed(color=discord.Color.green(), description="Moderator `%s` unbanned `%s` - (%s)" % (ctx.author.name, user.name, user.id)))
                print("Moderator `%s` unbanned `%s` - (%s)" % (ctx.author.name, user.name, user.id))
                for guild in bot.guilds:
                    try:
                        await guild.unban(user, reason=f"WatchDog - Global Unban")
                    except:
                        channel = bot.get_channel(int(os.getenv('botlogfail')))
                        await channel.send("**[Info]** Could not unban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, guild.name, guild.id))
                        print("**[Info]** Could not unban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, guild.name, guild.id))
                    guildCount += 1
                    percentRaw = (guildCount/guildCountAll)*100
                    percent = round(percentRaw, 1)
                    percent0 = round(percentRaw, 0)
                    if (percent0 == 25) or (percent0 == 50) or (percent0 == 75):
                        embed = discord.Embed(title="Account is being unbanned...", color=discord.Color.green(),
                            description="%s%% complete! 👌" % percent)
                        embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                        #Causes lag in embed - embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/475498943178866689/unban.gif")
                        await embed_message.edit(embed=embed)
                #do this when done
                #Send public unban notif in public ban list
                pblchannel = bot.get_channel(int(os.getenv('pbanlist')))
                pblembed = discord.Embed(title="Account unbanned", color=discord.Color.green(),
                    description="`%s` has been globally unbanned" % user.id)
                pblembed.set_footer(text="%s has been globally unbanned" % user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                pblembed.set_thumbnail(url=user.avatar_url)
                await pblchannel.send(embed=pblembed)
                #Send private ban notif in private moderator ban list
                prvchannel = bot.get_channel(int(os.getenv('prvbanlist')))
                prvembed = discord.Embed(title="Account unbanned", color=discord.Color.green(),
                    description="`%s` has been globally unbanned" % user.id)
                prvembed.add_field(name="Moderator", value="%s (`%s`)" % (ctx.author.name, ctx.author.id), inline=True)
                prvembed.add_field(name="Name when unbanned", value="%s" % user, inline=True)
                prvembed.add_field(name="In server", value="%s (`%s`)" % (ctx.guild.name, ctx.guild.id), inline=True)
                prvembed.add_field(name="In channel", value="%s (`%s`)" % (ctx.channel.name, ctx.channel.id), inline=True)
                prvembed.set_footer(text="%s has been globally unbanned" % user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                prvembed.set_thumbnail(url=user.avatar_url)
                await prvchannel.send(embed=prvembed)
                #edits final embed
                embed = discord.Embed(title="Account unbanned", color=discord.Color.green(),
                    description="`%s` has been globally unbanned 👌" % user)
                embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/475498943178866689/unban.gif")
                await embed_message.edit(embed=embed)
            else:
                await ctx.send(embed=Embed(color=discord.Color.red(), description="You are not a Global Moderator! Shame!"))

        @bot.command(name="mban", aliases=["multipleban"])
        async def _mban(ctx, *args, reason = "No reason given"):
            """Bans multiple users globally."""
            mods = list(map(int, os.getenv("mods").split()))
            if ctx.author.id in mods:
                banguild = bot.get_guild(int(os.getenv('banlistguild')))
                banguild_ban_list = await banguild.bans()
                argCountAllWithText = len(args)
                if argCountAllWithText == 0:
                    return
                else:
                    #Sends main embed
                    guild = []
                    argCount = 0
                    embed = discord.Embed(title="Accounts are being banned...", color=discord.Color.green(),
                        description="0% complete! 👌")
                    embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed_message = await ctx.send(embed=embed)
                    #ban on own guild
                    for arg in args:
                        try:
                            user = await ctx.bot.fetch_user(arg)
                        except:
                            print("User not fetched, removing from args: " + arg)
                            argslist = list(args)
                            argslist.remove(arg)
                            args = tuple(argslist)
                            continue
                        if user == ctx.bot.user:
                            await ctx.send(embed=Embed(color=discord.Color.red(), description="ID of bot was found in list!"))
                            argslist = list(args)
                            argslist.remove(arg)
                            args = tuple(argslist)
                            continue
                        elif user.id in mods:
                            await ctx.send(embed=Embed(color=discord.Color.red(), description="ID of Global Moderator was found in list!"))
                            argslist = list(args)
                            argslist.remove(arg)
                            args = tuple(argslist)
                            continue
                        else:
                            #Priorize banning all accounts on own guild
                            #tries to ban
                            try:
                                await ctx.guild.ban(user, reason=f"WatchDog - Global Ban")
                            except:
                                channel = bot.get_channel(int(os.getenv('botlogfail')))
                                await channel.send("**[Info]** Could not ban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, ctx.guild.name, ctx.guild.id))
                                print("**[Info]** Could not ban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, ctx.guild.name, ctx.guild.id))
                    #ban on all other guilds
                    for arg in args:
                        try:
                            user = await ctx.bot.fetch_user(arg)
                        except:
                            print("User not fetched, removing from args")
                            argslist = list(args)
                            argslist.remove(arg)
                            args = tuple(argslist)
                            continue

                        banned = False

                        for BanEntry in banguild_ban_list:
                            if BanEntry.user.id == user.id:
                                banCount += 1
                                print("User already banned, skipping - " + BanEntry.user.name)
                                ban_list_list = list(ban_list)
                                ban_list_list.remove(BanEntry)
                                ban_list = tuple(ban_list_list)
                                #Does the embed change
                                percentRaw = (argCount/argCountAllWithText)*100
                                percent = round(percentRaw, 1)
                                percent0 = round(percentRaw, 0)
                                if (percent0 == 25) or (percent0 == 50) or (percent0 == 75):
                                    embed = discord.Embed(title="Accounts are being banned...", color=discord.Color.green(),
                                        description="%s%% complete! 👌" % percent)
                                    embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                                    await embed_message.edit(embed=embed)
                                banned = True
                                break
                        
                        if banned == True:
                            continue
                        elif user == ctx.bot.user:
                            argslist = list(args)
                            argslist.remove(arg)
                            args = tuple(argslist)
                            continue
                        elif user.id in mods:
                            argslist = list(args)
                            argslist.remove(arg)
                            args = tuple(argslist)
                            continue
                        else:
                            #checks other guilds
                            for guild in bot.guilds:
                                #checks if own guild, if it is, skip
                                if guild != ctx.guild:
                                    #tries to ban
                                    try:
                                        await guild.ban(user, reason=f"WatchDog - Global Ban")
                                    except:
                                        channel = bot.get_channel(int(os.getenv('botlogfail')))
                                        await channel.send("**[Info]** Could not ban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, guild.name, guild.id))
                                        print("**[Info]** Could not ban the user `%s` (%s) in the guild `%s` (%s)" % (user.name, user.id, guild.name, guild.id))
                        #Does the embed change
                        argCount += 1
                        percentRaw = (argCount/argCountAllWithText)*100
                        percent = round(percentRaw, 1)
                        percent0 = round(percentRaw, 0)
                        if (percent0 == 25) or (percent0 == 50) or (percent0 == 75):
                            embed = discord.Embed(title="Accounts are being banned...", color=discord.Color.green(),
                                description="%s%% complete! 👌" % percent)
                            embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                            await embed_message.edit(embed=embed)
                        #Do this when done
                        #Sends a message in the botlog
                        channel = bot.get_channel(int(os.getenv('botlog')))
                        await channel.send(embed=Embed(color=discord.Color.red(), description="Moderator `%s` banned `%s` - (%s)" % (ctx.author.name, user.name, user.id)))
                        print("Moderator `%s` banned `%s` - (%s)" % (ctx.author.name, user.name, user.id))
                        #Send public ban notif in public ban list
                        pblchannel = bot.get_channel(int(os.getenv('pbanlist')))
                        pblembed = discord.Embed(title="Account banned", color=discord.Color.red(),
                            description="`%s` has been globally banned" % user.id)
                        pblembed.set_footer(text="%s has been globally banned" % user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                        pblembed.set_thumbnail(url=user.avatar_url)
                        await pblchannel.send(embed=pblembed)
                        #Send private ban notif in private moderator ban list
                        prvchannel = bot.get_channel(int(os.getenv('prvbanlist')))
                        prvembed = discord.Embed(title="Account banned", color=discord.Color.red(),
                            description="`%s` has been globally banned" % user.id)
                        prvembed.add_field(name="Moderator", value="%s (`%s`)" % (ctx.author.name, ctx.author.id), inline=True)
                        prvembed.add_field(name="Name when banned", value="%s" % user, inline=True)
                        prvembed.add_field(name="In server", value="%s (`%s`)" % (ctx.guild.name, ctx.guild.id), inline=True)
                        prvembed.add_field(name="In channel", value="%s (`%s`)" % (ctx.channel.name, ctx.channel.id), inline=True)
                        prvembed.set_footer(text="%s has been globally banned" % user, icon_url="https://cdn.discordapp.com/attachments/456229881064325131/489102109363666954/366902409508814848.png")
                        prvembed.set_thumbnail(url=user.avatar_url)
                        await prvchannel.send(embed=prvembed)
                    #send final embed, telling the ban was sucessful
                    embed = discord.Embed(title="Accounts banned", color=discord.Color.green(),
                        description="%s accounts have been globally banned 👌" % len(argslist))
                    embed.set_footer(text="%s - Global WatchDog Moderator" % ctx.author.name, icon_url=ctx.author.avatar_url)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/456229881064325131/475498849696219141/ban.gif")
                    await embed_message.edit(embed=embed)
            else:
                await ctx.send(embed=Embed(color=discord.Color.red(), description="You are not a Global Moderator! Shame!"))

def setup(bot):
    bot.add_cog(Moderation(bot))
