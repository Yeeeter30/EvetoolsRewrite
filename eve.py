# must have "py-cord" installed
# do pip install py-cord

# Imports
import discord
from discord.ext import commands
import os
import datetime
import asyncio
from itertools import cycle
import random

# Intents and bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Start time
start_time = datetime.datetime.now(datetime.UTC)

# Statuses
statuses = [
    discord.Activity(type=discord.ActivityType.listening, name='Made By YieldingRS!'),
    discord.Activity(type=discord.ActivityType.listening, name='Coded in Python!'),
    discord.Activity(type=discord.ActivityType.listening, name='Invented On 6/21/24'),
    discord.Activity(type=discord.ActivityType.listening, name='EveTools is back officially.'),
    discord.Activity(type=discord.ActivityType.listening, name='Version 1.8')
    ]

# On ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user} w rewrite")
    await bot.change_presence(activity=statuses[0])
    status_cycle = cycle(statuses)
    async def change_status():
        while True:
            await asyncio.sleep(12)
            await bot.change_presence(activity=next(status_cycle))
    bot.loop.create_task(change_status())

# Remove help
bot.remove_command("help")

# Help (say commands)
@bot.slash_command(name="help", description="Help and show commands.")
async def help1(ctx):
    embed=discord.Embed(title="Help", description="Commands")
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    embed.set_author(name=f"{ctx.author.name}", icon_url=avatar_url)
    embed.add_field(name="Commands", value="""
/help
/repeat
/kick
/ban
/ping
/coinflip
/randomnum
/createrole
/deleterole
/uptime
/shutdown (OWNER ONLY)
    """, inline=False)
    embed.set_footer(text="Made by YieldingRS | EVETOOLS")
    await ctx.respond(embed=embed)

# Repeat the word you say
@bot.slash_command(name="repeat", description="Repeat the word you said.")
@commands.is_owner()
async def repeat(ctx, *, text):
    await ctx.respond(text)
    
# Repeat error
@repeat.error
async def repeaterr(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond("You are not the owner")
    
# Kick a user
@bot.slash_command(name="kick", description="Kick a user.")
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Option(discord.Member, "Select a User"), reason: discord.Option(str, "Send a reason")):
    await ctx.respond(f"Kicked {user.name}")
    await user.send(f"you have been kicked from {ctx.guild.name} for {reason}")
    await user.kick(reason=reason)
    
# Kick error
@kick.error
async def kickerr(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("No permissions.")
    
# Ban a user
@bot.slash_command(name="ban", description="Bans a user.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Option(discord.Member, "Select a User"), reason: discord.Option(str, "Send a reason")):
    await ctx.respond(f"Banned {user.name}")
    await user.send(f"you have been banned from {ctx.guild.name} for {reason}")
    await user.ban(reason=reason)

# Ban error
@ban.error
async def banerr(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("No permissions.")

# Temp Ban
@bot.slash_command(name="tempban", description="Temporary ban a user.")
async def tempban(ctx, user: discord.Option(discord.Member, "Select a user"), reason: discord.Option(str, "Send a reason"), length: discord.Option(int, "Length")):
    await ctx.respond(f"Temp Banned {user.name}")
    await user.send(f"you have been Temporarily banned from {ctx.guild.name} for {reason}")
    await user.ban(reason=reason, delete_message_days=7)
    await asyncio.sleep(length)
    try:
        await ctx.guild.unban(user)
    except:
        pass

# Temp ban error
@tempban.error
async def temperr(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("No permissions.")

# Ping
@bot.slash_command(name="ping", description="Show the bots ping.")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.respond(f"Youre ping is {latency}ms")
    
# Shutdown
@bot.slash_command(name="shutdown", description="Shutdown the bot.")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.respond("shutting down the bot")
    print(f"{ctx.author.name} has shut down the bot")
    await bot.close()

# Shutdown error
@shutdown.error
async def shutdownerr(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond("You are not the owner.")

# Uptime
@bot.slash_command(name="uptime", description="Show the bots uptime.")
async def uptime(ctx):
    now = datetime.datetime.now(datetime.UTC)
    delta = now - start_time
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptimetotal = f"{days}d {hours}h {minutes}m {seconds}s"
    await ctx.respond(f"Uptime is: {uptimetotal}")

# Flip a coin
@bot.slash_command(name="coinflip", description="Flip a coin.")
async def coinflip(ctx):
    result = random.choice(["Heads", "Tails"])
    await ctx.respond(result)

# Pick a random number
@bot.slash_command(name="randomnum", description="Pick a random number.")
async def randomnum(ctx, *, min: int, max: int):
    number = random.randint(min, max)
    await ctx.respond(f"Youre number is {number}")

# Create a role 
@bot.slash_command(name="createrole", description="Create a role.")
@commands.has_permissions(manage_roles=True)
async def createrole(ctx, rolename: str):
    guild = ctx.guild
    await guild.create_role(name=rolename)
    await ctx.respond(f"Created the role {rolename}")

# Createrole error
@createrole.error
async def createerr(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("No permissions.")

# Delete a role
@bot.slash_command(name="deleterole", description="Delete a role.")
@commands.has_permissions(manage_roles=True)
async def deleterole(ctx, rolename: discord.Option(discord.Role, "select a role")):
    await rolename.delete()
    await ctx.respond(f"Deleted the role {rolename}")
   
# Deleterole error 
@deleterole.error
async def deleteerr(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("No permissions.")

# members
@bot.slash_command(name="members", description="Get all server members")
async def members(ctx):
    await ctx.respond(f"We have {len(ctx.guild.members)} members")

# Run the bot
bot.run("token here")