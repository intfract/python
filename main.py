import math
import time
import requests
import json
import os

def r(n, to):
  return round(n / to) * to

def _(string, data):
  return string.format(**data)

def get(url):
  res = requests.get(url)
  return json.loads(res.content.decode('utf-8'))

def repo(author, repo):
  data = get(_('https://api.github.com/repos/{author}/{repo}', {
    'repo': repo,
    'author': author,
  }))

  owner = data['owner']['login']
  
  langs = get(_('https://api.github.com/repos/{author}/{repo}/languages', {
    'repo': repo,
    'author': author,
  }))
  
  ratio = {}
  total = 0
  
  for lang in langs.keys():
    total += langs[lang]
  
  for lang in langs.keys():
    ratio[lang] = r((langs[lang] / total) * 100, 1)
  
  return {
    'owner': owner,
    'languages': ratio,
  }

username = 'intfract'

user = get(_('https://api.github.com/users/{username}', { 
  'username': username,
}))

users = get('https://api.github.com/search/users?q=type%3Auser')

print(user['bio'])
print(users['total_count'])
print(repo('intfract', 'defract'))