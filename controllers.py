import os
from dotenv import load_dotenv
from requests import Request, Session

load_dotenv()

def headlines_controller():
  # env variables
  host = os.getenv('PULSE_HOST')
  key = os.getenv('PULSE_KEY')

  url = 'https://crypto-pulse.p.rapidapi.com/news'
  s = Session()
  request = Request('GET', url)
  prepared = request.prepare()

  # headers
  prepared.headers['X-RapidAPI-Host'] = host
  prepared.headers['X-RapidAPI-Key'] = key

  resp = s.send(prepared)
  return resp.json()

def topcoins_controller():
  # env variables
  host = os.getenv('MINEABLE_HOST')
  key = os.getenv('MINEABLE_KEY')

  url = 'https://mineable-coins.p.rapidapi.com/coins'
  s = Session()
  request = Request('GET', url)
  prepared = request.prepare()

  # headers
  prepared.headers['X-RapidAPI-Host'] = host
  prepared.headers['X-RapidAPI-Key'] = key

  resp = s.send(prepared)
  return resp.json()

