# https://discordpy.readthedocs.io/en/stable/index.html#

import math
from queue import PriorityQueue
import discord

from Discord.PriorityQueueBot.Utils import get_priority
from Discord.PriorityQueueBot.WaitList import WaitList

'''
    Post weekly announcement msg
    Create/reset priority queue
    Monitor msg for reactions
    Update priority queue with reactor type
'''


class WaitListBot(discord.Client):
    def __init__(self, announcementChannel):
        self.waitList = WaitList()
        self.announcementChannel = announcementChannel
        self.announcementID = -1

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

    async def on_reaction_added(self, reaction, user):
        if self.is_announcement(reaction.message):
            priority = get_priority(user.roles)
            entry = {'priority': priority, 'name': user.name}
            self.waitList.add(entry)
            waitlist = self.waitList.get()
            await self.send(self.announcementChannel, waitlist)

    async def on_reaction_remove(self, reaction, user):
        if self.is_announcement(reaction.message):
            priority = get_priority(user.roles)
            entry = {'priority': priority, 'name': user.name}
            self.waitList.remove(entry)
            waitlist = self.waitList.get()
            await self.send(self.announcementChannel, waitlist)


intents = discord.Intents.default()
intents.message_content = True

client = WaitListBot(intents=intents)
client.run()
