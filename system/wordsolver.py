wordList = ["heart", "trait", "crate", "crash", "horse", "angle", "force", "speed", "light", "smash", "prose", "class", "slice", "phone", "sharp", "violin", "piano", "viola", "cello", "trash", "stand", "liver", "slime", "lemon", "apple", "seven", "globe", "table", "spoon", "toast", "train", "trail", "break", "snack", "trick", "press", "touch", "smell", "sight", "roads", "prank", "baker", "meter", "trace", "laden", "front", "apall", "bowel", "crane", "drive", "enter", "float", "hands", "juice", "koala", "locks", "notes", "order", "parks", "quest", "rests", "score", "under", "words", "shore", "earth", "stone", "spark", "spore", "depth", "trail", "ships", "scale", "grate", "music", "lever", "hills", "still", "panic", "quiet", "zebra", "tiger", "birds", "slack", "lacks", "parks", "chair", "melon", "orange", "field", "print", "power", "lines", "coarse", "lanes", "nails", "miles", "limes", "great", "brake", "paint", "slate", "parts", "floor", "shape", "space", "spans", "water", "cloud", "stars", "orbit", "start", "tarts", "carts", "search", "reach", "chair", "hairs", "share", "bench", "still", "lilts", "tills", "panda", "index", "edits", "tides", "slide", "ropes", "chord", "nodes", "paths", "space", "trace", "every", "bring", "tried", "pores", "state", "taste", "retry", "speak", "table", "field", "flaps", "after", "diver", "crest", "learn", "bloom", "plume", "chart", "wheel", "climb", "cycle", "store", "rotor", "motor", "react", "branch", "bleat"]
from random import choice, randint


def creategame():
  wordChoice = choice(wordList)
  numberList = []
  counter = 0
  while counter <= len(wordChoice) - 1:
    number = randint(0, 4)
    if number not in numberList:
      numberList.append(number)
    else:
      counter -= 1
    counter += 1


  scrambleList = []
  for x in wordChoice:
    scrambleList.append(x)

  counter = 0
  while counter <= len(scrambleList) - 1:
    newIndex = numberList[counter]
    olditem = scrambleList[counter]
    newItem = scrambleList[newIndex]
    scrambleList[counter] = newItem
    scrambleList[newIndex] = olditem
    counter += 1
  correctString = ""
  for x in wordChoice:
    correctString += x
  scrambledString = ""
  for x in scrambleList:
    scrambledString += x
  if scrambledString == correctString or scrambledString in wordList:
    wordChoiceOne = choice(wordList)
    wordChoiceList = []
    for y in wordChoiceOne:
      wordChoiceList.append(y)
    
    wordChoiceList.reverse()
    
    scrambledStringTwo = ""
    for z in wordChoiceList:
      scrambledStringTwo += z
    return [wordChoiceOne, scrambledStringTwo]
  else:  
    return [correctString, scrambledString] 
