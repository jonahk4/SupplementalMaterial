import nextcord
from nextcord.ext import commands
from replit import db
import asyncio
from random import shuffle

class StudySetButton(nextcord.ui.Button):
  def __init__(self, assignedAction=None, user_id = None, current_card = 0):
    self.assignedAction = assignedAction
    self.user_id = user_id
    self.current_card = current_card
    self.terms = db[user_id]['studyset']['cards']
    self.front_faces = []
    self.back_faces = []
    self.current_state = "back"
    for t in self.terms:
      self.front_faces.append(t)
      self.back_faces.append(self.terms[t])
    if self.assignedAction == "flip":
      super().__init__(style = nextcord.ButtonStyle.gray, label=self.assignedAction)
    if self.assignedAction == "restart":
      super().__init__(style = nextcord.ButtonStyle.red, label=self.assignedAction)
    elif self.assignedAction == "continue":
      super().__init__(style = nextcord.ButtonStyle.green, label=self.assignedAction)
    elif self.assignedAction == "back":
      super().__init__(style = nextcord.ButtonStyle.blurple, label=self.assignedAction)
  async def callback(self, interaction: nextcord.Interaction):
    if self.assignedAction == "flip" and self.current_card <= len(self.front_faces) - 1:
      if self.current_state == "front":
        embed = nextcord.Embed(
          title = f"Card {self.current_card + 1}",
          description = f"{self.back_faces[self.current_card]}",
        )
        self.current_state = "back"
        await interaction.response.edit_message(embed=embed)
      else:
        embed = nextcord.Embed(
          title = f"Card {self.current_card + 1}",
          description = f"{self.front_faces[self.current_card]}",
        )
        
        self.current_state = "front"
        await interaction.response.edit_message(embed=embed)
    elif self.assignedAction == "restart":
      for child in self.view.children:
        child.current_card = 0
        child.current_state = "front"
      embed = nextcord.Embed(
        title = f"Card {self.current_card + 1}",
        description = f"{self.front_faces[self.current_card]}",
      )
      await interaction.response.edit_message(embed=embed)
    elif self.assignedAction == "continue":
      if self.current_card + 1 <= len(self.front_faces) - 1:
        for child in self.view.children:
          child.current_card += 1
          child.current_state = "front"
        embed = nextcord.Embed(
          title = f"Card {self.current_card + 1}",
          description = f"{self.front_faces[self.current_card]}",
        )
        await interaction.response.edit_message(embed=embed)
      else:
        embed = nextcord.Embed(
          title = "Blank",
          description = "End of deck."
        )
        for child in self.view.children:
          child.current_card = len(self.front_faces)
        await interaction.response.edit_message(embed=embed)
    elif self.assignedAction == "back":
      if self.current_card > 0:
        for child in self.view.children:
          child.current_card -= 1
          child.current_state = "front"
        embed = nextcord.Embed(
          title = f"Card {self.current_card + 1}",
          description = f"{self.front_faces[self.current_card]}",
        )
        await interaction.response.edit_message(embed=embed)
      else:
        pass
      
class StudySetUI(nextcord.ui.View):
  def __init__(self, user_id):
    super().__init__()
    buttonList = ["flip", "restart", "continue", "back"]
    for b in buttonList:
      self.add_item(StudySetButton(b, user_id))
