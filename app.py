import discord
import os
import hashlib 
import redis
API_KEY = "AIzaSyDMoflY0MsM1XbgWsg_FViZBXx0msmFmQk"
redis_host = "redis-10362.c98.us-east-1-4.ec2.cloud.redislabs.com"
TOKEN = "Nzk4NTgwNzc0NDA0MDk2MDYw.X_3GTQ.S0huhcP2bHe1hIrb6x_a4IrS1PE"

redis_port = 10362
redis_password = "83gIS9wjeBwi4qVllNa1DGeNiKgX7YUi"
client = discord.Client()
r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
l = []
def put_db(key,value):
  print("key",key,"value",value)
  msg = r.get(key)
  if not msg:
    r.set(key, value)
    print(msg)
  else:
    msg = value + ' ' + msg
    print("update",msg) 
    r.set(key, msg)

def get_db(key):
  key = key.lower()
  print(key)
  key = key.replace(' ','')
  key = hashlib.sha1(key.encode()).hexdigest()
  print(key)
  msg = r.get(key)
  return msg


def set_history(data):
  orginal = data
  data = data.lower()
  data = data.split() 
  for d in data:
    print(d)
    result = hashlib.sha1(d.encode())
    key = result.hexdigest()
    put_db(key, orginal)

  result = hashlib.sha1(orginal.lower().encode()).hexdigest()
  put_db(result, orginal)


def google_hit(data):
  from googlesearch import search   

  # to search 
  query = data

  links = []
  for j in search(query, tld="co.in", num=10, stop=10, pause=2): 
      links.append(j) 
  
  print(links)
  return links
  
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    data = message.content
    #print(data)

    if data.startswith('$google'):
      data = data.replace('$google','')
      msg = google_hit(data)
      set_history(data)
      await message.channel.send(msg)


    if data.startswith('$recent'):
      data = data.replace('$recent','')
      msg = get_db(data)
      await message.channel.send(msg)

    if message.content.startswith('$hello'):
        #r.set("msg:hello", "Hello !!!")
        msg = r.get("test")
        if not msg:
          r.set("test", "testing")
          print(msg)
        else:
          msg = "How" + ' ' + msg 
          r.set("test", msg)
        await message.channel.send(msg)

    if message.content.startswith('$hella'):
        await message.channel.send('bhag!')

    data = message.content
    #print(data)

client.run(TOKEN)
