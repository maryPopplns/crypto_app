import os
from dotenv import load_dotenv
from requests import Request, Session

load_dotenv()

def headline_request():
  # env variables
  host = os.getenv('HOST')
  key = os.getenv('KEY')

  url = 'https://crypto-pulse.p.rapidapi.com/news'
  s = Session()
  request = Request('GET', url)
  prepared = request.prepare()

  # headers
  prepared.headers['X-RapidAPI-Host'] = host
  prepared.headers['X-RapidAPI-Key'] = key

  resp = s.send(prepared)
  return resp.json()