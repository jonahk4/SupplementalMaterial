import nextcord
import datetime 

class Command:
  def __init__(self, name, description, arguments="None", required_permissions="None", category="None"):
    self.name = name
    self.arguments = arguments
    self.description = description
    self.category = category
    self.required_permissions = required_permissions

class HelpCommand:
  def __init__(self, commands=None):
    self.commands = commands
  def present(self):
    pagetext = "Commands for Polaris can be used through the slash command system on Discord.\n\nA list of commands can also be viewed here: https://en.polarisbot.com/docs/\n"
    categories = [self.commands[0].category]
    i = 1
    while i <= len(self.commands) - 1:
      if self.commands[i - 1].category == self.commands[i].category or self.commands[i].category in categories:
        pass
      else:
        categories.append(self.commands[i].category)
      i += 1
    for category in categories:
      pagetext += f"\n**__{category}__**\n"
      for command in self.commands:
        if command.category == category:
          pagetext += f"{command.name}\u2002"
        else:
          pass
    embed = nextcord.Embed(
      description = pagetext
    )
    embed.set_footer(text = "For more information on a command use /help [commandName]")
    embed.set_author(name = "Polaris Help", icon_url = "https://cdn.discordapp.com/attachments/1023304673924497408/1023304773669240882/logo.png")
    return embed


def findcommand(query, commandlist):
  returnlist = []
  for command in commandlist:
    if command.name == query:
      returnlist.append(command)
    else:
      pass
  pagetext = ""
  for command in returnlist:
    pagetext += f"**/{command.category.lower()} {command.name}**\n{command.description}\n\n"
    pagetext += f"Parameters: {command.arguments}\nRequired Permissions: {command.required_permissions}\n\n"
  embed = nextcord.Embed(
    title = f"Your query returned {len(returnlist)} results:",
    description = pagetext,
  )
  embed.set_author(name = "Polaris Help", icon_url = "https://cdn.discordapp.com/attachments/1023304673924497408/1023304773669240882/logo.png")
  embed.set_footer(text=f"{datetime.datetime.utcnow()}")
  return embed
  
      
