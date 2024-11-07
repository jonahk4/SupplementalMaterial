from replit import db

def status(server_id, choice):
  if server_id in db:
    if choice == "on":
      db[server_id]["autoresponderstatus"] = "on"
    else:
      db[server_id]["autoresponderstatus"] = "off"
  else:
    if choice == "on":
      db[server_id] = {"autoresponderstatus": "on"}
      db[server_id]["messagecounter"] = 0
    else:
      db[server_id] = {"autoresponderstatus": "off"}
      db[server_id]["messgaecounter"] = 0

def addautoresponse(server_id, inputmessage, response):
  if server_id in db:
    if db[server_id].get("messagecounter"):
      if db[server_id]["messagecounter"] < 10:
        if inputmessage not in db[server_id].keys():
          db[server_id][inputmessage.lower()] = response
          db[server_id]["messagecounter"] += 1
        else:
          raise TypeError
      else:
        raise ValueError
    else:
      db[server_id]["autoresponderstatus"] = "on"
      db[server_id][inputmessage.lower()] = response
      db[server_id]["messagecounter"] = 0
      db[server_id]["messagecounter"] += 1

  else:
    db[server_id]["messagecounter"] = 0
    db[server_id] = {"autoresponderstatus": "on", inputmessage.lower(): response}
    db[server_id]["messagecounter"] = 0
    db[server_id]["messagecounter"] += 1

def deleteautoresponse(server_id, response):
  if server_id in db:
    if response.lower() in db[server_id]:
      if response != "messagecounter" and response != "autoresponderstatus":
        del db[server_id][response]
        db[server_id]["messagecounter"] -= 1
      else:
        pass
    else:
      raise ValueError
  else:
    raise TypeError

def inputmessage(server_id):
  return db[server_id].keys()
  
def inputresponse(server_id):
  return db[server_id].values()
    
def checkid(server_id):
  if server_id in db:
    return True
  else:
    return False
    
def checkmessage(server_id, message):
  if message.lower() in db[server_id]:
    return True
  else:
    return False

def clearautoresponse(server_id):
  if server_id in db:
    del db[server_id]
  else:
    raise ValueError

def checkstatus(server_id):
  if db[server_id]["autoresponderstatus"] == "on":
    return True
  else:
    return False

def messagecounter(server_id):
  return db[server_id]["messagecounter"]