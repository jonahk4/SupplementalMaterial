import nextcord
from nextcord.ext import commands
import asyncio
from system import calc
import math
from system.systemofequations import SystemOfEquations
from replit import db
import datetime
import re
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

class CalculatorButtonNumber(nextcord.ui.Button):
  def __init__(self, setlabel, setrow):
    self.setlabel = setlabel
    self.setrow = setrow
    super().__init__(style=nextcord.ButtonStyle.secondary, label=setlabel, row = setrow)
  async def callback(self, interaction: nextcord.Interaction):
    self.view.currentstate += self.label
    await interaction.response.edit_message(content = self.view.currentstate, view=self.view)
  
    
class CalculatorButtonFunction(nextcord.ui.Button):
  def __init__(self, setlabel, setrow):
    self.setlabel = setlabel
    self.setrow = setrow
    super().__init__(style=nextcord.ButtonStyle.red, label=setlabel, row = setrow)
  async def callback(self, interaction: nextcord.Interaction):
    if self.label == "delete":
      self.view.currentstate = self.view.currentstate[:-1]
      await interaction.response.edit_message(content = self.view.currentstate, view=self.view)
    else:
      self.view.currentstate += self.label + "("
      await interaction.response.edit_message(content = self.view.currentstate, view=self.view)
      
class CalculatorButtonOperation(nextcord.ui.Button):
  def __init__(self, setlabel, setrow):
    self.setlabel = setlabel
    super().__init__(style=nextcord.ButtonStyle.green, label=setlabel, row=setrow)
  async def callback(self, interaction: nextcord.Interaction):
      self.view.currentstate += self.label
      await interaction.response.edit_message(content = self.view.currentstate, view=self.view)
class CalculatorReturnResult(nextcord.ui.Button):
  def __init__(self, setlabel, setrow):
    self.setlabel = setlabel
    self.setrow = setrow
    super().__init__(style=nextcord.ButtonStyle.blurple, label=setlabel, row = setrow)
  async def callback(self, interaction: nextcord.Interaction):
    expression = self.view.currentstate.split(":")
    try:
      result = N(parse_expr(expression[1], transformations="all"))
      await interaction.response.edit_message(content = result, view=self.view)
    except:
      await interaction.response.edit_message(content = "Error", view=self.view)
  
    

class MainCalculatorView(nextcord.ui.View):
  def __init__(self, currentstate, specialfunction):
    self.currentstate = currentstate
    self.specialfunction = specialfunction
    super().__init__()
    i = 0
    y = 0
    operations = ["+", "-", "*", "/", "(", ")"]
    while i < 10:
      if i % 3 == 0:
        y += 1
        self.add_item(CalculatorButtonNumber(str(i), y))
      else:
        self.add_item(CalculatorButtonNumber(str(i), y))
      i += 1
    i = 0
    otherfunctions = ["ln", "exp", "sinh", "cosh"]
    while i <= len(otherfunctions) - 1:
        self.add_item(CalculatorButtonFunction(otherfunctions[i], i))
        i += 1
    i = 1 
    
    while i <= len(operations) - 1 and i < 5:
        self.add_item(CalculatorButtonOperation(operations[i], i))
        i += 1
    
    while i <= len(operations) - 1:
      self.add_item(CalculatorButtonOperation(operations[i], 4))
      i += 1
    self.add_item(CalculatorButtonOperation(operations[0], 4))

    functions = ["sin", "cos", "tan", "delete"]
    i = 0
    while i <= len(functions) - 1:
      self.add_item(CalculatorButtonFunction(functions[i], 0))
      i += 1
    self.add_item(CalculatorReturnResult("enter", 4))
      