class Study(commands.Cog):
  def __init__(self, client):
    self.client = client

  @nextcord.slash_command()
  async def studyset(self, interaction: nextcord.Interaction):
    pass

  @studyset.subcommand()
  async def flashcards(self, interaction: nextcord.Interaction):
    """Study the flashcards created"""
    if str(interaction.user.id) in db and 'studyset' in db[str(interaction.user.id)]:
      embed = nextcord.Embed(
        title = f"Flashcard mode - **{interaction.user.name}**",
        description = "Please press any card to start review."
      )
      view = StudySetUI(user_id = str(interaction.user.id))
      message = await interaction.send(embed=embed, view=view)
    else:
      await interaction.send("Sorry, it appears you don't have any studysets at the moment.")
    
  @studyset.subcommand(description = "Add a new card to the study set.")
  async def add(self, interaction: nextcord.Interaction, term:str = nextcord.SlashOption(description = "Phrase or question to ask.", max_length = 31), answer:str = nextcord.SlashOption(description = "Correct answer to phrase or question.", max_length = 31)):
    user_id = str(interaction.user.id)
    await interaction.send("Please wait...")
    if user_id not in db:
      db[user_id] = {}
      db[user_id]['studyset'] = {}
      db[user_id]['studyset']['cardcounter'] = 0
      db[user_id]['studyset']['cards'] = {}
      db[user_id]['studyset']['cards'] = {}
      db[user_id]['studyset']['cards'][term] = answer
      await interaction.channel.send("Card added.")
      db[user_id]['studyset']['cardcounter'] += 1
      return
    elif user_id in db and 'studyset' not in db[user_id]:
      db[user_id]['studyset'] = {}
      db[user_id]['studyset']['cardcounter'] = 0
      db[user_id]['studyset']['cards'] = {}
      db[user_id]['studyset']['cards'] = {}
      db[user_id]['studyset']['cards'][term] = answer
      await interaction.channel.send("Card added.")
      db[user_id]['studyset']['cardcounter'] += 1
      return
    elif (user_id in db and 'studyset' in db[user_id]) and int(db[user_id]['studyset']['cardcounter'] < 30):
      cardcounter = db[user_id]['studyset']['cardcounter']
      db[user_id]['studyset']['cards']
      db[user_id]['studyset']['cards'][term] = answer
      db[user_id]['studyset']['cardcounter'] += 1
      await interaction.channel.send(f"Card added. You have {db[user_id]['studyset']['cardcounter']}/30 cards used.")
      return
    elif (user_id in db and 'studyset' in db[user_id]) and int(db[user_id]['studyset']['cardcounter'] >= 30):
      await interaction.channel.send("Sorry, you have created the maximum number of cards allowed. Please delete some to add more.")
      return
    else:
      await interaction.channel.send("An error occured. Please try again later.")
      return
  @studyset.subcommand(description = "View the cards created in the study set.")
  async def view(self, interaction: nextcord.Interaction):
    user_id = str(interaction.user.id)
    if (user_id in db and 'studyset' in db[user_id]) and int(db[user_id]['studyset']['cardcounter']) > 0:
      cardCounter = 0
      questions = []
      answers = []
      while cardCounter < db[user_id]['studyset']['cardcounter']:
        questions.append(list(db[user_id]['studyset']['cards'].keys())[cardCounter])
        answers.append(list(db[user_id]['studyset']['cards'].values())[cardCounter])
        cardCounter += 1
      cardCounterTwo = 0
      returnMessage = f"**{interaction.user.name}'s Study Set**\n"
      while cardCounterTwo < len(questions):
        returnMessage += f"`{cardCounterTwo}` {questions[cardCounterTwo]} ---> {answers[cardCounterTwo]}\n"
        cardCounterTwo += 1
      returnMessage += "\n```To remove a card from the study set, please specify the number indicated on the left in the /removestudycard command.```"
      await interaction.send(returnMessage)
      return
    else:
      await interaction.send("Sorry, it appears you do not have any cards in this study set at the moment.", ephemeral = True)
      return

  @studyset.subcommand(description = "Remove a card from your study set.")
  async def remove(self, interaction: nextcord.Interaction, number:int = nextcord.SlashOption(description = "Card number to remove from study set.")):
    user_id = str(interaction.user.id)
    if (user_id in db and 'studyset' in db[user_id]):
      try:
        keyList = list(db[user_id]['studyset']['cards'].keys())
        del db[user_id]['studyset']['cards'][keyList[number]]
        db[user_id]['studyset']['cardcounter'] -= 1
        await interaction.send("Card deleted.")
        return
      except:
        await interaction.send("Sorry, we could not find this card.")
      return
    elif (user_id in db and 'studyset' in db[user_id]) and str(number) not in db[user_id]['studyset']['cards']:
      await interaction.send("Sorry, we could not find this card.")
      return
    else:
      await interaction.send("Sorry, it appears that you do not have any cards in the study set at the moment.")
      return
    
  @studyset.subcommand(description = "Study the set created.")
  async def study(self, interaction: nextcord.Interaction, reverse: str = nextcord.SlashOption(choices = {"true":"true", "false":"false"}), mode: str = nextcord.SlashOption(choices = {"test":"test", "study":"study"})):
    await interaction.send("Please wait...")
    user_id = str(interaction.user.id)
    if (user_id in db and 'studyset' in db[user_id]) and db[user_id]['studyset']['cardcounter'] > 0:
      cardOrderList = []
      addNumber = 0
      correctAnswers = 0
      while addNumber < db[user_id]['studyset']['cardcounter']:
        cardOrderList.append(addNumber)
        addNumber += 1
      shuffle(cardOrderList)
      studyCardCounter = 0
      while len(cardOrderList) > 0:
        if reverse == "false":
          await interaction.send(list(db[user_id]['studyset']['cards'].keys())[cardOrderList[-1]])
          correctAnswer = list(db[user_id]['studyset']['cards'].values())[cardOrderList[-1]].lower()
        elif reverse == "true":
          await interaction.send(list(db[user_id]['studyset']['cards'].values())[cardOrderList[-1]])
          correctAnswer = list(db[user_id]['studyset']['cards'].keys())[cardOrderList[-1]].lower()
        def checkAnswer(m):
          if m.content.lower() == correctAnswer:
            raise ValueError
          elif m.content.lower() != correctAnswer and m.author == interaction.user:
            raise KeyError
          else:
            pass
        try:
          await self.client.wait_for('message', check=checkAnswer)
        except ValueError:
          await interaction.send("Correct!")
          if mode == "test":
            correctAnswers += 1
          del cardOrderList[-1]
          continue
        except KeyError:
          if mode == "test":
            await interaction.channel.send(f"Oops! Not quite! The correct answer was **{correctAnswer}**.")
            del cardOrderList[-1]
            continue
          else:
            await interaction.channel.send("Oops! Not quite!")
      if mode == "study":
        await interaction.channel.send("Great job!")
        return
      await interaction.send(f"You got {correctAnswers}/{db[user_id]['studyset']['cardcounter']} questions correct. Great job!")
      return
    else:
      await interaction.channel.send("Sorry, it appears your study set is empty at the moment. Add cards through the `/addstudycard` command.")
    
  @studyset.subcommand(description = "Delete a created study set.")
  async def reset(self, interaction: nextcord.Interaction):
    await interaction.send("Please wait...")
    user_id = str(interaction.user.id)
    if user_id in db and "studyset" in db[user_id]:
      del db[user_id]['studyset']
      await interaction.channel.send(":green_circle: Study set has been cleared.")
    else:
      await interaction.send("Sorry, it appears your study set is empty at the moment. Add cards through the `/addstudycard` command.")
def setup(client):
	client.add_cog(Study(client))