def boardSearch(board):
  #across
  h1 = []
  h2 = []
  h3 = []
  i = 0
  while i < len(board):
    if i <=2:
      h1.append(board[i])
    elif i>2 and i<=5:
      h2.append(board[i])
    elif i>5:
      h3.append(board[i])
    i+=1
  
  hb=[h1,h2,h3]
  for row in hb:
    counter = 0
    for c in row:
      if c == 1:
        counter += 1
      if counter == 2:
        try:
          index = row.index(0)
          if row == hb[0]:
            return index
          elif row == hb[1]:
            return index+3
          elif row == hb[2]:
            return index+6
        except: 
          pass

  #vertical
  v1 = [0, 3, 6]
  v2 = [1, 4, 7]
  v3 = [2, 5, 8]
  v1c = [0, 3, 6]
  v2c = [1, 4, 7]
  v3c = [2, 5, 8]
  i = 0
  while i < len(board):
    if i in v1c:
      index = v1c.index(i)
      v1[index] = board[i]
    elif i in v2c:
      index = v2c.index(i)
      v2[index] = board[i]
    elif i in v3c:
      index = v3c.index(i)
      v3[index] = board[i]
    i+= 1

  vb = [v1, v2, v3]
  for column in vb:
    counter = 0
    for c in column:
      if c == 1:
        counter += 1
      if counter == 2:
        try:
          index = column.index(0)
          placeInList = vb.index(column)
          if placeInList == 0:
            return v1c[index]
          elif placeInList == 1:
             return v2c[index]
          elif placeInList == 2:
            return v3c[index]
        except:
          pass
    
        
  #diagonal 
  d1 = [0, 4, 8]
  d2 = [2, 4, 6]
  d1c = [0, 4, 8]
  d2c = [2, 4, 6]
  i = 0
  while i < len(board):
    if i in d1c:
      index = d1c.index(i)
      d1[index] = board[i]
    elif i in d2c:
      index = d2c.index(i)
      d2[index] = board[i]
    i+= 1

  db = [d1, d2]
  for diagonal in db:
    counter = 0
    for c in diagonal:
      if c == 1:
        counter += 1
      if counter == 2:
        try:
          index = diagonal.index(0)
          placeInList = db.index(diagonal)
          if placeInList == 0:
            return d1c[index]
          elif placeInList == 1:
             return d2c[index]
        except:
          pass

  prioritySquares = [0, 2, 6, 8]
  for y in prioritySquares:
    if board[y] == 0:
      return y
  counter = 0
  while counter <= 8:
    if board[counter] == 0:
      return counter
    counter += 1

