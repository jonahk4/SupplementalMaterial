import nextcord
from nextcord.ext import commands
import asyncio
from random import randint, choice, shuffle
from tictactoe import tictactoebot
from replit import db
import os


    
def winningconditions(boardlist):
  if boardlist[0] != 0:
    if boardlist[0] == boardlist[1] and boardlist[1] == boardlist[2]:
      return True
  if boardlist[3] != 0:
    if boardlist[3] == boardlist[4] == boardlist[5]:
      return True
  if boardlist[6] != 0:
    if boardlist[6] == boardlist[7] == boardlist[8]:
      return True
  if boardlist[0] != 0:
    if boardlist[0] == boardlist[3] == boardlist[6]:
      return True
  if boardlist[1] != 0:
    if boardlist[1] == boardlist[4] == boardlist[7]:
      return True
  if boardlist[2] != 0:
    if boardlist[2] == boardlist[5] == boardlist[8]:
      return True
  if boardlist[0] != 0:
    if boardlist[0] == boardlist[4] == boardlist[8]:
      return True
  if boardlist[2] != 0:
    if boardlist[2] == boardlist[4] == boardlist[6]:
      return True

def tieconditions(boardlist):
  if boardlist[0] != 0:
    if boardlist[0] == boardlist[1] and boardlist[3] == boardlist[4]:
      if boardlist[6] == boardlist[7]:
        return True
  elif boardlist[1] != 0:
    if boardlist[1] == boardlist[2] and boardlist[4] == boardlist[5]:
      if boardlist[7] == boardlist[8]:
        return True
  elif boardlist[3] != 0:
    if boardlist[0] == boardlist[3] and boardlist[1] == boardlist[4]:
      if boardlist[2] == boardlist[5]:
        return True
  elif boardlist[4] != 0:
    if boardlist[0] == boardlist[4] and boardlist[2] == boardlist[4]:
      return True
  elif boardlist[6] != 0:
    if boardlist[6] == boardlist[4] and boardlist[8] == boardlist[4]:
      return True
  elif boardlist == [1, 2, 2, 2, 1, 1, 0, 1, 2]:
    return True
  elif boardlist == [1, 1, 2, 2, 1, 1, 0, 2, 2]:
    return True
  elif boardlist == [2, 1, 2, 1, 1, 2, 1, 2, 1]:
    return True
  elif boardlist == [1, 1, 2, 2, 1, 1, 1, 2, 2]:
    return True
  elif boardlist == [2, 1, 2, 1, 1, 2, 0, 2, 1]:
    return True


