import nextcord
from nextcord.ext import commands
import asyncio
from replit import db
import os
import datetime
import math

class Settings(commands.Cog):
  def __init__(self, client):
    self.client = client
  @nextcord.slash_command(default_member_permissions = 268435472)
  async def settings(self, interaction: nextcord.Interaction):
    pass
  
  @settings.subcommand()
  async def language(self, interaction: nextcord.Interaction, language:str = nextcord.SlashOption(choices = {"ko":"ko", "es":"es", "en":"en"}), description = "Please select a language."):
    """Set the language for Polaris in your server."""
    await interaction.send("Sorry, this command is still under construction. Please try again later.")
    return

  @settings.subcommand()
  async def power(self, interaction: nextcord.Interaction, choice:str = nextcord.SlashOption(choices = {"on":"on", "off":"off"}, description = "Please select an option.")):
    """Set whether Polaris should respond to commands in your server."""
    server_id = str(interaction.guild.id)
    if server_id in db:
      db[server_id]['power'] = choice
    else:
      db[server_id] = {'power': choice}
    await interaction.send(f"Polaris has been turned {choice}")
    
  
def setup(client):
	client.add_cog(Settings(client))