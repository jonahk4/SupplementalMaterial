# import urllib library
from urllib.request import urlopen

# import json
import json

class XKCDCOMIC:
  def __init__(self):
    self.__number = None
    pass
  def getLatestComic(self):
    url = "https://xkcd.com/info.0.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    title = data_json['title']
    alt = data_json['alt']
    image = data_json['img']
    number = data_json['num']
    return [title, response, image, alt, number]
  def getComic(self, number):
    self.__number = number
    url = f"https://xkcd.com/{number}/info.0.json"
    response = urlopen(url)
    data_json = json.loads(response.read())
    title = data_json['title']
    alt = data_json['alt']
    image = data_json['img']
    number = data_json['num']
    return [title, response, image, alt, number]
    