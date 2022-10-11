# https://discordpy.readthedocs.io/en/stable/index.html#

# send a msg to a specific channel
# https://www.google.com/search?q=discord.py+sending+a+message+in+a+channel&rlz=1C1RXQR_enCA978CA978&oq=discord.py+sending+a+message+in+a+channel&aqs=chrome..69i57.6491j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_gXY-Y5_xObCT0PEPmNKL-Aw_18

import math
import discord
from discord.ext import commands

from WaitList import PriorityItem, WaitList
from Utils import get_priority
from BotCommands import *
# from WaitList import WaitList
'''
    Post weekly announcement msg
    Create/reset priority queue
    Monitor msg for reactions
    Update priority queue with reactor type
'''


class WaitListBot(discord.Client):

    def __init__(self, channelID, intents):
        super().__init__(intents)
        self.channelID = channelID
        self.channel = bot.get_channel(self.channelID)
        # self.announcementID = -1
        self.wait_list = WaitList()

    def is_announcement(self, msgId):
        if self.announcementID != -1 and msgId == self.announcementID:
            return True
        return False

    async def on_ready(self):
        print(f'Logged on as {self.user}. Hi, this is the waitlist bot!')
        # TODO
        # send announcement msg in announcement channcel
        # save announcement msg id to class

        # await self.send

    async def send(self, channel, message):
        await self.send_message(self.get_channel(channel), message)

    async def on_message(self, message):
        pass