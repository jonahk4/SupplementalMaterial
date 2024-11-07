import os
import asyncio
import nextcord
from system.keep_alive import keep_alive
from nextcord.ext import commands
import datetime
from replit import db
from re import fullmatch
intents = nextcord.Intents.default()
intents.members = True
intents.guild_reactions = True
intents.message_content = True
intents.guilds = True
import system
import math
from system import autoresponse
from system import helpcommand
import sys
import random
from dadjokes import Dadjoke
client = commands.Bot(command_prefix = "*", case_insensitive = True, intents = intents, strip_after_prefix = True)
from replit import db

@client.event 
async def on_ready():
  print("Use CTRL+C to stop startup.")
  print("Conducting system checks. Standby...")
  await asyncio.sleep(3)
  db['startuptime'] = str(datetime.datetime.utcnow())
  print("Checking version number...")
  await asyncio.sleep(3)
  os.system('clear')
  keep_alive()
  print("All systems operational.")
  counter = 0
  while counter < 300:
    print("Runtime in progress.")
    await asyncio.sleep(60)
    counter += 1
  os.system("kill 1")
  os.system('python3 main.py')


@client.listen('on_message')
async def respondMessage(message):
  if message.author == client.user:
    return
  if (str(message.guild.id) in db and 'status' in db[str(message.guild.id)]) and db[str(message.guild.id)]['status'] == "on":
    if message.content.lower() in db[str(message.guild.id)]['autoreplies']:
      reply = db[str(message.guild.id)]['autoreplies'][message.content.lower()]
      await message.channel.send(reply)
      return
    else:
      return
  else:
    return


  
@client.event
async def on_member_join(member):
  if str(member.guild.id) in db and 'welcomeMessage' in db[str(member.guild.id)]:
    welcomeMessage = str(db[str(member.guild.id)]['welcomeMessage'])
    channel = nextcord.utils.get(member.guild.text_channels, id = int(db[str(member.guild.id)]['welcomeMessageChannel']))
    await channel.send(welcomeMessage)
  else:
    return

@client.event
async def on_raw_reaction_add(payload):
  if str(payload.guild_id) in db and "role" in db[str(payload.guild_id)]:
    if str(payload.message_id) == db[str(payload.guild_id)]['reactionMessage'] and payload.emoji.name == db[str(payload.guild_id)]["roleEmoji"]:
      guild = client.get_guild(payload.guild_id)
      role = nextcord.utils.get(guild.roles, id = int(db[str(payload.guild_id)]['role']))
      await payload.member.add_roles(role)
    else:
      return
  else:
    return

@client.event
async def on_guild_join(guild):
  embed = nextcord.Embed(
    title = "Hi there!",
    description = f"Thanks for inviting Polaris to your server. All commands can be invoked using the prefix `/`.\nA list of commands can also be found here: {os.environ['website_link']}.",
    colour = 0x10E6F1
  )
  embed.set_footer(text = f"Server ID: {guild.id} | {datetime.datetime.utcnow()} UTC")
  channel = guild.text_channels[0]
  if channel != guild.rules_channel:
    await channel.send(embed = embed)
    return
  else:
    channel = guild.text_channels[1]
    await channel.send(embed = embed)
    return


  
@client.event
async def on_command_error(ctx, err):
  if isinstance(err, commands.CommandNotFound):
    if "*" not in str(err) and ctx.message.content.count("*") <= 1:
      embed = nextcord.Embed(
        title = "Polaris has switched to Slash Commands.",
        description = "Type \"/\" to view a list of slash commands for Polaris. If no commands appear, please kick and reinvite the bot with this link: https://polarisbot.com/invite"
      )
      
      embed.set_footer(text = f"Server Id: {ctx.guild.id} | {datetime.datetime.utcnow()} UTC")
      
      await ctx.send(embed = embed)
    else:
      return
  else:
    return


@client.event
async def on_application_command_error(interaction, exception):
  await interaction.send("An error occured while using this command. Please try again later. If this issue persists, please contact support here: https://support.polarisbot.com", ephemeral = True)
  return

    



@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def viewkeyvalue(ctx, user):
  if ctx.author.id == int(os.environ['user1']) or ctx.author.id == int(os.environ['user2']):
   if str(user) in db:
     await ctx.send(f"{db[user]}")
  else:
    return

