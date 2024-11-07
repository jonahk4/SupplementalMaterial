import nextcord
from nextcord.ext import commands
import asyncio
from replit import db
import datetime
import datetime

class Moderation(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.__member = None
    self.__reason = None
    self.__amount = None
    self.__slowmode_delay = None
    self.__reason = None
    self.__member = None
    self.__reason = None
    self.__title = None
    self.__description = None
    self.__colour = None
    self.__category = None
    self.__guess = None
    self.__footer = None
    self.__number = None
    self.__duration = None
  @nextcord.slash_command(default_member_permissions = 268435456)
  async def moderation(self, interaction: nextcord.Interaction):
    pass
  @moderation.subcommand()
  async def mute(self, interaction: nextcord.Interaction, member:nextcord.Member = nextcord.SlashOption(description = "Member to mute"), timeperiod: int = nextcord.SlashOption(description = "Time period of mute"), reason:str = nextcord.SlashOption(description = "Reason for mute.", required = False, default="N/A")):
    """Mute(timeout) a member for a specified period of time."""
    self.__member = member
    self.__reason = reason
    commandTime = datetime.timedelta(seconds = int(timeperiod))
    await member.timeout(timeout = commandTime, reason = reason)
    await interaction.send(f"{member} has been muted for {timeperiod} seconds.")
 
  @moderation.subcommand()
  async def unmute(self, interaction: nextcord.Interaction, member:nextcord.Member = nextcord.SlashOption(description = "Member to unmute.")):
    self.__member = member
    """Unmutes a given member. (Gets rid of timeout)"""
    await member.timeout(timeout = None)
    await interaction.send(f"{member} has been unmuted.")
    
 
  @moderation.subcommand()
  async def clear(self, interaction: nextcord.Interaction, amount: int = nextcord.SlashOption(description = "Amount of messages to clear.")):
    """Clears a given amount of messages in the channel the command is invoked in."""
    self.__amount = amount
    if amount > 0 and amount <= 500:
      await interaction.send("Please wait...")
      await asyncio.sleep(2)
      message_count = await interaction.channel.purge(limit = amount + 1)
      await interaction.channel.send(f"{len(message_count)} messages were deleted in this channel. This includes the message in which the command was used.", delete_after = 5)
     
    elif amount <= 0:
      embed = nextcord.Embed(
        title = "",
        description = "Please choose an amount greater than zero.",
        colour = 0x10E6F1
      )
      await interaction.send(embed = embed, ephemeral = True)
    elif amount > 500:
      embed = nextcord.Embed(
        title = "",
        description = "Error: Maximum of `500` messages can be cleared at at time.",
        colour = 0x10E6F1
      )
      await interaction.send(embed = embed, ephemeral = True)
  
      
 
  @moderation.subcommand()
  async def setslowmode(self, interaction: nextcord.Interaction, slowmode_delay:int = nextcord.SlashOption(description = "Delay time", default=0, required = False)):
    """Sets a given slowmode delay for the channel the command is invoked in."""
    self.__slowmode_delay = slowmode_delay
    await interaction.channel.edit(slowmode_delay = slowmode_delay)
    await interaction.send(f"Channel cooldown has been set to {slowmode_delay} seconds.", delete_after = 2)
    
 
  
  @moderation.subcommand()
  async def ban(self, interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(description = "Member to ban."), reason:str = nextcord.SlashOption(description = "Reason for ban.")):
    """Bans a given member from the server."""
    self.__member = member
    self.__reason = reason
    await interaction.send("Please wait...")
    embed = nextcord.Embed(
      title = "Warning.",
      description = f"Are you sure you want to proceed with this action? This will ban {member} from your server.",
      colour = 0x10E6F1
    )
    message = await interaction.channel.send(embed = embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    def check(reaction, user):
      if user == interaction.user and reaction.emoji == "✅":
        return user == interaction.user and reaction.emoji == "✅"
      elif user == interaction.user and reaction.emoji == "❌":
        raise ValueError
    try:
      reaction, user = await self.client.wait_for('reaction_add', timeout = 10.0, check = check)
      await member.ban(reason = reason)
      await interaction.channel.send(f"{member} has been banned. Reason will show up in audit log.")
    except ValueError:
      await interaction.channel.send("Action canceled.")
    except asyncio.TimeoutError:
      await interaction.channel.send("Action canceled.")
 
  
  @moderation.subcommand()
  async def kick(self, interaction: nextcord.Interaction, member : nextcord.Member = nextcord.SlashOption(description  = "Member to kick from server."), reason: str = nextcord.SlashOption(description = "Reason for kicking member from server.")):
    """Kicks a given member from the server."""
    self.__member = member
    self.__reason = reason
    await interaction.send("Please wait...")
    embed = nextcord.Embed(
      title = "Warning.",
      description = f"Are you sure you want to proceed with this action? This will kick {member} from your server.",
      colour = 0x10E6F1
    )
    message = await interaction.channel.send(embed = embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    def check(reaction, user):
      if user == interaction.user and reaction.emoji == "✅":
        return user == interaction.user and reaction.emoji == "✅"
      elif user == interaction.user and reaction.emoji == "❌":
        raise ValueError
    try:
      reaction, user = await self.client.wait_for('reaction_add', timeout = 10.0, check = check)
      await member.kick(reason = reason)
      await interaction.channel.send(f"{member} has been kicked from this server. Reason will show up in audit log.")
    except ValueError:
      await interaction.channel.send("Action canceled.")
    except asyncio.TimeoutError:
      await interaction.channel.send("Action canceled.")
  
  
  @moderation.subcommand()
  async def createembed(self, interaction: nextcord.Interaction, title:str = nextcord.SlashOption(description = "Title of embed message", required = False, default = ""), description:str = nextcord.SlashOption(description = "Description for embed message", required = False, default = "No description provided."), colour:int = nextcord.SlashOption(description = "Color for embed message", required = False, default = 0x10E6f1), image_url: str = nextcord.SlashOption(description = "Url to image for embed message.", required = False, default = ""), author:str = nextcord.SlashOption(description = "Set author of embed message", required = False, default = ""), footer:str = nextcord.SlashOption(description = "Footer for embed message.", required = False, default = ""), channel: nextcord.abc.GuildChannel = nextcord.SlashOption(description = "Channel to send the embed message in.", required = False, channel_types = [nextcord.ChannelType.text])):
    """Creates an embedded message."""
    
    embed = nextcord.Embed(
      title = title,
      description = description,
      colour = nextcord.Colour(colour),
    )
    await interaction.send("Please wait...")
    embed.set_footer(text = footer)
    embed.set_image(url = image_url)
    embed.set_author(name = author)
    if channel == None:
      await interaction.channel.send(embed = embed)
    else:
      await channel.send(embed = embed)
    await interaction.channel.send("Embed sent.")
 
    
    


  @moderation.subcommand()
  async def addwarning(self, interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(description = "Member to add warning for."), reason:str = nextcord.SlashOption(description = "Reason for adding warning.", required = False)):
    if member.top_role.permissions.manage_roles == False and member.guild_permissions.manage_roles == False:
      server_id = str(interaction.guild.id)
      if server_id in db and 'warnings' not in db[server_id]:
        db[server_id]['warnings'] = {}
        db[server_id]['warnings'][str(member.id)] = 1
        await interaction.send(f"{member} has been warned.")
        return
      elif server_id in db and 'warnings' in db[server_id]:
        if str(member.id) in db[server_id]['warnings']:
          db[server_id]['warnings'][str(member.id)] += 1
          await interaction.send(f"{member} has been warned.")
          return
        else:
          db[server_id]['warnings'][str(member.id)] = 1
          await interaction.send(f"{member} has been warned.")
          return
      elif server_id not in db:
        db[server_id] = {}
        db[server_id]['warnings'] = {}
        db[server_id]['warnings'][str(member.id)] = 1
        await interaction.send(f"{member} has been warned.")
    else:
      await interaction.send("This is not allowed.", ephemeral = True)
 

  @moderation.subcommand()
  async def viewwarnings(self, interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(description = "Member to view warnings for.")):
    server_id = str(interaction.guild.id)
    if (server_id in db and 'warnings' in db[server_id]) and str(member.id) in db[server_id]['warnings']:
      await interaction.send(f"{member} has {db[server_id]['warnings'][str(member.id)]} warning(s).")
    else:
      await interaction.send("This member does not have any warnings.")

  

  @moderation.subcommand()
  async def removewarnings(self, interaction: nextcord.Interaction, member: nextcord.Member = nextcord.SlashOption(description = "Member to remove warnings for."), number: int = nextcord.SlashOption(description = "Number of warnings to remove.")):
    server_id = str(interaction.guild.id)
    try:
      number = int(number)
      if (server_id in db and 'warnings' in db[server_id] and str(member.id) in db[server_id]['warnings']):
        if number <= db[server_id]['warnings'][str(member.id)]:
          db[server_id]['warnings'][str(member.id)] -= number
          await interaction.send(f"{number} warning(s) removed for {member}")
        if db[server_id]['warnings'][str(member.id)] == 0:
          del db[server_id]['warnings'][str(member.id)]
          return
        else:
          await interaction.send("Invalid number specified. Greater than number of warnings member has.", ephemeral = True)
      else:
        await interaction.send("This member does not have any warnings.", ephemeral = True)
    except ValueError:
      await interaction.send("Invalid number specified.", ephemeral = True)
 




def setup(client):
	client.add_cog(Moderation(client))