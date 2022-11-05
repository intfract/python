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
    with open(f"out/{url.split('/')[-1].split('?')[-1]}", 'wb') as f:
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

  if (type(data) == str or type(data) == KeyError):
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

def pastpaper(code, series, year, type, paper, variant):
  return _('https://papers.gceguide.com/Cambridge IGCSE/{name} ({code})/20{year}/{code}_{series}{year}_{type}_{paper}{variant}.pdf', {
    'name': codes[code],
    'code': code,
    'series': series[:1],
    'year': str(year)[-2:],
    'type': type,
    'paper': paper,
    'variant': variant,
  })

username = 'intfract'

user = get(_('https://api.github.com/users/{username}', { 
  'username': username,
}))

users = get('https://api.github.com/search/users?q=type%3Auser')

# print(user)
# print(users)
# print(repo('intfract', 'defract'))

codes = {
  '0452': 'Accounting',
  '0654': 'Sciences - Co-ordinated (Double)',
}

# 2016 pdf papers struggle to load 
for i in range(21, 16, -1):
  for j in range(1, 4):
    get(pastpaper('0654', 'winter', i, 'qp', 2, j))
