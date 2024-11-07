import nextcord
from nextcord.ext import commands
from replit import db
import asyncio

#reactionMessage, role, roleEmoji ---> Database values for each server.

class ReactionRole(commands.Cog, name = "Reaction Roles"):
  def __init__(self, client):
    self.client = client

  @nextcord.slash_command(default_member_permissions = 268435456)
  async def reactionrole(self, interaction: nextcord.Interaction):
    pass
  @reactionrole.subcommand()
  async def add(self, interaction: nextcord.Interaction, message: str = nextcord.SlashOption(description = "Message user will react to"), channel: nextcord.abc.GuildChannel = nextcord.SlashOption(description = "Channel message should be sent in", channel_types = [nextcord.ChannelType.text]), role: nextcord.Role = nextcord.SlashOption(description = "Role that should be given"), reaction: str = nextcord.SlashOption(description = "Reaction to message.")):
    """Add reaction role."""
    messageSendChannel = nextcord.utils.get(interaction.guild.text_channels, name = str(channel))
    messageSent = await messageSendChannel.send(message)
    if str(interaction.guild.id) in db:
      db[str(interaction.guild.id)]['reactionMessage'] = str(messageSent.id)
      db[str(interaction.guild.id)]['role'] = str(role.id)
      db[str(interaction.guild.id)]["roleEmoji"] = str(reaction)
    elif str(interaction.guild.id) not in db:
      db[str(interaction.guild.id)] = {"reactionMessage": str(messageSent.id), "role": str(role.id), "roleEmoji": str(reaction)}
    await messageSent.add_reaction(reaction)
    await interaction.send("Reaction role has been set up for this server.")
      
      

  

  @reactionrole.subcommand()
  async def remove(self, interaction: nextcord.Interaction):
    """Remove reaction role."""
    if str(interaction.guild.id) in db and 'role' in db[str(interaction.guild.id)]:
      del db[str(interaction.guild.id)]['role']
      del db[str(interaction.guild.id)]['roleEmoji']
      del db[str(interaction.guild.id)]['reactionMessage']
      await interaction.send("Reaction role message has been disabled.")
    else:
      await interaction.send("Sorry, it appears there is no reaction role message setup for this server.", ephemeral = True)

  @reactionrole.subcommand()
  async def addembed(self, interaction: nextcord.Interaction, channel: nextcord.abc.GuildChannel = nextcord.SlashOption(description = "Channel message should be sent in", channel_types = [nextcord.ChannelType.text]), role: nextcord.Role = nextcord.SlashOption(description = "Role that should be given"), reaction: str = nextcord.SlashOption(description = "Reaction to message."), title:str = nextcord.SlashOption(description = "Title of embed message", required = False, default = ""), description:str = nextcord.SlashOption(description = "Description for embed message", required = False, default = "No description provided."), colour:int = nextcord.SlashOption(description = "Color for embed message", required = False, default = 0x10E6f1), image_url: str = nextcord.SlashOption(description = "Url to image for embed message.", required = False, default = ""), author:str = nextcord.SlashOption(description = "Set author of embed message", required = False, default = ""), footer:str = nextcord.SlashOption(description = "Footer for embed message.", required = False, default = "")):
    """Create a reaction role embed message."""
    embed = nextcord.Embed(
      title = title,
      description = description,
      colour = colour
    )
    embed.set_image(url = image_url)
    embed.set_footer(text = footer)
    embed.set_author(name = author)
    messageSent = await channel.send(embed = embed)
    if str(interaction.guild.id) in db:
      db[str(interaction.guild.id)]['reactionMessage'] = str(messageSent.id)
      db[str(interaction.guild.id)]['role'] = str(role.id)
      db[str(interaction.guild.id)]["roleEmoji"] = str(reaction)
    elif str(interaction.guild.id) not in db:
      db[str(interaction.guild.id)] = {"reactionMessage": str(messageSent.id), "role": str(role.id), "roleEmoji": str(reaction)}
    await messageSent.add_reaction(reaction)
    await interaction.send("Reaction role has been set up for this server.")
      
    

  

    
      
      

def setup(client):
  client.add_cog(ReactionRole(client))