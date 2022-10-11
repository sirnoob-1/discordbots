#━━━━━━━━━━━━━━━━━━━━━━━ ❯ VTLog Job Logger Imports // Cog: VTLOG ❮ ━━━━━━━━━━━━━━━━━━━━━━━

#-Module Imports-
import datetime
import nextcord
import requests
import calendar
import time

#-Class Imports-
from nextcord.ext import commands, tasks

#- VtlogHandler-
class VtlogHandler(commands.Cog):
    """A class for handling all Vtlog
        events. This Cog is utilised
        by running a 5 minute event timer
        and checking for inconsistencies
        within locally stored data and API"""

    #-__Init__-
    def __init__(self, vtlogClient):
        self.vtlogClient = vtlogClient

    #────────────────────》 Task Loops《────────────────────

    #-Timer-
    @tasks.loop(seconds = 30)
    async def timer(self):
        print('-------Starting Job Cycle-------')
        startTime = int(time.time())


        apiData = await self.fetch_api_data()
        print('Job Logger -- [SUCCESS] VTLOG Data Fetched')


        if apiData == False:
            print('Job Logger -- [INFO] No new entries - returning')
            self.vtlogClient.lastAPI = int(time.time())
            print('Job Logger -- [INFO] Updated lastAPI timestamp.')
            return

        await self.update_member_cache()

        memberCache = self.vtlogClient.memberCache

        apiEmbedList = []

        print('Job Logger -- [SUCCESS] Starting Job Entry Loop')
        for jobEntry in apiData:


            for member in memberCache['response']['members']:

                if member['username'] == jobEntry['username']:
                    break

            print('Job Logger -- [SUCCESS] Found new job entry for ' + member['username'])

            try:
                jobData = jobEntry["data"]
                jobDest = jobData["destination"]
                jobSource = jobData["source"]
                jobTruck = jobData["truck"]
                jobCargo = jobData["cargo"]
                jobFinance = jobData["finance"]
                jobDate = calendar.day_name[datetime.date.today().weekday()][0:3] + ' ' + datetime.date.today().strftime("%B %d, %Y")

            except:
                print('Job Logger -- [FAIL] DATA BAD - Breaking loop')
                break

            print('Job Logger -- [SUCCESS] DATA OK - Constructing Embed')

            jobEmbed = nextcord.Embed(title = 'Job Delivered | Result: ' + str(jobFinance["total_profit"]) + ' credits', url = f'https://vtlog.net/job/{jobEntry["job_id"]}', color = 0x0390fc)

            jobEmbed.add_field(name = '📅 Date', value = jobDate + '**　　　　**') #- Expanding the first column to create a seperated look
            jobEmbed.add_field(name = '🗺️ Source', value = jobSource["company"] + ' - ' + jobSource["city"])
            jobEmbed.add_field(name = '👉 Destination', value = jobDest["company"] + ' - ' + jobDest["city"])
            jobEmbed.add_field(name = '🚚 Vehicle', value = jobTruck["brand"] + ' ' + jobTruck["model"] + ' (' + jobTruck["license_plate"] + ')')
            jobEmbed.add_field(name = '👋 Departed', value = f'<t:{jobSource["departure"]}:t>')
            jobEmbed.add_field(name = '🌤️ Arrived', value = f'<t:{jobDest["arrival"]}:t>')
            jobEmbed.add_field(name = '↔️ Distance', value = jobData["distance_driven"])
            jobEmbed.add_field(name = '🚨 Cargo', value = jobCargo["name"])
            jobEmbed.add_field(name = '🏋️‍♂️ Weight', value = str(jobCargo["mass"]) + 'kg')
            jobEmbed.add_field(name = '⏰ Duration', value = str(datetime.timedelta(seconds = jobDest["arrival"] - jobSource["departure"])))
            jobEmbed.add_field(name = '🌎 Fuel Economy', value = str(round(int(jobData["fuel_consumed"]) / jobData["distance_driven"] * 100, 2))  + ' L / 100km')
            jobEmbed.add_field(name = '⛽ Fuel', value = str(jobData["fuel_consumed"]) + 'L')
            jobEmbed.add_field(name = '💵 Profit', value = str(jobFinance["total_profit"]) + ' Credits')
            jobEmbed.add_field(name = '📥 Earned Credits', value = jobFinance["total_income"])
            jobEmbed.add_field(name = '📤 Lost Credits', value = jobFinance["total_expenses"])

            jobEmbed.set_footer(text = 'Logbook', icon_url = 'https://i.imgur.com/l98wY7X.png')
            jobEmbed.set_author(icon_url = member['avatar'], name = member['username'], url = f'https://vtlog.net/profile/{member["steam_id"]}')
            jobEmbed.timestamp = datetime.datetime.fromtimestamp(int(jobDest["arrival"]))

            if member['discord_id'] == 0:
                member['discord_id'] == ' '

            apiEmbedList.append([int(jobDest["arrival"]), jobEmbed, ('<@' + str(member["discord_id"]) + '>') if str(member["discord_id"]) != "0" else False])

            print('Job Logger -- [SUCCESS] DATA OK - Embed entry Queued')

        print('Job Logger -- [SUCCESS] Exited Job Entry Loop')

        apiEmbedList.sort(key=lambda x: int(x[1].fields[5].value.strip(' ').strip('<t:').strip(':t>')))

        print('Job Logger -- [SUCCESS] Data sorted - Exporting')

        logGuild = self.vtlogClient.get_guild() #-Set
        postChannel = logGuild.get_channel() #-Set

        for jobArray in apiEmbedList:

            await postChannel.send(embed = jobArray[1], content = jobArray[2] if jobArray[2] != False else '')
            print('Job Logger -- [SUCCESS] Published entry for ' + jobArray[1].author.name)

        print('Job Logger -- [SUCCESS] Job Cycle Exited - Completed in ' + str(int(time.time() - startTime)) + ' seconds')

    #-MemberUpdater-
    @tasks.loop(seconds = 600)
    async def memberUpdater(self):

        await self.update_member_cache()

    #-TimerReviver-
    @tasks.loop(seconds = 300)
    async def timerReviver(self):

        try:
            self.timer.start()
            self.memberUpdater.start()

        except RuntimeError:
            pass

    #────────────────────》 Async Functions《────────────────────

    #-Fetch_API_Data-
    async def fetch_api_data(self):

        callTime = int(time.time())

        vtlogRequest = requests.get('https://api.vtlog.net/v3/companies/COMPANY_NUM/jobs') #-Set
        vtlogJobs = vtlogRequest.json()['response']['jobs']
        print('Job Logger -- [INFO] - VTlog API returned ' + str(vtlogRequest).strip('<>'))

        newJobs = []


        for jobObj in vtlogJobs:
            
            if int(jobObj['data']['destination']['arrival']) >= self.vtlogClient.lastAPI:

                newJobs.append(jobObj)

        self.vtlogClient.jobCache = vtlogJobs


        if len(newJobs) == 0:
            return False

        self.vtlogClient.lastAPI = callTime
        print('Job Logger -- [INFO] Updated lastAPI timestamp')

        return newJobs

    #-Update_Member_Cache-
    async def update_member_cache(self):

        self.vtlogClient.memberCache = requests.get('https://api.vtlog.net/v3/companies/COMPANY_NUM/members').json() #- Set
        print('Job Logger -- [INFO] Member Cache Cycled')


    #────────────────────》 Events《────────────────────

    #On_Ready-
    @commands.Cog.listener()
    async def on_ready(self):

        if not self.vtlogClient.hasConnected: #- If the bot has been started from file...
            print(f'━━━━━━━━━━━━━━━━━━━━━━━━\n'
                f'Logged in to Discord as {self.vtlogClient.user.display_name} // ID: {self.vtlogClient.user.id}\n'
                f'API Version: {nextcord.__version__} // Nextcord\n'
                f'Ping: {round(self.vtlogClient.latency * 1000)}ms\n'
                f'Heartbeat: {str((round(self.vtlogClient._connection.heartbeat_timeout)))}ms\n'
                f'Connected: {str(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))}'
                '\n━━━━━━━━━━━━━━━━━━━━━━━━')

            self.timer.start()
            self.memberUpdater.start()
            self.timerReviver.start()
            print('Job Logger -- [SUCCESS] Timers Initiated')

        else:
            return print('{self.vtlogClient.user.display_name} Websocket reconnected ' + str(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))


def setup(vtlogClient):
    vtlogClient.add_cog(VtlogHandler(vtlogClient))
