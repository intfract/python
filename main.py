import math
import time
import requests
import json
import os
import urllib

def r(n, to):
  return round(n / to) * to

def _(string, data):
  return string.format(**data)

def get(url):
  url.replace(' ', '%20')
  res = requests.get(url, stream=True)
  if url.endswith('.pdf'):
    with open(f'out/{url[-18:]}', 'wb') as f:
      for chunk in res.iter_content(2000):
        f.write(chunk)
  else:
    try:
      data = json.loads(res.content.decode('utf-8'))
      if data['message']:
        return data['message']
      return data
    except Exception as e:
      return e

def repo(author, repo):
  data = get(_('https://api.github.com/repos/{author}/{repo}', {
    'repo': repo,
    'author': author,
  }))

  if (type(data) == str):
    return data

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

# print(user)
# print(users)
# print(repo('intfract', 'defract'))

print(get(_('https://papers.gceguide.com/Cambridge IGCSE/Sciences - Co-ordinated (Double) (0654)/20{year}/0654_{series}{year}_{type}_{paper}{variant}.pdf', {
  'series': 'w',
  'year': '21',
  'type': 'qp',
  'paper': 2,
  'variant': 1,
})))