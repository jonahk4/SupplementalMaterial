#imports
import nextcord
from nextcord.ext import commands
import asyncio
from system import tickets
from replit import db
class Tickets(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.__category = None
    self.__reason = None
    self.__message = None
    self.__topic = None

  @nextcord.slash_command(default_member_permissions = 16)
  async def tickets(self, interaction: nextcord.Interaction):
    pass
  
  @tickets.subcommand()
  async def setup(self, interaction: nextcord.Interaction):
    """Setup the ticket system for the server."""
    server_id = str(interaction.guild.id)
    if (server_id in db and 'ticketStatus' in db[server_id]) and nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory'])):
      await interaction.send("Error: `Ticket system has already been setup for this server.`", ephemeral = True)
      return
    elif server_id in db and 'ticketStatus' not in db[server_id]:
      await interaction.send("We're updating some things on our end. Please standby...")
      db[server_id]['ticketStatus'] = "on"
      db[server_id]['ticketMessage'] = "Thanks for opening a ticket! We'll be with you in a few moments."
      db[server_id]['ticketDescription'] = "Welcome to a new ticket!"
      newCategory = await interaction.guild.create_category(name = "Tickets")
      db[server_id]['ticketCategory'] = str(newCategory.id)
    else:
      await interaction.send("We're updating some things on our end. Please standby...")
      db[server_id] = {}
      db[server_id]['ticketStatus'] = "on"
      db[server_id]['ticketMessage'] = "Thanks for opening a ticket! We'll be with you in a few moments."
      db[server_id]['ticketDescription'] = "Welcome to a new ticket!"
      newCategory = await interaction.guild.create_category(name = "Tickets")
      db[server_id]['ticketCategory'] = str(newCategory.id)
    await interaction.channel.send("Ticket system has been set up.")
    return
  

  @tickets.subcommand()
  async def editmessage(self, interaction: nextcord.Interaction, message:str = nextcord.SlashOption(description = "new ticket message to edit.")):
    """Edit the message that is sent when a ticket is created."""
    server_id = str(interaction.guild.id)
    if (server_id in db and 'ticketStatus' in db[server_id]) and nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory'])):
      db[server_id]['ticketMessage'] = message
      await interaction.send("Message updated.")
      return
    else:
      await interaction.send("Please setup the ticket system using the `/setupticketsystem` command.", ephemeral = True)
      return
  
  @tickets.subcommand()
  async def edittopic(self, interaction: nextcord.Interaction, topic: str = nextcord.SlashOption(description = "Topic to set ticket when created.")):
    """Edit the topic that is set when a new ticket is created."""
    server_id = str(interaction.guild.id)
    if (server_id in db and 'ticketStatus' in db[server_id]) and nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory'])):
      db[server_id]['ticketDescription'] = topic
      await interaction.send("Topic has been edited.")
      return
    else:
      await interaction.send("Please setup the ticket system using the `*/setupticketsystem` command.", ephemeral = True)
      return
 
  @tickets.subcommand()
  async def setstatus(self, interaction: nextcord.Interaction, choice:str = nextcord.SlashOption(description = "Choice to set ticket system", choices = {"on": "on", "off": "off"})):
    """Set the ticket system to be on or off."""
    server_id = str(interaction.guild.id)
    if (server_id in db and 'ticketStatus' in db[server_id]) and (nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory'])) and choice == "on"):
      db[server_id]['ticketStatus'] = 'on'
      await interaction.send("Ticket system is `active`")
      return
    elif (server_id in db and 'ticketStatus' in db[server_id]) and (nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory'])) and choice == "off"):
      db[server_id]['ticketStatus'] = "off"
      await interaction.send("Ticket system is `inactive`")
      return
    else:
      await interaction.send("Please setup the ticket system using the `/setupticketsystem` command.", ephemeral = True)
      return
 
  
       
  @tickets.subcommand()
  async def settings(self, interaction: nextcord.Interaction):
    """Returns the settings for the ticket system in your server."""
    server_id = str(interaction.guild.id)
    if (server_id in db and 'ticketStatus' in db[server_id]) and nextcord.utils.get(interaction.guild.categories, id = int(db[server_id]['ticketCategory'])):
      ticketMessage = db[server_id]['ticketMessage']
      ticketDescription = db[server_id]['ticketDescription']
      embed = nextcord.Embed(
        title = f"Ticket system settings for **{interaction.guild.name}**",
        description = f"Ticket message: {ticketMessage}\nTicket topic: {ticketDescription}",
        colour = 0x10E6F1
      )
      embed.set_footer(text = f"Ticket system is {db[server_id]['ticketStatus']} for this server.")
      await interaction.send(embed = embed)
      return
    else:
      await interaction.send("Please setup the ticket system using the `/setupticketsystem` command.", ephemeral = True)
      return
    
  
  @tickets.subcommand()
  async def closeticket(self, interaction: nextcord.Interaction):
    """Closes the ticket the command is invoked in."""
    await interaction.send("Please wait...")
    embed = nextcord.Embed(
        title = "Warning.",
        description = "Are you sure you want to close this ticket?",
        colour = 0x10E6F1
      )
    message = await interaction.channel.send(embed = embed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    def check(reaction, user):
      if user == interaction.user and reaction.emoji == '✅':
        return user == interaction.user and reaction.emoji == '✅'
      elif user == interaction.user and reaction.emoji != '✅':
        raise ValueError
    
        
    try:
      reaction, user = await self.client.wait_for('reaction_add', timeout = 10.0, check = check)
      await interaction.channel.send("Ticket is closing automatically in 5 seconds.")
      await asyncio.sleep(5)
      await interaction.channel.delete()
      return
    except ValueError:
      await interaction.channel.send(':x:Canceled.')
      return
    except asyncio.TimeoutError:
      await interaction.channel.send(":x:Canceled.")
      return
 

def setup(client):
	client.add_cog(Tickets(client))