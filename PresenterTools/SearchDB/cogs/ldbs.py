#━━━━━━━━━━━━━━━━━━━━━━━ ❯ PresenterTools LocalDBSearcher // Cog: ldbs (local Database Search) ❮ ━━━━━━━━━━━━━━━━━━━━━━━

#-Module Imports-
import datetime
import nextcord
import requests
import calendar
import time
import eyed3
import os

#-Class Imports-
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from logging import getLogger

getLogger().setLevel("ERROR") #- Prevents eyeD3 from spitting out rubbish

#- VtlogHandler-
class ldbsHandler(commands.Cog):
    """A class for handling
    PresenterTools LDBS functions"""

    #-__Init__-
    def __init__(self, ldbsClient):
        self.ldbsClient = ldbsClient

    GUILDID = 899031670974464040

    #────────────────────》 Commands 《────────────────────

    #-SearchDataBase-
    @nextcord.slash_command(name = 'search_database', description = 'Searches the local database for a queried song', guild_ids=[GUILDID])
    async def searchDataBase(self, interaction: Interaction, query: str = SlashOption(description = 'The query of the song to search for')):

        print('PresenterTools LDBS -- [SUCCESS] Started \'searchDatabase\' Function')

        #-Vars-
        MatchingSongs = []
        SongTotalIterateCounter = 0
        StartTime = time.time()
        SongQuery = query.lower()
        SongQuery = SongQuery.replace('-', '')
        SongQuery = SongQuery.replace('  ', ' ')
        SongCounter = 0

        #-Sequence-
        await interaction.response.defer()

        if not os.path.exists('./media'):
            print("PresenterTools LDBS -- ERROR -- Could not find the media directory!")
            return await interaction.followup.send('Error! Could not find the database, please try again shortly')
            
        
        for filetype in os.listdir('./media'):

            if os.path.isfile(os.path.join('./media', filetype)):
                SongCounter += 1

        print('PresenterTools LDBS -- [SUCCESS] Iterated ' + str(SongCounter) + ' songs')

        for song in os.listdir('./media'):

            SongFile = eyed3.load(f'./media/{song}')
            SongArtist = SongFile.tag.artist
            SongTitle = SongFile.tag.title

            SongTotal = (SongArtist if SongArtist is not None else '').lower() + ' ' + (SongTitle if SongTitle is not None else '').lower()
            
            if SongQuery in SongTotal:
                MatchingSongs.append(SongArtist + ' - ' + SongTitle)
            
            SongTotalIterateCounter += 1
        
        SearchEmbed = nextcord.Embed(color = 0x0390fc)
        if len(MatchingSongs) == 0:
            SearchEmbed.description = f'❌ Couldn\'t find anything matching \'{query}\' on Sailor Radio, why not ask one of our presenters if they\'ve got what your looking for, or try a new keyword.'
            print('PresenterTools LDBS -- [SUCCESS]  Passed, unable to find anything matching query ' + query)

            
        else:
            SearchEmbed.title = f'Found {len(MatchingSongs)} Song' + ('s' if len(MatchingSongs) == 0 or len(MatchingSongs) > 1 else '') +  f' matching \'{query}\''
            print('PresenterTools LDBS -- [SUCCESS] Found ' + str(len(MatchingSongs)) + ' matching songs!')

        
        counter = 0
        for song in MatchingSongs:
            if counter == 15:
                break

            try:
                SearchEmbed.description += f'` - ` {song}\n';

            except TypeError:
                SearchEmbed.description = f'` - ` {song}\n'
            counter += 1
        
        if len(MatchingSongs) > 15:
            SearchEmbed.description += f'\n *Displaying* ***15*** *out of* ***{len(MatchingSongs)}*** *total matching songs*'
            print('PresenterTools LDBS -- [SUCCESS] Shortened embed due to high amount of results')


        
        if not 'Couldn\'t find anything matching' in SearchEmbed.description:
            SearchEmbed.set_footer(text = f'Iterated {SongCounter} songs in: {round(time.time() - StartTime, 2)}s, {round(len(MatchingSongs) / SongCounter * 100, 1)}% of all songs')
        
        if len(SearchEmbed.description) >= 4096:
            SearchEmbed.description = SearchEmbed.description[:4096]
        await interaction.followup.send(embed = SearchEmbed)

        print('PresenterTools LDBS -- [SUCCESS] Function successful, ending')


#-Setup-
def setup(ldbsClient):
    ldbsClient.add_cog(ldbsHandler(ldbsClient))