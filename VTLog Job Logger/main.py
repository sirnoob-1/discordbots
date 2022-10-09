#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ❯ VTlog Job Logger - Created by sirnoob_1#0001 ❮ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

'''
 __      _________ _                        _       _       _                                 
 \ \    / /__   __| |                      | |     | |     | |                                
  \ \  / /   | |  | |     ___   __ _       | | ___ | |__   | |     ___   __ _  __ _  ___ _ __ 
   \ \/ /    | |  | |    / _ \ / _` |  _   | |/ _ \| '_ \  | |    / _ \ / _` |/ _` |/ _ \ '__|
    \  /     | |  | |___| (_) | (_| | | |__| | (_) | |_) | | |___| (_) | (_| | (_| |  __/ |   
     \/      |_|  |______\___/ \__, |  \____/ \___/|_.__/  |______\___/ \__, |\__, |\___|_|   
                                __/ |                                    __/ | __/ |          
                               |___/                                    |___/ |___/   

'''
#━━━━━━━━━━━━━━━━━━━━━━━ ❯ VTLog Job Logger Imports ❮ ━━━━━━━━━━━━━━━━━━━━━━━

#-Module Imports-
import nextcord
import time
import os

#-Class Imports-
from nextcord.ext import commands

#━━━━━━━━━━━━━━━━━━━━━ ❯ VTLog Job Logger Declerations ❮ ━━━━━━━━━━━━━━━━━━━━━


vtlogClient = commands.Bot(command_prefix = ["PREFIX"], case_insensitive = True, intents = nextcord.Intents.all()) #-Set
vtlogClient.remove_command('help')

vtlogClient.lastAPI = int(time.time()) #- An integer for the bot to filter newest results with
vtlogClient.memberCache = {} #- Dictionary to hold attributes of VTLog users
vtlogClient.jobCache = {} #- Dictionary to hold job cache, which holds the data of a previous API call, it looks for new entries by comparing it to updated data.

vtlogClient.hasConnected = False #- Bool to prevent websocket reconnections from breaking the timers

#━━━━━━━━━━━━━━━━━━━━━ ❯ VTLog Job Logger Startup (<> LIVE <>) ❮ ━━━━━━━━━━━━━━━━━━━━━

if os.path.exists:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            vtlogClient.load_extension(f'cogs.{filename[:-3]}')
            print(f'Job Logger -- Loaded {filename[:-3]} --')

else:
    print("Job Logger -- ERROR -- Could not find extension directory!")

#-Run-
vtlogClient.run('INSERT TOKEN HERE') #-Set
