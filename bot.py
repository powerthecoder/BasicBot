import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import json
import os
import sys

client = commands.Bot(command_prefix="$")




##      EVENTS      ##

@client.event
async def on_ready():
    print(" ")
    print("-------------------------------")
    print("Bot Online")
    print('Logged In As: ',client.user.name)
    print('ID: ',client.user.id)
    print('Discord Version: ',discord.__version__)
    print('-------------------------------')
    print(" ")
    print(" ")

client.remove_command('help')

@client.event
async def on_member_join(member):
    mod_logs = client.get_channel(757145970159910982)
    dev_logs = client.get_channel(665553350355582986)
    print(f"{member} Joined Server")
    role = discord.utils.get(member.guild.roles, id=757145053465673820)
    await Member.add_roles(member, role)
    await mod_logs.send(f"**{member}** Joined The Server")
    await dev_logs.send(f"**{member}** Joined the Server")

@client.event
async def on_member_remove(member):
    mod_logs = client.get_channel(757145970159910982)
    dev_logs = client.get_channel(665553350355582986)
    print(f"{member} Left Server")
    await mod_logs.send(f"**{member}** left the Server")
    await dev_logs.send(f"**{member}** left the Server")


@client.event
async def on_message_delete(message):
    mod_logs = client.get_channel(757145970159910982)
    dev_logs = client.get_channel(665553350355582986)
    embed=discord.Embed(title="Message Delted", description=f"**Message:** {message.content} \n**Author:** {message.author.mention} \n**Channel:** <#{message.channel.id}>")
    await mod_logs.send(embed=embed)
    await dev_logs.send(embed=embed)
    print("Someone delted a message")


##      Commands        ##

@client.commands()
async def help(ctx):
    embed=discord.Embed(title="Help Menu", description="Prefix `$`")
    embed.add_field(name="`$help`", value="Get Help Menu")
    embed.add_field(name="`$mutevc <mins>`", value="To mute a enitre Voice Channel that you are in. `<mins>` is optional, but this will unmute the voice channel after the amount of mins have passed")
    embed.add_field(name="`$unmutevc`", value="To unmute a Voice Channel that you are in")
    embed.add_field(name="`$warn @user <reason>`", value="To give a warning to someone")


@client.command(pass_context=True)
@has_permissions(manage_messages=True)
async def mutevc(ctx, *,args=None):
    if (args == None):
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, speak=False, use_voice_activation=False)
        embed=discord.Embed(title="Voice Muted", description=f"**Channel Muted:** {channel} \n**Muted By:** {ctx.message.author} \n**Duration:** None")
        await ctx.send(embed=embed)
        mod_logs = client.get_channel(757145970159910982)
        dev_logs = client.get_channel(665553350355582986)
        await mod_logs.send(embed=embed)
        await dev_logs.send(embed=embed)
    else:
        channel = ctx.author.voice.channel
        await channel.set_permissions(ctx.guild.default_role, speak=False, use_voice_activation=False)
        embed=discord.Embed(title="Voice Muted", description=f"**Channel Muted:** {channel} \n**Muted By:** {ctx.message.author} \n**Duration:** {args}")
        await ctx.send(embed=embed)
        mod_logs = client.get_channel(757145970159910982)
        dev_logs = client.get_channel(665553350355582986)
        await mod_logs.send(embed=embed)
        await dev_logs.send(embed=embed)
        try:
            mins = int(args) * 60
            await asyncio.sleep(mins)
        except Exception as e:
            await ctx.send("Please use a number. Number is counted as mins")
        await channel.set_permissions(ctx.guild.default_role, speak=True, use_voice_activation=True)
        msg = ctx.send(f"**{channel}** Unmuted")
        await asyncio.sleep(10)
        await msg.delete()


@client.command(pass_context=True)
@has_permissions(manage_messages=True)
async def unmutevc(ctx):
    channel = ctx.author.voice.channel
    await channel.set_permissions(ctx.guild.default_role, speak=True, use_voice_activation=True)
    embed=discord.Embed(title="Voice Unmuted", description=f"**Channel Unmuted:** {channel} \n**Muted By:** {ctx.message.author}")
    await ctx.send(embed=embed)
    mod_logs = client.get_channel(757145970159910982)
    dev_logs = client.get_channel(665553350355582986)
    await mod_logs.send(embed=embed)
    await dev_logs.send(embed=embed)


@client.command(pass_context=True)
@has_permissions(manage_messages=True)
async def warn(ctx, user_name:discord.Member, *,args=None):
    mod_logs = client.get_channel(757145970159910982)
    dev_logs = client.get_channel(665553350355582986)
    author = ctx.message.author
    userid = user_name.id
    if (args == None):
        msg = await ctx.send("Please add a reason")
        await asyncio.sleep(5)
        await msg.delete()
    else:
        with open("/home/leo/ftp/Discord/BasicBot/warnings.json", "r") as f:
            users = json.load(f)
        target = user_name.id
        if not f'{target}' in users:
            users[f'{target}'] = {}
            users[f'{target}'] = 1
            embed=discord.Embed(title="Warning", description=f"**User Warnned:** {user_name} \n**Total Warnings:** 1 \n**Warned By:** {author} \n**Reason:** {args}")
            await ctx.send(f'<@{userid}>')
            await ctx.send(embed=embed)
            await mod_logs.send(f'<@{userid}>')
            await dev_logs.send(f'<@{userid}>')
            await dev_logs.send(embed=embed)
            await mod_logs.send(embed=embed)
        else:
            warnam = int(users[f'{target}'])
            warnam += 1
            users[f'{target}'] = warnam
            embed=discord.Embed(title="Warning", description=f"**User Warnned:** {user_name} \n**Total Warnings:** {warnam} \n**Warned By:** {author} \n**Reason:** {args}")
            await ctx.send(f'<@{userid}>')
            await ctx.send(embed=embed)
            await mod_logs.send(f'<@{userid}>')
            await dev_logs.send(f'<@{userid}>')
            await dev_logs.send(embed=embed)
            await mod_logs.send(embed=embed)
        with open('/home/leo/ftp/Discord/BasicBot/warnings.json', 'w') as f:
            json.dump(users, f)

client.run("")
    