class TicTacToe(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.__p1 = None
    self.__p2 = None

  @nextcord.slash_command()
  async def tictactoe(interaction: nextcord.Interaction):
    pass
  @tictactoe.subcommand()
  async def play(self, interaction: nextcord.Interaction, p1:nextcord.Member = nextcord.SlashOption(description = "Player 1"), p2:nextcord.Member = nextcord.SlashOption(description = "Player 2")):
    """Play tictactoe with another member of the server."""
    
    playerList = [str(p1), str(p2)]
    shuffle(playerList)
    player1 = playerList[0]
    player2 = playerList[1]
    #Print board
    if p1 == p2:
      await interaction.send("Please play with another player other than yourself.", ephemeral = True)
      return

    if p1.bot or p2.bot:
      await interaction.send("Please play with another player other than a bot.", ephemeral = True)
      return
    message = ""
    boardlist = [0, 0, 0, 0, 0, 0, 0, 0, 0]
   
    
    await interaction.send("Please wait...")
    await interaction.channel.send(":one::two::three:\n:four::five::six:\n:seven::eight::nine:")
    await interaction.channel.send("Please type the number of the square you would like to select to start.")
    #Makes board depending on square value input.
    def makeboard(squareValues):
      returnString = ""
      linecount = 0
      splitlist = [3, 6]
      for v in squareValues:
        if linecount in splitlist:
          returnString += "\n"
        if v == 0:
          returnString += ":white_large_square:"
          linecount += 1
        elif v == 1:
          returnString += ":red_square:"
          linecount += 1
        elif v == 2:
          returnString += ":blue_square:"
          linecount += 1
      return returnString

    #game_logic
    gamecounter = 0
    p1turns = [0, 2, 4, 6, 8]
    p2turns = [1, 3, 5, 7]
    while gamecounter <= 9:
      startboard = makeboard(boardlist)
      await interaction.channel.send(startboard)
      if gamecounter in p1turns:
        await interaction.channel.send(f"It is {player1}'s turn. Please choose a square.")
        
        def check(m):
          if str(m.author) == player1:
            if gamecounter in p1turns:
              index = int(m.content) - 1
              if boardlist[index] == 0:
                boardlist[index] = 1
                if winningconditions(boardlist = boardlist):
                  raise SyntaxError
                elif tieconditions(boardlist = boardlist):
                  raise NameError
                else:
                  raise ValueError
              else:
                raise TypeError
            else:
              raise TypeError
          else:
            pass
        try:
          await self.client.wait_for('message', timeout = 15.0, check = check)
        except ValueError:
          gamecounter += 1
        except TypeError:
          await interaction.channel.send("Invalid square specified.")
        except asyncio.TimeoutError:
          await interaction.reply("Game has been stopped due to inactivity.")
        except SyntaxError:
          await interaction.channel.send(makeboard(boardlist))
          await interaction.channel.send(f":tada: {player1} wins!")
          return
        except NameError:
          await interaction.channel.send(makeboard(boardlist))
          await interaction.channel.send("It's a tie!")
          return
      elif gamecounter in p2turns:
        await interaction.channel.send(f"It is {player2}'s turn. Please choose a square.")
        def check(m):
          if str(m.author) == player2:
            if gamecounter in p2turns:
              index = int(m.content) - 1
              if boardlist[index] == 0:
                boardlist[index] = 2
                if winningconditions(boardlist = boardlist):
                  raise SyntaxError
                elif tieconditions(boardlist = boardlist):
                  raise NameError
                else:
                  raise ValueError
              else:
                raise TypeError
            else:
              raise TypeError
          else:
            pass
        try:
          await self.client.wait_for('message', timeout = 15.0, check = check)
        except ValueError:
          gamecounter += 1
        except TypeError:
          await interaction.channel.send("Invalid square specified.")
        except asyncio.TimeoutError:
          await interaction.channel.send("Game has been stopped due to inactivity.")
        except SyntaxError:
          await interaction.channel.send(makeboard(boardlist))
          await interaction.channel.send(f":tada: {player1} wins!")
          return
        except NameError:
          await interaction.channel.send(makeboard(boardlist))
          await interaction.channel.send("It's a tie!")
          return
  
        
    
    
    
    

    
  @tictactoe.subcommand()
  async def playwithbot(self, interaction: nextcord.Interaction):
    """Play tictactoe with Polaris"""
    await interaction.send("Please wait...")
    await interaction.channel.send("Ready to play! Hint: Less than nine turns are needed to win.")
    await interaction.channel.send(":one::two::three:\n:four::five::six:\n:seven::eight::nine:")
    await interaction.channel.send("Please type the number of the square you would like to select to start.")
    def setupboard(boardlist):
      returnString = ""
      linecount = 0
      splitlist = [3, 6]
      for v in boardlist:
        if linecount in splitlist:
          returnString += "\n"
        if v == 0:
          returnString += ":white_large_square:"
          linecount += 1
        elif v == 1:
          returnString += ":red_square:"
          linecount += 1
        elif v == 2:
          returnString += ":blue_square:"
          linecount += 1
      return returnString
        
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    playerlist = [[str(interaction.user.name), "Polaris"]]
    players = [item for item in playerlist for i in range(8)]
    playerlistone = [p for x in players for p in x]

    turncounter = 0
    p1turns = [0, 2, 4, 6, 8]
    p2turns = [1, 3, 5, 7]
    def check(m):
      if m.author == interaction.user:
        if len(str(m.content)) == 1:
          if board[int(m.content) - 1] == 0 and turncounter in p1turns:
            board[int(m.content) - 1] = 1
            if tieconditions(boardlist = board):
              raise TypeError
            elif winningconditions(boardlist = board):
              raise NameError
            else:
              raise ValueError 
          else:
            raise SyntaxError
        else:
          pass
      else:
        pass
    counterTwo = 0
    await interaction.channel.send(setupboard(board))
    while turncounter <= 8:
      await interaction.channel.send(f"Current turn: :red_square: {playerlistone[counterTwo]}")
      try:
        await self.client.wait_for('message', timeout = 600.0, check = check)
      except TypeError:
        await interaction.channel.send("It's a tie!")
        return
      except NameError:
        await interaction.channel.send(f":tada: {interaction.user.mention} wins! :tada:")
        return
      except SyntaxError:
        await interaction.channel.send("Invalid square specified.")
      except asyncio.TimeoutError:
        await interaction.channel.send(f"{interaction.user.mention} Game has been stopped due to inactivity.")
        return
      except ValueError:
        turncounter += 1
        counterTwo += 1
        await interaction.channel.send(setupboard(board))
        botchoice = tictactoebot.boardSearch(board = board)
        board[botchoice] = 2
        if board.count(0) == 1:
          await interaction.channel.send(f"Polaris chose square {botchoice + 1}.\nPlease wait...")
          await interaction.channel.send(setupboard(board))
          await interaction.channel.send("It's a tie!")
          return
        await interaction.channel.send(setupboard(board))
        await interaction.channel.send(f"Polaris chose square {botchoice + 1}.\nPlease wait...")
        if tieconditions(boardlist = board):
          await interaction.channel.send("It's a tie!")
          return
        elif winningconditions(boardlist = board):
          await interaction.channel.send(":tada: Polaris wins! :tada:")
          return
        else:
          turncounter += 1
          counterTwo += 1
        
      
     
  
    
def setup(client):
	client.add_cog(TicTacToe(client))