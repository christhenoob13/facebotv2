import asyncio
import json
from fbchat_muqit import Client, Message, ThreadType, State
from handler.loadConfig import loadConfig
from handler.loadEvents import loadEvents
from handler.loadCommands import loadCommands
from handler.messageHandler import handleMessage
from handler.eventHandler import handleEvent
config = json.load(open('config.json', 'r'))

class Greeg(Client):
  def BOT(self, data):
    self.commands = loadCommands() # dict
    self.events = loadEvents() # list
    
    self.prefix = data['prefix']
    self.botName = data['botName']
    self.owner = data['owner']
    self.admin = data['admin']
  
  async def onListening(self):
    print("\033[96m[BOT] \033[0mListening...")
  
  async def __botEvent(self, event, **data):
    asyncio.create_task(handleEvent(self, event, **data))
  async def __messaging(self, mid, author_id, message, message_object, thread_id, thread_type, **kwargs):
    if author_id != self.uid:
      await self.__botEvent('type:message', mid=mid,author_id=author_id,message=message,message_object=message_object,thread_id=thread_id,thread_type=thread_type,**kwargs)
      asyncio.create_task(handleMessage(self,mid,author_id,message,message_object,thread_id,thread_type,**kwargs))
  
  """MESSAGE EVENTS"""
  async def onReply(self, mid, author_id, message, message_object, thread_id,thread_type, **kwargs):
    await self.__messaging(mid, author_id, message, message_object, thread_id,  thread_type, **kwargs)
  async def onMessage(self,mid,author_id,message,message_object,thread_id,thread_type,**kwargs):
    await self.__messaging(mid, author_id, message, message_object, thread_id,  thread_type, **kwargs)
  
  """OTHER EVENTS"""
  
  
async def main():
  cookies_path = "fbstate.json"
  bot = await Greeg.startSession(cookies_path)
  if await bot.isLoggedIn():
    fetch_bot = await bot.fetchUserInfo(bot.uid)
    bot_info = fetch_bot[bot.uid]
    kol = await loadConfig(bot_info.name)
    bot.BOT(kol)
    print(f"\033[97m⦿━━━━━━━━━━━━━━━⦿ \033[96mFACEBOT \033[97m⦿━━━━━━━━━━━━━━━⦿")
    print(f"\033[32m[BOT] \033[0m{bot_info.name} is now logged in")
  try:
    await bot.listen()
  except Exception as e:
    print("ERROR: ", e)

if __name__ == '__main__':
  asyncio.run(main())