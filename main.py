import math
import time
import requests
import json

def _(string, data):
  return string.format(**data)

def get(url):
  res = requests.get(url)
  return json.loads(res.content.decode('utf-8'))

user = get(_('https://api.github.com/users/{username}', { 
  'username': 'intfract',
}))

users = get('https://api.github.com/search/users?q=type%3Auser')

print(user['bio'])
print(users['total_count'])