@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def shutdown(ctx):
  if ctx.author.id == int(os.environ['user1']) or ctx.author.id == int(os.environ['user2']):
    embed = nextcord.Embed(
      title = ":warning: Attention!",
      description = "Continuing with this command will shut the bot down. **The bot will not come back online without a manual restart**. Are you sure you want to proceed?"
    )
    message = await ctx.send(embed = embed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    def check(reaction, user):
      if user == ctx.author and reaction.emoji == "✅":
        raise TypeError
      elif user == ctx.author and reaction.emoji != "✅":
        raise ValueError
      else:
        pass
    try:
      await client.wait_for('reaction_add', timeout = 15.0, check = check)
    except TypeError:
      await ctx.send("Please wait. Bot is shutting down.")
      file = open('system/helpcommand.py', 'a')
      file.write('\nThe shutdown command has been used. Please delete this line and restart the bot when ready.')
      file.close()
      await client.close()
      sys.exit()
    except ValueError:
      await ctx.send("Action canceled.")
      return
    except asyncio.TimeoutError:
      await ctx.send("Action canceled.")
      return
  else:
    return

@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def setversion(ctx, v):
  if (ctx.author.id) == int(os.environ['user1']) or (ctx.author.id) == int(os.environ['user2']):
    db['version'] = v
    await ctx.send(f"Version number updated to v{v}")
  else:
    pass
    
@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def viewlaststarttime(ctx):
  if (ctx.author.id) == int(os.environ['user1']) or (ctx.author.id) == int(os.environ['user2']):
    await ctx.send(f"Last start time: {db['startuptime']} UTC")
    return
  else:
    return
@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def addbotalert(ctx, message):
  if (ctx.author.id) == int(os.environ['user1']) or (ctx.author.id) == int(os.environ['user2']):
    notAllowedCharacters = ["*"]
    for c in message:
      if c in notAllowedCharacters:
        await ctx.send("Error: Character detected in message that is bad for formatting. Ex: `*`")
        return
      else:
        pass
    if len(message) <= 300:
      db['botalerts'] = f"{message}"
      await ctx.send("Alert added. This will be displayed when users use the command `*getbotinfo`. Remove this alert with `*resetbotalerts`")
      return
    else:
      await ctx.send("Error: Alert is too long.")
  else:
    return

@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def resetbotalerts(ctx):
  db['botalerts'] = "Operational"
  await ctx.send("Alert removed.")

@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def removeUserFromDatabase(ctx, user):
  if (ctx.author.id) == int(os.environ['user1']) or (ctx.author.id) == int(os.environ['user2']):
    if str(user) in db:
      del db[str(user)]
      await ctx.send("User removed from database.")
      return
    else:
      await ctx.send("User not found in database.")
      return
  else:
    return
  




@client.command(hidden = True)
@commands.has_permissions(administrator = True)
async def removeServerFromDatabase(ctx, server_id):
  try:
    if ctx.author.id == int(os.environ['user1']) or ctx.author.id == int(os.environ['user2']):
      del db[str(server_id)]
      await ctx.send(f"`{server_id}` removed from database.")
      return
    else:
      return
  except ValueError:
    await ctx.send("Server not found in database.")





@client.slash_command(name = "dataset", description = "Commands related to datasets.")
async def dataset(interaction: nextcord.Interaction):
  pass

@dataset.subcommand(name = "range", description = "Get the range of a given data set.")
async def getRange(interaction: nextcord.Interaction, dataset:str = nextcord.SlashOption(description = "The list of values to find the range of. (Seperate values by commas please)")):
  """Finds the range of a dataset with given values."""
  if fullmatch("[-,.0123456789 ]*", str(dataset)):
    try:
      calculationList = []
      valueList = dataset.split(",")
      for value in valueList:
        calculationList.append(float(value))
    
      range = max(calculationList) - min(calculationList)
      await interaction.send(f"Range of datatset: {range}")
    except:
      await interaction.send("An error occured.", ephemeral = True)
  else:
    await interaction.send("`Format Error: Could not interpret values given.`", ephemeral = True)

@dataset.subcommand(name = "average", description = "Get the average of a given data set.")
async def getAverage(interaction: nextcord.Interaction, dataset:str = nextcord.SlashOption(description = "The list of values to find the average of. (Seperate values by commas please)")):
  """Finds the average of a data set with given values."""
  if fullmatch("[-,.0123456789 ]*", str(dataset)):
    try:
      calculationList = []
      valueList = dataset.split(",")
      for value in valueList:
        calculationList.append(float(value))
    
      average = sum(i for i in calculationList) / len(calculationList)
      await interaction.send(f"Average of datatset: {average}")
    except:
      await interaction.send("An error occured.", ephemeral = True)
  else:
    await interaction.send("`Format Error: Could not interpret values given.`", ephemeral = True)

@dataset.subcommand(name = "standard_deviation", description = "Get the standard deviation of a given data set.")
async def getStandardDeviation(interaction: nextcord.Interaction, dataset:str = nextcord.SlashOption(description = "The list of values to find the standard deviation of. (Seperate values by commas please)")):
  """Finds the standard deviation of a given dataset."""
  if fullmatch("[-,.0123456789 ]*", str(dataset)):
    try:
      calculationList = []
      valueList = dataset.split(",")
      for value in valueList:
        calculationList.append(float(value))
    
      average = sum(i for i in calculationList)/len(calculationList)
      topNumber = 0
      for value in calculationList:
        difference_squared = (value - average) ** 2
        topNumber += difference_squared
      standard_deviation = (topNumber / len(calculationList)) ** (1/2)
        
      await interaction.send(f"Standard Deviation of datatset: {standard_deviation}")
    except:
      await interaction.send("An error occured.", ephemeral = True)
  else:
    await interaction.send("`Format Error: Could not interpret values given.`", ephemeral = True)

@dataset.subcommand(name = "countitems", description = "Get the number of values in the specified list.")
async def countItems(interaction: nextcord.Interaction, dataset:str = nextcord.SlashOption(description = "The list to count the number of values. (Seperate values by commas please)")):
  """Returns the number of items in a list."""
  try:
    itemlist = dataset.split(",")
    lenCounter = 0
    for i in itemlist:
      lenCounter += 1
    await interaction.send(f"Number of items in list specified: {lenCounter}")
    return
  except:
    await interaction.send("Number of items in list specified: 1")
    return
    
      
  else:
    await interaction.send("`Format Error: Could not interpret values given.`", ephemeral = True)





    
client.remove_command('help')
  

@client.slash_command()
async def help(interaction: nextcord.Interaction, command:str = nextcord.SlashOption(description = "Name of command to search.", required = False, default = None)):
  """Help command for bot."""
  if command == None:
    embed = helpcommand.HelpCommand(helpcommand.commandlist).present()
    await interaction.send(embed = embed)
  else:
    embed = helpcommand.findcommand(command, helpcommand.commandlist)
    await interaction.send(embed = embed)
      
@client.slash_command()
async def createticket(interaction: nextcord.Interaction):
  """Create a ticket."""
  server_id = str(interaction.guild.id)
  if (server_id in db and 'ticketStatus' in db[server_id]) and (nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory'])) and db[server_id]['ticketStatus'] == "on"):
    await interaction.send("Please wait...")
    category = nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory']))
    topic = db[server_id]['ticketDescription']
    message = db[server_id]['ticketMessage']
    new_channel = await interaction.guild.create_text_channel(
      name = str(interaction.user),
      position = 0,
      topic = topic,
      category = category,
      slowmode_delay = 0,
      nsfw = False,
      reason = str("Support was needed for " + str(interaction.user)))
    
    await new_channel.set_permissions(client.user, view_channel = True, send_messages = True)
    for role in interaction.guild.roles:
      if role.permissions.manage_channels == True:
        await new_channel.set_permissions(role, send_messages = True, view_channel = True)
      else:
        await new_channel.set_permissions(role, view_channel = False)
    await new_channel.set_permissions(interaction.user, send_messages = True, view_channel = True)
    await new_channel.send(interaction.user.mention)
    await new_channel.send(message)
    await interaction.channel.send("Ticket created.")
    return
  else:
    await interaction.send("Please setup the ticket system using the '/setup` command.'", ephemeral = True)
    return
      
@client.slash_command()
async def invite(interaction: nextcord.Interaction):
  """Link to invite Polaris to a server."""
  await interaction.send(f"Invite link for bot: {str(os.environ['invite_link'])}", ephemeral = True)


@client.slash_command()
async def getbotinfo(interaction: nextcord.Interaction):
  """Returns information about the bot."""
  timetoformat = db['startuptime']
  timestringformat = timetoformat.split("-")
  year = timestringformat[0]
  month = timestringformat[1]
  othertimestring = timestringformat[2].split(" ")
  day = othertimestring[0]
  timestring = othertimestring[1].split(":")
  hour = timestring[0]
  minute = timestring[1]
  t1 = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
  t2 = datetime.datetime.utcnow()
  tdelta = t2 - t1
  seconds = tdelta.total_seconds()
  days = math.floor(seconds / 86400)
  s1 = seconds - (days * 86400)
  hours = math.floor(s1 / 3600)
  s2 = s1 - (hours * 3600)
  minutes = round(s2 / 60)
  embed = nextcord.Embed(
    description = f"Current version: v{db['version']}\nApproximate time since last restart: {days} days {hours} hours {minutes} minute(s)"
  )
  embed.set_author(name = "Polaris Information", icon_url = "https://cdn.discordapp.com/attachments/998996177070608426/999074269906616380/logo.png")
  embed.set_footer(text = f"Command Status: {db['botalerts']}")
  await interaction.send(embed = embed)


client.load_extension('frivolity.frivolity')
client.load_extension('moderation.moderation')
client.load_extension('reactionrole.reactionrole')
client.load_extension("settings.settings")
client.load_extension('utilities.utilities')
client.load_extension('autoresponder.autoresponse')
client.load_extension('tickets.tickets')
client.load_extension('welcome.welcome')
client.load_extension('economy.economy')
client.load_extension('tictactoe.tictactoe')
client.load_extension('study.study')
try:
  client.run(os.environ['TOKEN'])
except:
  os.system('kill 1')
  os.system('python3 main.py')
  client.run(os.environ['TOKEN'])

  
