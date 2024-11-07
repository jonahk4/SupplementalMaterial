from replit import db
import datetime

def add_user_value(user, balance):
  if user in db:
   raise TypeError
  else:
    db[user] = {"balance": balance, "lastrewarddaily": 0, "lastquizm": 0, "lastquizh": 0}
  
def addquiz(user):
  if user in db:
    db[user]["lastquizm"] = None
    db[user]["lastquizh"] = None
  elif user not in db:
    db[user] = {"lastquizm": 0, "lastquizh": 0, "balance": 0, "lastrewarddaily": 0}
def return_current_value(user):
  try:
    value = db[user]["balance"]
    return value
  except KeyError:
    raise TypeError

def returnuser(user):
  return db[user]["balance"]

def addbalance(user, amount):
  db[user] = {"balance": int(amount), "lastrewarddaily": None}
  
def returnlastdaily(user):
  try:
    return db[user]["lastdaily"]
  except KeyError:
    raise SyntaxError

def recordlastdaily(user):
  try:
    x = str(datetime.datetime.utcnow())
    returnstringTwo = ""
    returndatelist = []
    counter = 1
    while counter <= 10:
      for y in x:
        returndatelist.append(y)
        counter += 1
    for z in returndatelist:
      returnstringTwo += z
    returnstring = returnstringTwo.split("-")
    returnstringOne = returnstring[2]
    returnstringthree = returnstringOne.split(" ")
    db[user]["lastdaily"] = returnstringthree[0]
  except KeyError:
    x = str(datetime.datetime.utcnow())
    returnstringTwo = ""
    returndatelist = []
    counter = 1
    while counter <= 10:
      for y in x:
        returndatelist.append(y)
        counter += 1
    for z in returndatelist:
      returnstringTwo += z
    returnstring = returnstringTwo.split("-")
    returnstringOne = returnstring[2]
    returnstringthree = returnstringOne.split(" ")
    db[user]["lastdaily"] = returnstringthree[0]

  

def returnlastquiz(user):
  try:
    return db[user]["lastquiz"]
  except KeyError:
    raise SyntaxError

def recordlastquiz(user2):
  try:
    x = str(datetime.datetime.utcnow())
    returnstringTwo = ""
    returndatelist = []
    counter = 1
    while counter <= 10:
      for y in x:
        returndatelist.append(y)
        counter += 1
    for z in returndatelist:
      returnstringTwo += z
    returnstring = returnstringTwo.split(" ")
    returnstringOne = returnstring[1]
    returnstringthree = returnstringOne.split(":")
    db[user2]["lastquizm"] = returnstringthree[1]
    db[user2]["lastquizh"] = returnstringthree[0]
  except KeyError:
    x = str(datetime.datetime.utcnow())
    returnstringTwo = ""
    returndatelist = []
    counter = 1
    while counter <= 10:
      for y in x:
        returndatelist.append(y)
        counter += 1
    for z in returndatelist:
      returnstringTwo += z
    returnstring = returnstringTwo.split(" ")
    returnstringOne = returnstring[1]
    returnstringthree = returnstringOne.split(":")
    db[user2]["lastquizm"] = returnstringthree[1]
    db[user2]["lastquizh"] = returnstringthree[0]

def waittimedaily(user):
  try:
    x = str(datetime.datetime.utcnow())
    y = x.split("-")
    z = y[2]
    d = z.split(" ")
    m = d[0]
    if int(m) - int(db[user]["lastdaily"]) != 0:
      return True
    else:
      return False
  except KeyError:
    return True

def waittimequiz(user):
  try:
    x = str(datetime.datetime.utcnow())
    y = x.split(" ")
    z = y[1]
    d = z.split(":")
    m = d[1]
    l = d[0]
    string1 = int(m)/60
    string2 = int(db[user]["lastquizm"])/60
    string3 = float(string2) - float(string1)
    if abs(string3) >= 0.1 or int(l) != int(db[user]["lastquizh"]):
      return True
    else:
      return False
  except KeyError:
    return True



def returnvalues(user):
  return db[user].keys()
def update_user_value(user, addition):
  if user in db:
    original_balance = db[user]["balance"]
    newBalance = original_balance + addition
    db[user]["balance"] = newBalance
  else:
    db[user]= {"balance": addition}

def reset_balance(user):
  db[user] = 0

def delete_user(user):
  del db[user]

def gift(original, giftuser, amount):
  if amount <= db[original]["balance"] and giftuser in db:
    db[original]["balance"] -= amount
    db[giftuser]["balance"] += amount
  elif amount <= db[original]["balance"] and giftuser not in db:
    db[original]["balance"] -= amount
    db[giftuser]["balance"] += amount
  elif amount > db[original]["balance"]:
    raise ValueError
  
def checkusers():
  return db.keys()
  
    
