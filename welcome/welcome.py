import nextcord
from nextcord.ext import commands
from replit import db
import asyncio

class Confirm(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = "No input"
    self.timeout = 10

  @nextcord.ui.button(label = "Confirm", style = nextcord.ButtonStyle.green)
  async def confirmButton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.value = "confirm"
    self.stop()
    return
    

  @nextcord.ui.button(label = "Cancel", style = nextcord.ButtonStyle.danger)
  async def cancelButton(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.value = "cancel"
    self.stop()
    return


class Welcome(commands.Cog):
  def __init__(self, client):
    self.client = client

  @nextcord.slash_command(default_member_permissions = 8192)
  async def welcome(interaction: nextcord.Interaction):
    pass
  @welcome.subcommand()
  async def add(self, interaction:nextcord.Interaction, message:str = nextcord.SlashOption(description = "Message to send when member joins server."), channel: nextcord.abc.GuildChannel = nextcord.SlashOption(description = "Channel to send message in.", channel_types = [nextcord.ChannelType.text])):
    """Add welcome message to server."""
    if str(interaction.guild.id) in db:
      db[str(interaction.guild.id)]['welcomeMessage'] = message
      db[str(interaction.guild.id)]['welcomeMessageChannel'] = str(channel.id)
      await interaction.send("Welcome message has been edited.")
    elif str(interaction.guild.id) not in db:
      db[str(interaction.guild.id)] = {'welcomeMessage': message, 'welcomeMessageChannel': str(channel.id)}
      await interaction.send("Welcome message has been edited.")
  @welcome.subcommand()
  async def viewwelcomemessage(self, interaction: nextcord.Interaction):
    """View welcome message for server."""
    if str(interaction.guild.id) in db and 'welcomeMessage' in db[str(interaction.guild.id)]:
      embed = nextcord.Embed(
        title = f"Welcome message for **{interaction.guild.name}**:",
        description = db[str(interaction.guild.id)]['welcomeMessage'],
        colour = 0x10E6F1
      )
      embed.set_footer(text = f"This will be sent in <#{db[str(interaction.guild.id)]['welcomeMessageChannel']}>.")
      await interaction.send(embed = embed)
      
    else:
      await interaction.send("It appears there is no welcome message for the server at the moment.", ephemeral = True)

  
  @welcome.subcommand()
  async def remove(self, interaction: nextcord.Interaction):
    """Remove welcome message from server."""
    if str(interaction.guild.id) in db and 'welcomeMessage' in db[str(interaction.guild.id)]:
      del db[str(interaction.guild.id)]['welcomeMessage']
      await interaction.send("Welcome message deleted.")
    else:
      await interaction.send("It appears there is no welcome message for the server at the moment.", ephemeral = True)

  @welcome.subcommand()
  async def edit(self, interaction: nextcord.Interaction, new_message:str = nextcord.SlashOption(description = "New message to send when member joins server.")):
    """Edit the welcome message for server."""
    await interaction.send("Please wait...")
    view = Confirm()
    if str(interaction.guild.id) in db and 'welcomeMessage' in db[str(interaction.guild.id)]:
      overwrites = {
        self.client.user: nextcord.PermissionOverwrite(send_messages = True, view_channel = True),
        interaction.user.top_role: nextcord.PermissionOverwrite(send_messages = True, view_channel = True),
        interaction.guild.default_role: nextcord.PermissionOverwrite(view_channel = False)
      }
      channel = await interaction.guild.create_text_channel(name = "welcome-message-edit", overwrites = overwrites)
      embed = nextcord.Embed(
        title = "Action requested",
        description = f"**Change server welcome message:**\n\n{db[str(interaction.guild.id)]['welcomeMessage']} --> {new_message}",
        colour = 0x10E6F1
      )
      await channel.send(interaction.user.mention)
      await channel.send("This channel will be automatically deleted after command is used.")
      await channel.send(embed = embed, view = view)
      await view.wait()
      if view.value == "No input":
        await channel.send("Canceled.")
      elif view.value == "confirm":
        del db[str(interaction.guild.id)]['welcomeMessage']
        db[str(interaction.guild.id)]['welcomeMessage'] = new_message
        await channel.send("Message edited.")
      elif view.value == "cancel":
        await channel.send("Canceled.")
      await channel.send("This channel will automatically be deleted in 5 seconds.")
      await asyncio.sleep(5)
      await channel.delete()
    else:
      await interaction.send("It appears there is no welcome message for the server at the moment.", ephemeral = True)

  
  

  
  

def setup(client):
  client.add_cog(Welcome(client))