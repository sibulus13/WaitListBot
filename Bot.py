# https://discordpy.readthedocs.io/en/stable/index.html#

# send a msg to a specific channel
# https://www.google.com/search?q=discord.py+sending+a+message+in+a+channel&rlz=1C1RXQR_enCA978CA978&oq=discord.py+sending+a+message+in+a+channel&aqs=chrome..69i57.6491j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_gXY-Y5_xObCT0PEPmNKL-Aw_18

import math
import discord
from discord.ext import commands

from Discord.WaitListBot.WaitList import PriorityItem, WaitList
from Utils import get_priority

# from WaitList import WaitList
'''
    Post weekly announcement msg
    Create/reset priority queue
    Monitor msg for reactions
    Update priority queue with reactor type
'''

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


class WaitListBot(discord.Client):

    def __init__(self, channelID):
        self.channelID = channelID
        self.channel = bot.get_channel(self.channelID)
        # self.announcementID = -1
        self.wait_list = WaitList()

    def is_announcement(self, msgId):
        if self.announcementID != -1 and msgId == self.announcementID:
            return True
        return False

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        # TODO
        # send announcement msg in announcement channcel
        # save announcement msg id to class

        # await self.send

    async def send(self, channel, message):
        await self.send_message(self.get_channel(channel), message)

    async def on_message(self, message):
        pass

    @bot.command()
    async def signup(self, ctx):
        '''
            sign up user
        '''
        name = ctx.Author
        roles = ctx.Author.roles
        priority = get_priority(roles)
        item = PriorityItem(priority, name)
        msg = self.wait_list.add(item)
        counts = self.wait_list.get_counts()
        await self.channel.send(msg + '\n' + counts)

    @bot.command()
    async def unsignup(self, ctx):
        '''
            unsignup user
        '''
        name = ctx.Author
        roles = ctx.Author.roles
        priority = get_priority(roles)
        item = PriorityItem(priority, name)
        msg = self.wait_list.remove(item)
        await self.channel.send(msg)

    @bot.command()
    async def show(self, ctx):
        '''
            show sign up list
        '''
        signup_list = self.wait_list.get()
        await self.channel.send(signup_list)

    @bot.command()
    async def help(self, ctx):
        msg = 'Below are a list of commands: \n \
                \t signup: Sign up on this week\'s waitlist \n \
                \t unsignup: Un-sign up from this week\'s waitlist \n \
                \t show: show sign up list and waitlist\
                '

        await self.channel.send(msg)


# intents = discord.Intents.default()
# intents.message_content = True

# client = WaitListBot(intents=intents)
# client.run()