class Utilities(commands.Cog):
  def __init__(self,client):
    self.client = client
    
  @nextcord.slash_command()
  async def utilities(self, interaction: nextcord.Interaction):
    pass

  @utilities.subcommand()
  async def calc(self, interaction: nextcord.Interaction, expression: str = nextcord.SlashOption(description = "Expression to evaluate.", required=False, default=None)):
    """Calculator"""
    if expression != None:
      evaluateExpression = ""
      for x in expression:
        if x == "^":
          evaluateExpression += "**"
        else:
          evaluateExpression += x
      result = N(evaluateExpression)
      embed = nextcord.Embed(
        title = f"Input: {expression}",
        description = f"Result: {result}"
      )
      await interaction.send(embed = embed)  
    else:
      await interaction.send("Enter expression (Radian Mode):", view=MainCalculatorView("Enter expression (Radian Mode): ", ""))
  @utilities.subcommand()
  async def projectile(self,interaction: nextcord.Interaction,vinitial:float = nextcord.SlashOption(description = "Initial velocity (m/s)"), angle:float = nextcord.SlashOption(description = "Angle to horizontal in degrees")):
    """Calculates the range of a projectile launched at a given velocity and angle."""
    self.__vinitial = vinitial
    self.__angle = angle
    result1 = math.radians(angle)
    viy = math.sin(result1)
  
    viiy = viy * vinitial
    a = -9.8
    vfy = (-1) * viy
    vffy = vfy * vinitial
    t = (vffy - viiy)/a
    vix = math.cos(result1)
    viix = vix * vinitial
    vfx = math.cos(result1) 
    vffx = vfx * vinitial
    ans = ((viix + vffx)/2) * t
    finalans = ans * 3.3
    embed = nextcord.Embed(
      title = "Results: ",
      description = f"Angle of launch: {angle} degrees\nInitial Velocity: {vinitial}\nTotal Distance Traveled: {finalans} ft",
      colour = 0x10E6F1
    )
    await interaction.send(embed = embed)


  @utilities.subcommand()
  async def dna(self,interaction, sequence: str =  nextcord.SlashOption(description = "Sequence to return pairs.")):
    """Returns the DNA and RNA pairs of a given DNA sequence."""
    self.__sequence = sequence
    return_pair = []
    return_pairr = []
    
    for letter in sequence:
      if letter.lower() == "a":
        return_pair.append("T")
      if letter.lower() == "t":
        return_pair.append("A")
      if letter.lower() == "c":
        return_pair.append("G")
      if letter.lower() == "g":
        return_pair.append("C")
    for letter in sequence:
      if letter.lower() == "a":
        return_pairr.append("U")
      if letter.lower() == "t":
        return_pairr.append("A")
      if letter.lower() == "c":
        return_pairr.append("G")
      if letter.lower() == "g":
        return_pairr.append("C")
    embed = nextcord.Embed(
      title = "Result:",
      description = "`Base Pair DNA:` " + str(return_pair) + "\n\n" + "`mRNA:` " + str(return_pairr),
      colour = 0x10E6F1
    )
    await interaction.send(embed = embed)
  
  """@utilities.subcommand()
  async def changecoordinates(self, interaction: nextcord.Interaction, inputtype: nextcord.SlashOption(description="Coordinate system input", choices = {"cartesian": "cartesian", "polar":"polar", "spherical": "spherical", "cylindrical": "cylindrical"}), outputType:nextcord.SlashOption(description="Coordinate system input", choices = {"cartesian": "cartesian", "polar":"polar", "spherical": "spherical", "cylindrical": "cylindrical"}), startCoordinates:str = nextcord.SlashOption("Starting coordinates")):
    "\""Change between two given coordinate systems."\""
    await interaction.send("This command is still under construction, please try again later!")"""
  @utilities.subcommand()
  async def setreminder(self, interaction: nextcord.Interaction,message:str = nextcord.SlashOption(description = "Reminder message."),timeduration:int = nextcord.SlashOption(description = "Time to wait before sending message"), alert:str = nextcord.SlashOption(description="Should Polaris mention you in the message sent?", choices={"y":"y", "n":"n"})):
    """Sends a message between a given time interval."""
    
    if timeduration < 60:
      await interaction.send("Please choose a time interval of at least 60 seconds.", ephemeral = True)
     
    elif timeduration >= 60 and timeduration < 86401:
      await interaction.send("Automated message added.")
      await asyncio.sleep(timeduration)
      if alert == "y":
        await interaction.channel.send(interaction.user.mention)
      embed = nextcord.Embed(
        title = f"{interaction.user} set a reminder.",
        description = f"Message: {message}"
      )
      embed.set_footer(text=f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
      await interaction.channel.send(embed=embed)
    else:
      await interaction.send("Please choose a smaller time interval.", ephemeral = True)

      
    
    
    
  
  @utilities.subcommand()
  async def ping(self, interaction: nextcord.Interaction):
    """Returns response delay from Discord client in miliseconds."""
    latency =  round((self.client.latency*1000), 2)
    embed=nextcord.Embed(
      title="Bot Latency :globe_with_meridians:",
      description = f"{latency} ms\n\nThis is a measure of the delay of data transfer to the bot when you use a command."
    )
    embed.set_footer(text=f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
    await interaction.send(embed=embed)
    
  @utilities.subcommand()
  async def solvesystem(self, interaction: nextcord.Interaction, equations: str = nextcord.SlashOption(description = "system of equations")):
    """Solve a system of two or three equations."""
    equationSet = SystemOfEquations(equations)
    try:
      result = str(equationSet.solvesystem())
      if result == "[]":
        result = "No solutions"
      embed = nextcord.Embed(
        title = f"Input: {equations}",
        description = f"Output: ```{result}```"
      )
      embed.set_footer(text = f"Server ID: {interaction.guild.id} | {datetime.datetime.utcnow()}")
      await interaction.send(embed = embed)
    except:
      await interaction.send("Sorry, an error occured while trying to solve this system. Please contact us at https://support.polarisbot.com if you believe this is a bug.")
  

    
  @utilities.subcommand()
  async def quadratic(self, interaction: nextcord.Interaction, equation: str = nextcord.SlashOption(description = "Function of x (degree 2)")):
    """Finds the roots of a given quadratic equation. Answer(s) must be a real number."""
    #a
    if equation[-1] == "2" and equation[-2] == "^":
      equation += "+0x+0"
    userInput = []
    if equation[0] == "x":
      a=1
    elif equation[0] == "-" and equation[1] == "x":
      a=-1
    else:
      termOne = equation.split("x^2")
      a=termOne[0]
    #b
    termOne = equation.split("x^2")
    operationList = ["+", "-"]
    if termOne[1][0] in operationList and termOne[1][1] == "x":
      b=termOne[1][0] + "1"
    else:
      if "x" not in termOne[1]:
        b=0
      else:
        termTwo = termOne[1].split("x")
        b=termTwo[0]
    #c
    iterator = -1
    cTermList = []
    
    while equation[iterator+1] not in operationList and equation[iterator] != "x":
      cTermList.append(equation[iterator])
      iterator -= 1
    cTermList.reverse()
    combineTermCounter = 0
    c=""
    while combineTermCounter < len(cTermList):
      c += str(cTermList[combineTermCounter])
      combineTermCounter += 1
    if c=="":
      c=0
  
    a=float(a)
    b=float(b)
    c=float(c)
    
    d = (b**2) - (4*a*c)
    if d < 0:
      d1 = abs(d)
      r11 = (-b/(2*a))
      r1 = f"{round(r11, 2)}+{round((math.sqrt(d1))/(2*a),2)}i"
      r12 = (-b/(2*a))
      r2 = f"{round(r12,2)}-{round(math.sqrt(d1)/(2*a),2)}i"
    elif d >= 0:
      r11 = (-b+math.sqrt(d))/(2*a)
      r1 = f"{round(r11,2)}"
      r12 = (-b-math.sqrt(d))/(2*a)
      r2 = f"{round(r12,2)}"

    embed = nextcord.Embed(
      title=f"Input: Roots of f(x)={equation}",
      description=f"Output: x={r1} or x={r2}"
    )
    embed.set_footer(text=f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
    await interaction.send(embed=embed)
    
  @utilities.subcommand()
  async def convertangle(self, interaction: nextcord.Interaction, start: str=nextcord.SlashOption(name="from", description="Starting unit", choices = {"rad":"rad", "deg": "deg"}), to: str=nextcord.SlashOption(description="Ending unit", choices={"rad":"rad", "deg": "deg"}), value:float = nextcord.SlashOption(description="Angle to convert")):
    """Converts a given angle in degrees to radians."""
    if (start == "deg" and to == "rad"):
      returnValue = math.radians(value)
    elif (start == "rad" and to == "deg"):
      returnValue = math.degrees(value)
    else:
      returnValue = value
    embed = nextcord.Embed(
      title = f"Input: {value} {start} to {to}",
      description = f"Result: {returnValue} {to}"
    )
    embed.set_footer(text=f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
    await interaction.send(embed = embed)
    
  @utilities.subcommand()
  async def converttemperature(self, interaction: nextcord.Interaction, number: float = nextcord.SlashOption(description="quantity of given unit"), start: str = nextcord.SlashOption(name="from", description="Units to convert from.", choices={"degrees Fahrenheit": "degrees Fahrenheit", "degrees Celsius": "degrees Celsius", "Kelvin": "Kelvin"}), to: str=nextcord.SlashOption(description="Units to convert to.", choices={"degrees Fahrenheit": "degrees Fahrenheit", "degrees Celsius": "degrees Celsius", "Kelvin": "Kelvin"})):
    """Convert between common units of temperature."""
    if start == "degrees Celsius":
      if to == "degrees Fahrenheit":
        c = number
        returnNumber = (1.8*c) + 32
        content = f"Start with conversion: F=1.8C+32\n\nPlug in known values\nF=1.8({c}) + 32\nF={returnNumber}°F"
      elif to =="Kelvin":
        c = number
        returnNumber = 273 + c
        content = f"Start with conversion: K=273+C\n\nPlug in known values\nK=273+({c})\nK={returnNumber}K"
    elif start == "degrees Fahrenheit":
      if to == "degrees Celsius":
        f = number
        returnNumber = round((((f - 32)*5)/9), 2)
        content = f"Start with conversion F=1.8C+32\n\nRearrange to solve for C\nC=(F-32)/1.8\n\nPlug in known values\nC=(({f})-32)/1.8\nC={returnNumber}°C"
      elif to == "Kelvin":
        f = number
        returnNumber = round((((((f-32)*5)/9) + 273)), 2)
        content = f"Start with conversion F=1.8C+32\n\nRearrange to solve for C\nC=(F-32)/1.8\n\nUse conversion K=273+C and substitute for C.\n\nK=((F-32)/1.8)+273\n\nPlug in known values\nK=((({f})-32)/1.8)+273\nK={returnNumber}K"
    elif start == "Kelvin":
      if to == "degrees Fahrenheit":
        k = number
        returnNumber = round((((k-273) * 1.8) + 32), 2)
        content = f"Start with conversion K=273+C\n\nRearrange to solve for C\nC=K-273\n\nUse conversion factor F=1.8C+32 and substitute for C.\nF=1.8(K-273)+32\n\nSubstitute in known values\nF=1.8(({k})-273)+32\nF={returnNumber}°F"
      elif to == "degrees Celsius":
        k = number
        returnNumber = round((k-273), 2)
        content = f"Start with conversion K=273+C\n\nRearrange to solve for C\nC=K-273\n\nPlug in known values\nC=({k})-273\nC={returnNumber}°C"
    embed = nextcord.Embed(
      title = f"Input: {number} {start} to {to}",
      description = content
    )
    embed.set_footer(text = f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
    await interaction.send(embed = embed)
    
  @utilities.subcommand()
  async def dotproduct(self, interaction: nextcord.Interaction, v1:str = nextcord.SlashOption(description = "vector A"), v2:str=nextcord.SlashOption(description="vector B")):
    """Take the dot product between two vectors."""
    a=[]
    b=[]
    returnResult = 0
    for x in v1:
      if re.fullmatch('\d', x):
        a.append(x)
      else:
        pass
    for y in v2:
      if re.fullmatch('\d', y):
        b.append(y)
      else:
        pass
    if len(a) != len(b):
      await interaction.send(f"Invalid operation between {str(a)} and {str(b)}")
      return
    i=0
    while i<=len(a) - 1:
      returnResult += (float(a[i])*float(b[i]))
      i+=1
    embed = nextcord.Embed(
      title = f"Input: {v1}•{v2}",
      description = f"Result: {round(returnResult, 2)}"
    )
    embed.set_footer(text=f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
    await interaction.send(embed=embed)
    return
      
  @utilities.subcommand()
  async def convertcoordinates(self, interaction: nextcord.Interaction, expression:str = nextcord.SlashOption(description="Coordinates to convert."), start:str=nextcord.SlashOption(name="from", description="Starting coordinate system", choices={"cartesian":"cartesian", "polar":"polar"}), to:str=nextcord.SlashOption(description="New coordinate system", choices={"cartesian":"cartesian", "polar":"polar"})):
    """Convert between cartesian and polar coordinate systems."""
    if start == "cartesian" and to == "polar":
      formatCoordinates = expression.split(",")
      xCoordToFormat = formatCoordinates[0]
      yCoordToFormat = formatCoordinates[1]
      xCoordString = xCoordToFormat.split("(")
      x = float(xCoordString[1])
      yCoordString = yCoordToFormat.split(")")
      y = float(yCoordString[0])
  
      r = round(math.sqrt(((x**2)+(y**2))), 2)
      if x == 0 and y > 0:
        theta = round((math.pi/2), 2)
      elif x == 0 and y < 0:
        theta = round(((3*math.pi)/2), 2)
      elif y == 0 and x > 0:
        theta = 0
      elif y == 0 and x < 0:
        theta = round((-1*math.pi), 2)
      else:
        theta = round(math.atan((y/x)), 2)
      embed = nextcord.Embed(
        title = f"{expression} to polar coordinates",
        description = f"Result: (r,θ) --> ({r},{theta})\nAlternate form: {r}(cos({theta})+sin({theta}))"
      )
      embed.set_footer(text=f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
      await interaction.send(embed=embed)

    elif start == "polar" and to == "cartesian":
      formatCoordinates = expression.split(",")
      rCoordToFormat = formatCoordinates[0]
      thetaCoordToFormat = formatCoordinates[1]
      rCoordString = rCoordToFormat.split("(")
      r = float(rCoordString[1])
      thetaCoordString = thetaCoordToFormat.split(")")
      theta = float(thetaCoordString[0])

      x = round((r * math.cos(theta)), 2)
      y = round((r * math.sin(theta)), 2)

      embed = nextcord.Embed(
        title = f"{expression} to cartesian coordinates",
        description = f"Result: ({x},{y})\n\nTheta was assumed to be in radians."
      )
      embed.set_footer(text=f"{datetime.datetime.utcnow()} | Server ID: {interaction.guild.id}")
      await interaction.send(embed=embed)

    

    
  
      
      
      
  

  



    

def setup(client):
  client.add_cog(Utilities(client))