import nextcord
from nextcord.ext import commands
import asyncio
from random import randint, choice, shuffle
from system import quiz
from system import wordsolver
from system import xkcdhelper
from system import economy
from dadjokes import Dadjoke
from replit import db
from textblob import TextBlob
from system import timehelper
import datetime

class QuizInterface(nextcord.ui.Select):
  def __init__(self, possible_choices, correct_answer):
    self.possible_choices = possible_choices
    self.correct_answer = correct_answer
    options = []
    i = 0
    while i <= len(self.possible_choices) - 1:
      options.append(nextcord.SelectOption(label=str(i+1), description=f"Answer choice {i+1}"))
      i += 1
    super().__init__(
      placeholder = "Select an answer choice...",
      min_values = 1,
      max_values = 1,
      options = options 
    )
  async def callback(self, interaction: nextcord.Interaction):
    self.disabled = True
    self.placeholder = self.values[0]
    if int(self.values[0]) == self.correct_answer:
      author_id = str(interaction.user.id)
      if author_id in db and 'balance' in db[author_id]:
        db[author_id]['balance'] += 15
      elif author_id in db and 'balance' not in db[author_id]:
        db[author_id]['balance'] = 15
      elif author_id not in db:
        db[author_id] = {}
        db[author_id]['balance'] = 15
      await interaction.response.edit_message(content=":star: Correct! 15 stars have been added to your current balance. :star:", view=self.view)
      self.view.isActive = False
    else:
      await interaction.response.edit_message(content=f"Sorry, your answer choice was incorrect. The correct answer was **{self.correct_answer}**", view=self.view)
      self.view.isActive = False

class QuizView(nextcord.ui.View):
    def __init__(self, possible_choices, correct_answer, isDisabled = False, isActive = True, timeout=15):
      self.possible_choices = possible_choices
      self.correct_answer = correct_answer
      self.isDisabled = isDisabled
      self.isActive = isActive
      super().__init__(timeout=timeout)
      self.add_item(QuizInterface(self.possible_choices, self.correct_answer))
    async def on_timeout(self):
      self.isDisabled = True
      for x in self.children:
        x.disabled = True
      
      
      
class Square(nextcord.ui.Button):
  def __init__(self, setrow, setemoji:nextcord.Emoji):
    self.setrow = setrow
    self.setemoji = setemoji
    super().__init__(style=nextcord.ButtonStyle.secondary, emoji=setemoji, row = setrow)
  async def callback(self, interaction: nextcord.Interaction):
    
    view = self.view
    id_list = []
    for x in self.view.children:
      id_list.append(x.custom_id)
    if self.view.startcounter == 0:
      for x in self.view.children:
        x.emoji = None
        x.label = "\u200b"
      await interaction.response.edit_message(content="Ready!", view=view)
      self.view.startcounter += 1
    else:
        activesquare = False
        for x in self.view.children:
          if x.emoji != None and x.disabled == False:
            activesquare = True
          else:
            pass
        if activesquare:
          self.emoji = self.view.squares[id_list.index(self.custom_id)]
          active_square_index = []
          i = 0
          while i < len(self.view.children):
            if (self.view.children[i].emoji != None and self.view.children[i].disabled == False) and id_list.index(self.custom_id) != i:
              active_square_index.append(i)
            else:
              pass
            i += 1
          if self.view.squares[id_list.index(self.custom_id)] == self.view.squares[active_square_index[0]]:
            self.view.children[id_list.index(self.custom_id)].disabled = True
            self.view.children[active_square_index[0]].disabled = True
            await interaction.response.edit_message(content="Match!", view=view)
            correctlist = []
            for x in self.view.children:
              if x.emoji != None:
                correctlist.append(x)
            if len(correctlist) == len(self.view.squares):
              await interaction.send(":tada:You won, great job!")
          else:
            if self.view.incorrect_tries < 3:
              self.view.incorrect_tries += 1
              await interaction.response.edit_message(content=f":x:Oops! No match. You have {3 - self.view.incorrect_tries} incorrect tries remaining.", view=view)
              self.emoji = None
              self.view.children[active_square_index[0]].emoji = None
            else:
              self.emoji = self.view.squares[id_list.index(self.custom_id)]
              await interaction.response.edit_message(content="Game over.", view=view)
              await interaction.send("Oops! You ran out of tries. You'll get it next time!")
        else:
          self.emoji = self.view.squares[id_list.index(self.custom_id)]
          await interaction.response.edit_message(content="Ready!", view=view)
        
        
      
class Squares(nextcord.ui.View):
  def __init__(self, squares, startcounter = 0, incorrect_tries = 0):
    self.squares = squares
    self.startcounter = startcounter
    self.incorrect_tries = incorrect_tries
    super().__init__()
    
    rowtracker = 0
    i = 0
    while i <= len(self.squares) - 1:
      if i % 3 == 0:
        rowtracker += 1
      self.add_item(Square(rowtracker, self.squares[i]))
      i += 1
  
      