commandlist = [
  Command("clear", "Clears a specified amount of messages from a channel. Must be less than 501 messages.", "[number_of_messages]", "manage_messages", "Moderation"),
  Command("mute", "Mute(timeout) a member for a specified period of time.", "[member] [time_duration] (reason)", "manage_roles", "Moderation"),
  Command("unmute", "Unmute a member.", "[member]", "manage_roles", "Moderation"),
  Command("reset", "Reset the autoreply system.", "None", "manage_messages", "Autoreply"),
  Command("add", "Add an automated reply to a given message in the server.", "[message_to_reply_to] [message_to_reply_with]", "manage_messages", "Autoreply"),
  Command("autoreplies", "View the autoreplies setup for the server.", "None", "manage_messages", "Autoreply"),
  Command("remove", "Remove an autoreply set for the server.", "[message_bot_should_not_respond_to]", "manage_messages", "Autoreply"),
  Command("setstatus", "Set whether the autoreply system should be on or off", "[on/off]", "manage_messages", "Autoreply"),
  Command("setup", "Set up the autoreply system for the server.", "None", "manage_messages", "Autoreply"),
  Command("balance", "Returns the current number of stars you have.", "None", "None", "Economy"),
  Command("daily", "Recieve your daily gift of 50 stars", "None", "None", "Economy"),
  Command("gift", "Gift another user a specified number of stars", "[member_of_server] [amount]", "None", "Economy"),
  Command("dadjoke", "Returns a random dadjoke.", "None", "None", "Frivolity"),
  Command("guesstheword", "Guess the word that the bot has scrambled.", "None", "None", "Frivolity"),
  Command("quiz", "Answer a quiz question for stars", "None", "None", "Frivolity"),
  Command("xkcd", "Returns the latest xkcd comic.", "[comic_number (optional)]", "None", "Frivolity"),
  Command("createembed", "Have the bot send an embed message with specified fields.", "(title) (description) (color) (image) (author) (footer) (channel)", "manage_channels", "Utilities"),
  Command("ban", "Ban a specified member from the server.", "[member] (reason)", "ban_members, manage_channels", "Moderation"),
  Command("kick", "Kick a specified member from the server.", "[member] (reason)", "manage_channels, kick_members", "Moderation"),
  Command("play", "Play tictactoe with another member of the server.", "[player_one] [player_two]", "None", "Tictactoe"),
  Command("playwithbot", "Play tictactoe with Polaris.", "None", "None", "Tictactoe"),
  Command("createticket", "Create a ticket in the server.", "None", "None", "Tickets"),
  Command("setup", "Setup the ticket system using Polaris for the server.", "None", "manage_channels", "Tickets"),
  Command("closeticket", "Delete the channel that this command is used in.", "None", "manage_channels", "Tickets"),
  Command('edittopic', "Edit the topic for the channel when a ticket is created.", "[new_topic]", "manage_channels", "Tickets"),
  Command('editmessage', "Edit the message sent when a ticket is created.", "[new_message]", "manage_channels", "Tickets"),
  Command("settings", "View the settings for the ticket system using Polaris in the server.", "None", "manage_channels", "Tickets"),
  Command("setstatus", "Set whether members have the ability to create a ticket in the server.", "[status (on/off)]", "manage_channels", "Tickets"),
  Command("setreminder", "Have the bot send a message after a certain period of time.", "[message] [time_duration]", "None", "Utilities"),
  Command("calc", "Calculator.", "[expression]", "None", "Utilities"),
  Command("dna", "Returns the base DNA and RNA pairs for a given sequence.", "[sequence]", "None", "Utilities"),
  Command("ping", "Returns the bot latency in miliseconds.", "None", "None", "Utilities"),
  Command("projectile", "Returns the horizontal displacement of a projectile launched at a specified initial speed and angle to the horizontal.", "[initial_speed(m/s)] [angle_of_launch(degrees)]", "None", "Utilities"),
  Command("quadratic", "Returns the roots of a quadratic equation", "[equation_as_function_of_x]", "None", "Utilities"),
  Command("solvesystem", "Solve a system of two or three linear equations.", "[equations]", "None", "Utilities"),
  Command("addwelcomemessage", "Set the message Polaris will send when a new member joins the server.", "[message] [channel]", "manage_messages", "Welcome"),
  Command("editwelcomemessage", "Edit the message sent when a member joins the server.", "[new_message]", "manage_messages", "Welcome"),
  Command("removewelcomemessage", "Remove the welcome message for the server.", "None", "manage_messages", "Welcome"),
  Command("viewwelcomemessage", "View the welcome message for the server.", "None", "manage_messages", "Welcome"),
  Command("addreactionrole", "Add a reaction role for the server with Polaris.", "[message] [channel] [role] [reaction]", "manage_roles", "Reaction Roles"),
  Command("deletereactionrole", "Remove the reaction role set.", "None", "manage_roles", "Reaction Roles"),
  Command("addwarning", "Warn a member of the server.", "[member]", "manage_roles", "Moderation"),
  Command("viewwarnings", "Returns the number of warnings that the specified member has in the server.", "[member]", "manage_roles", "Moderation"),
  Command("removewarnings", "Remove a specified number of warnings for a member of the server.", "[member] [number]", "manage_roles", "Moderation"),
  Command("editwelcomemessage", "Edit the existing welcome message set for the server.", "message", "manage_messages", "Welcome"),
  Command("reset", "Resets the autoreply system.", "None", "manage_messages", "Autoreply"),
  Command("getbotinfo", "Get information about the bot.", "None", "None", "Settings"),
  Command("invite", "Returns a link to invite the bot to your server.", "None", "None", "Settings"),
  Command("addembed", "Add a reaction role embed message.", "[channel] [role] [reaction] (title) (description) (color) (image) (author) (footer)", "manage_roles", "Reaction Roles"),
  Command("converttemperature", "Convert between common units of temperature.", "[number] [from] [to]", "None", "Utilities"),
  Command("addstudycard", "Add a card to the study set.", "[question] [answer]", "None", "Study"),
  Command("viewstudyset", "View the study set.", "None", "None", "Study"),
  Command("removestudycard", "Remove a card from the study set.", "[index]", "None", "Study"),
  Command("study", "Study the set created.", "[reverse=true/false]", "None", "Study"),
  Command("dotproduct", "Take the dot product between two vectors.", "[v1] [v2]", "None", "Utilities"),
  Command("match", "Matching game.", "None", "None", "Frivolity"),
  Command("convertcoordinates", "Convert between polar and rectangular coordinates.", "[coordinates to convert] [from] [to]", "None", "Utilities"),
  Command("convertangle", "Convert between degrees and radians.", "[from] [to] [angle]", "None", "Utilities")
    
]
