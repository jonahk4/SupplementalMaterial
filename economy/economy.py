import nextcord
from nextcord.ext import commands
import datetime
from system import economy
import asyncio
from replit import db
from system import timehelper
class Economy(commands.Cog):
  def __init__(self, client):
    self.client = client

  @nextcord.slash_command()
  async def economy(self, interaction: nextcord.Interaction):
    pass
    
  @economy.subcommand()
  async def daily(self, interaction: nextcord.Interaction):
    """Get daily gift of stars"""
    if (str(interaction.user.id) in db and 'lastdaily' not in db[str(interaction.user.id)]):
      await interaction.send("We're updating some things on our end. Please standby...")
      db[str(interaction.user.id)]['lastdaily'] = str(datetime.datetime.utcnow())
      await interaction.channel.send("Thanks for waiting!")
      db[str(interaction.user.id)]['balance'] = 50
      await interaction.channel.send(":star:Daily gift of 50 stars has been rewarded.:star:")
      return
    elif str(interaction.user.id) not in db:
      await interaction.send("We're updating some things on our end. Please standby...")
      db[str(interaction.user.id)] = {}
      db[str(interaction.user.id)]['lastdaily'] = str(datetime.datetime.utcnow())
      await interaction.channel.send("Thanks for waiting!")
      db[str(interaction.user.id)]['balance'] = 50
      await interaction.channel.send(":star:Daily gift of 50 stars has been rewarded.:star:")
      return
    else:
      if timehelper.getdifference(db[str(interaction.user.id)]['lastdaily']) < 86400:
        await interaction.send("Please try again later.", ephemeral = True)
        return
      else:
        db[str(interaction.user.id)]['lastdaily'] = str(datetime.datetime.utcnow())
    user = str(interaction.user.id)
    if user in db and 'balance' in db[user]:
      db[user]['balance'] += 50
      await interaction.send(":star:Daily gift of 50 stars has been rewarded.:star:")
      return
    elif user not in db:
      db[user] = {}
      db[user]['balance'] = 50
      await interaction.send(":star:Daily gift of 50 stars has been rewarded.:star:")
      return
 


  @economy.subcommand()
  async def balance(self, interaction: nextcord.Interaction):
    """Returns the number of stars you have."""
    user = str(interaction.user.id)
    if (user in db and "balance" in db[user]) and db[user]["balance"] > 0:
      currentBalance = db[user]["balance"]
      embed = nextcord.Embed(
        title = "",
        description = f"**Current Balance:**\n:star:{currentBalance} stars",
        colour = 0x10E6F1
      )
      embed.set_author(name = f'{interaction.user}')
      await interaction.send(embed = embed, ephemeral = True)
      return
    else:
      await interaction.send("Sorry, it appears you do not have any stars at the moment.", ephemeral = True)
      return
 

  @economy.subcommand()
  async def gift(self, interaction: nextcord.Interaction, member:nextcord.Member = nextcord.SlashOption(description = "Member to gift stars to."), amount: int = nextcord.SlashOption(description = "Number of stars to give.")):
    """Gift stars to another member of the server."""
    giftUser = member
    user = str(interaction.user.id)
    amountToAdd = int(amount)
    if ((user in db and 'balance' in db[user]) and db[user]['balance'] >= amountToAdd) and (str(giftUser.id) in db and 'balance' in db[str(giftUser.id)]):  
      db[str(giftUser.id)]['balance'] += int(amount)
      db[user]['balance'] -= int(amount)
      await interaction.send(f":star:{amount} stars were given to {giftUser.mention}.")
      return
    elif ((user in db and 'balance' in db[user]) and db[user]['balance'] >= amountToAdd) and (str(giftUser.id) not in db):
      db[str(giftUser.id)] = {"balance": int(amount)}
      db[user]['balance'] -= int(amount)
      await interaction.send(f"{amount} stars were given to {giftUser.mention}.")
      return
    else:
      await interaction.send("Sorry, it appears you do not have enough stars to gift this amount.", ephemeral = True)
      return
 

def setup(client):
	client.add_cog(Economy(client))