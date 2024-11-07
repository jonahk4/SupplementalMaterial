from replit import db


def setup(server_id):
  if server_id in db:
    db[server_id]["ticketdescription"] = "Please wait. Someone will be here to assist you as soon as soon as they are available. All messages in this channel are being recorded."
    db[server_id]["ticketmessage"] = "Please type your question or problem in this channel. Someone will be here to assist you as soon as soon as they are available."
    db[server_id]["ticketsystem"] = True
  else:
    db[server_id] = {"ticketdescription": "Please wait. Someone will be here to assist you as soon as soon as they are available. All messages in this channel are being recorded.", "ticketmessage": "Please type your question or problem in this channel. Someone will be here to assist you as soon as soon as they are available.", "ticketsystem": True}

def checktopic(server_id):
  if server_id in db:
    topic = db[server_id]["ticketdescription"]
    return topic

def checkmessage(server_id):
  if server_id in db:
    message = db[server_id]["ticketmessage"]
    return message

def editticketmessage(server_id, message):
  try: 
    if "ticketmessage" in db[server_id]:
      db[server_id]["ticketmessage"] = message
    else:
      raise ValueError
  except KeyError:
    raise ValueError

def edit_ticket_topic(server_id, topic):
  try:
    if "ticketdescription" in db[server_id]:
      db[server_id]["ticketdescription"] = topic
    else:
      raise ValueError
  except KeyError:
    raise ValueError

def returnticketmessage(server_id):
  if server_id in db:
    return db[server_id]["ticketmessage"]

def returnticketdescription(server_id):
  if server_id in db:
    return db[server_id]["ticketdescription"]



