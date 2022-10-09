#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ❯ PresenterTools LocalDBSearcher - Created by sirnoob_1#0001 ❮ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

'''
  _____                          _         _______          _     
 |  __ \                        | |       |__   __|        | |    
 | |__) | __ ___  ___  ___ _ __ | |_ ___ _ __| | ___   ___ | |___ 
 |  ___/ '__/ _ \/ __|/ _ \ '_ \| __/ _ \ '__| |/ _ \ / _ \| / __|
 | |   | | |  __/\__ \  __/ | | | ||  __/ |  | | (_) | (_) | \__ \
 |_|   |_|__\___||___/\___|_| |_|\__\___|_|  |_|\___/ \___/|_|___/
 | |    |  __ \|  _ \ / ____|                                     
 | |    | |  | | |_) | (___                                       
 | |    | |  | |  _ < \___ \                                      
 | |____| |__| | |_) |____) |                                     
 |______|_____/|____/|_____/                                      
'''
#━━━━━━━━━━━━━━━━━━━━━━━ ❯ PresenterTools LocalDBSearcher Imports ❮ ━━━━━━━━━━━━━━━━━━━━━━━

#-Module Imports-
import nextcord
import time
import os

#-Class Imports-
from nextcord.ext import commands

#━━━━━━━━━━━━━━━━━━━━━ ❯ PresenterTools LocalDBSearcher Declerations ❮ ━━━━━━━━━━━━━━━━━━━━━


ldbsClient = commands.Bot(command_prefix = ["PREFIX"], case_insensitive = True, intents = nextcord.Intents.all()) #-Set
ldbsClient.remove_command('help')

#━━━━━━━━━━━━━━━━━━━━━ ❯ PresenterTools LocalDBSearcher Startup (<> LIVE <>) ❮ ━━━━━━━━━━━━━━━━━━━━━

if os.path.exists:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            ldbsClient.load_extension(f'cogs.{filename[:-3]}')
            print(f'PresenterTools LDBS -- Loaded {filename[:-3]} --')

else:
    print("PresenterTools LDBS -- ERROR -- Could not find extension directory!")


if not os.path.exists('./media'):
    print("PresenterTools LDBS -- ERROR -- Could not find the media directory!")


#-Run-
ldbsClient.run('INSERT TOKEN HERE') #-Set
