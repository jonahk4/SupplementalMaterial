import nextcord
from nextcord.ext import commands
import asyncio
from replit import db
import os
from system import autoresponse
class Autoresponder(commands.Cog):
  def __init__(self, client):
    self.client = client
  @nextcord.slash_command(default_member_permissions = 8192)
  async def autoreply(interaction: nextcord.Interaction):
    pass
  @autoreply.subcommand()
  async def setup(self, interaction: nextcord.Interaction):
    """Setup the auto-reply system for server."""
    server_id = str(interaction.guild.id)
    await interaction.send("One moment please...")
    if server_id in db and 'status' in db[server_id]:
      await interaction.send("Auto-reply system has already been set up.")
      return
    elif server_id in db and 'status' not in db[server_id]:
      db[server_id]['status'] = "on"
      db[server_id]['autoreplycounter'] = 0
      db[server_id]['autoreplies'] = {}
      await interaction.channel.send("Auto-reply system is ready.")
      return
    elif server_id not in db:
      db[server_id] = {}
      db[server_id]['status'] = "on"
      db[server_id]['autoreplycounter'] = 0
      db[server_id]['autoreplies'] = {}
      await interaction.channel.send("Auto-reply system is ready.")
      return

  
  @autoreply.subcommand()
  async def setstatus(self, interaction: nextcord.Interaction, choice = nextcord.SlashOption(choices = {"on" : "on", "off": "off"})):
    """Set the auto-reply system to be on or off."""
    server_id = str(interaction.guild.id)
    if server_id in db and 'status' in db[server_id]:
      if choice == "on":
        db[server_id]['status'] = "on"
        await interaction.send(":green_circle: Autoreply system is now active.")
        return
      elif choice == "off":
        db[server_id]['status'] = "off"
        await interaction.send(":red_circle: Autoreply system is now inactive.")
        return
      else:
        await interaction.send("Please use `on` or `off` as the choice for this command.")
        return
    else:
      await interaction.send("Please setup the auto-reply system before using this command. Use `/setupAutoReply` for setup.")
      return


  @autoreply.subcommand()
  async def add(self, interaction: nextcord.Interaction, message_to_reply_to: str = nextcord.SlashOption(description = "message bot should reply to"), reply:str = nextcord.SlashOption(description = "message bot should reply with")):
    """Add an autoreply for the server."""
    sendReplyMessage = str(message_to_reply_to)
    reply = str(reply)
    server_id = str(interaction.guild.id)
    if (server_id in db and 'status' in db[server_id]) and (sendReplyMessage not in db[server_id]['autoreplies'] and db[server_id]['autoreplycounter'] < 10):
      db[server_id]['autoreplies'][sendReplyMessage.lower()] = reply
      db[server_id]['autoreplycounter'] += 1
      counter = db[server_id]['autoreplycounter']
      await interaction.send(f"Autoreply has been added. You have used {counter}/10 autoreply messages.")
      return
    elif (server_id in db and 'status' in db[server_id]) and sendReplyMessage in db[server_id]['autoreplies']:
      await interaction.send("Error: `Autoreply already exists.`")
      return
    elif (server_id in db and 'status' in db[server_id]) and db[server_id]['autoreplycounter'] >= 10:
      await interaction.send("Sorry, you have reached the maximum amount of autoreplies in this server. To add more, please delete ones you do not need using the `/removeAutoReply` command.")
      return
    else:
      await interaction.send("Please setup the autoreply system using the `/setupAutoReply` command.")
      return
  
  @autoreply.subcommand()
  async def remove(self, interaction: nextcord.Interaction, message_bot_replies_to: str = nextcord.SlashOption(description = "Message that the bot replies to.")):
    """Deletes the specified autoreply"""
    autoReplyMessage = str(message_bot_replies_to).lower()
    server_id = str(interaction.guild.id)
    if (server_id in db and 'status' in db[server_id]) and autoReplyMessage in db[server_id]['autoreplies']:
      del db[server_id]['autoreplies'][autoReplyMessage]
      db[server_id]['autoreplycounter'] -= 1
      await interaction.send("Autoreply deleted.")
      return
    elif (server_id in db and 'status' in db[server_id]) and autoReplyMessage not in db[server_id]['autoreplies']:
      await interaction.send("Error: `Autoreply not found.`")
      return
    else:
      await interaction.send("Please setup the autoreply system using the `/setupAutoReply` command.")
      return
  
  @autoreply.subcommand()
  async def autoreplies(self, interaction: nextcord.Interaction):
    """Returns the list of autoreplies for the server."""
    server_id = str(interaction.guild.id)
    if (server_id in db and 'status' in db[server_id]) and db[server_id]['autoreplies'] != {}:
      messageList = []
      replyList = []
      for x in db[server_id]['autoreplies'].keys():
        messageList.append(x)
      for y in db[server_id]['autoreplies'].values():
        replyList.append(y)
      await interaction.send(f"**Autoreplies for {interaction.guild.name}**\n(prompt--->reply)")
      while len(messageList) > 0:
        await interaction.channel.send(f"{messageList[0]} ---> {replyList[0]}")
        del messageList[0]
        del replyList[0]
      await interaction.channel.send("**---End Autoreply List---**")
      return
    elif (server_id in db and 'status' in db[server_id]) and db[server_id]['autoreplies'] == {}:
      await interaction.send("No autoreplies are active in this server at the moment.")
      return
    else:
      await interaction.send("Please setup the autoreply system using the `/setupAutoReply` command.")

  @autoreply.subcommand()
  async def reset(self, interaction: nextcord.Interaction):
    """Reset the autoreply system for the server."""
    await interaction.send(f"Please wait...")
    server_id = str(interaction.guild.id)
    if server_id not in db:
      await interaction.channel.send("There appears to be no autoreplies to delete at the moment.")
      return
    elif (server_id in db and 'autoreplies' not in db[server_id]) or (server_id in db and db[server_id]['autoreplies'] == {}):
      await interaction.channel.send("There appears to be no autoreplies to delete at the moment.")
      return
    elif server_id in db and 'autoreplies' in db[server_id]:
      embed = nextcord.Embed(
        title = f"Are you sure you want to proceed with this action?",
        description = "This will delete any changes made to the autoreply system in your server."
      )
      embed.set_footer(text = f"Server Id: {server_id}")
      message = await interaction.channel.send(embed = embed)
      await message.add_reaction("✅")
      await message.add_reaction("❌")
      def check(reaction, user):
        if user == interaction.user and reaction.emoji == "✅":
          raise ValueError
        elif user == interaction.user and reaction.emoji != "✅":
          raise TypeError
        elif user != interaction.user:
          pass
      try:
        await self.client.wait_for('reaction_add', timeout = 10.0, check = check)
      except ValueError:
        del db[server_id]['autoreplies']
        del db[server_id]['status']
        del db[server_id]['autoreplycounter']
        await interaction.channel.send("✅ Autoreply system has been reset.")
        return
      except TypeError:
        await interaction.channel.send("Action canceled.")
        return
      except asyncio.TimeoutError:
        await interaction.channel.send("Action canceled.")
        return
  

def setup(client):
	client.add_cog(Autoresponder(client))