class Frivolity(commands.Cog):
  def __init__(self, client):
    self.client = client
  @nextcord.slash_command()
  async def frivolity(self, interaction: nextcord.Interaction):
    pass
  @frivolity.subcommand()
  async def xkcd(self, interaction: nextcord.Interaction, comic_number: int = nextcord.SlashOption(description="XKCD comic number to return.", required=False)):
    """Sends the current xkcd comic link or specified number."""
    if comic_number == None:
      setcomic = xkcdhelper.XKCDCOMIC()
      comic = setcomic.getLatestComic()
      
      
      mytext = comic[3]
      myurl = comic[2]
      embed = nextcord.Embed(
        title = f'**Comic Number {comic[4]}: {comic[0]}**',
        description = mytext,
      )
      embed.set_image(url = myurl)
      
      await interaction.send(embed = embed)
    else:
      setcomic = xkcdhelper.XKCDCOMIC()
      comic = setcomic.getComic(number = int(comic_number))
      myurl = comic[2]
      mytext = comic[3]
      embed = nextcord.Embed(
        title = f"**Comic Number {comic[4]}: {comic[0]}**",
        description = mytext,
        )
      embed.set_image(url = myurl)
      await interaction.send(embed = embed)  
  

  @frivolity.subcommand()
  async def quiz(self, interaction: nextcord.Interaction):
    """Answer a quiz question to recieve stars."""
    if (str(interaction.user.id) in db and 'lastquiz' not in db[str(interaction.user.id)]):
      await interaction.channel.send("We're updating some things on our end. Please standby...")
      db[str(interaction.user.id)]['lastquiz'] = str(datetime.datetime.utcnow())
      await interaction.channel.send("Thanks for waiting!")
    elif str(interaction.user.id) not in db:
      await interaction.channel.send("We're updating some things on our end. Please standby...")
      db[str(interaction.user.id)] = {}
      db[str(interaction.user.id)]['lastquiz'] = str(datetime.datetime.utcnow())
      await interaction.channel.send("Thanks for waiting!")
    else:
      if timehelper.getdifference(db[str(interaction.user.id)]['lastquiz']) < 600:
        await interaction.send("Please try again later.", ephemeral = True)
        return
      else:
        db[str(interaction.user.id)]['lastquiz'] = str(datetime.datetime.utcnow())
    interface_object = quiz.Quiz(quiz.questions).sendquiz()
    view = QuizView(interface_object[1], interface_object[2])
    message = await interaction.send(content=":star: Answer the following quiz question in 15 seconds to get 15 stars. :star:", embed=interface_object[0], view=view)
    await asyncio.sleep(18)
    if view.isDisabled == True and view.isActive == True:
      await message.edit(content="Out of time!", embed=interface_object[0], view=view)
    else:
      return
  
  
    
    
  
  @frivolity.subcommand()
  async def dadjoke(self, interaction: nextcord.Interaction):
    """Sends a random dadjoke."""
    dadjoke = Dadjoke()
    await interaction.send(dadjoke.joke)
    

  
  @frivolity.subcommand()
  async def guesstheword(self, interaction: nextcord.Interaction):
    """Word guessing game."""
    
    await interaction.send("Try to unscramble the word:")
    scoreCounter = 0
    while scoreCounter <= 100:
      correctWord = choice(wordsolver.wordList)
      scrambleList = []
      for c in correctWord:
        scrambleList.append(c)
      shuffle(scrambleList)
      returnWord = ""
      for x in scrambleList:
        returnWord += x
  
      def check(m):

        if (m.author == interaction.user and m.channel == interaction.channel) and (len(m.content) == 6 or len(m.content) == 5):
        
          def searchWord():
            for x in scrambleList:
              if x in m.content.lower():
                pass
              else:
                raise ValueError
            return True
          
          wordToCheck = TextBlob(m.content.lower())
          copyWord = m.content.lower()   
          if (wordToCheck.correct() == copyWord and searchWord()) or copyWord == correctWord:
            raise TypeError
          else:
            raise ValueError
        else:
          pass
      
      embed = nextcord.Embed(
        title = f"Score: {scoreCounter}",
        description = returnWord
      )
      embed.set_footer(text = "Try to unscramble the word in 15 seconds.")
      embed.set_author(name = interaction.user.name, icon_url = str(interaction.user.display_avatar.url))
      await interaction.channel.send(embed = embed)
  
      try:
        await self.client.wait_for('message', timeout = 15.0, check = check)
      except TypeError:
        await interaction.channel.send("Correct!")
        scoreCounter += 1
      except ValueError:
        await interaction.channel.send(f"Sorry, the scrambled word was **{correctWord}**.")
        await interaction.channel.send(f":tada: Your final score was **{scoreCounter}**. Great job! :tada:")
        return
      except asyncio.TimeoutError:
        await interaction.channel.send(f"Oops! you ran out of time. The scrambled word was **{correctWord}**.\n\n:tada:Your final score was **{scoreCounter}**. Great job! :tada:")
        return
    await interaction.channel.send(":tada:Amazing! Your final score was 100!:tada:")
    return

  @frivolity.subcommand()
  async def match(self, interaction:nextcord.Interaction, difficulty: int=nextcord.SlashOption(required="False", description="Number of different items to choose. Defaults to 4.", default=4)):
    """Match the corresponding colored squares."""
    characterList = [
      "⛰️",
      "🏈",
      "⌨️",
      "🥕",
      "🏜️",
      "⛲",
    ]
    board = []
    if difficulty != None and difficulty > 6:
      await interaction.send("Sorry, this level isn't available yet. Please choose a lower number.")
      return
    else:
      i = 1
      while i<= difficulty:
        shuffle(characterList)
        board.append(characterList[-1])
        board.append(characterList[-1])
        del characterList[-1]
        i += 1
        
    shuffle(board)
    j = 0
    while j <= len(board) - 1:
      if board[j] == '':
        del board[j]
      j += 1
    newBoard = Squares(board)
    await interaction.send("Press any square to start: ", view=newBoard)
      

  
  
  
      
      
    

    


  


def setup(client):
	client.add_cog(Frivolity(client))