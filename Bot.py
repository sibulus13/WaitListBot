# https://discordpy.readthedocs.io/en/stable/index.html#

# send a msg to a specific channel
# https://www.google.com/search?q=discord.py+sending+a+message+in+a+channel&rlz=1C1RXQR_enCA978CA978&oq=discord.py+sending+a+message+in+a+channel&aqs=chrome..69i57.6491j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_gXY-Y5_xObCT0PEPmNKL-Aw_18

import math
import discord
from Discord.WaitListBot.WaitList import PriorityItem, WaitList

from Utils import get_priority
# from WaitList import WaitList
'''
    Post weekly announcement msg
    Create/reset priority queue
    Monitor msg for reactions
    Update priority queue with reactor type
'''


class WaitListBot(discord.Client):

    def __init__(self, announcementChannel):
        self.announcementChannel = announcementChannel
        self.announcementID = -1
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

    # async def on_reaction_added(self, reaction, user):
    #     if self.is_announcement(reaction.message):
    #         priority = get_priority(user.roles)
    #         entry = PriorityItem(priority, user.name)
    #         self.wait_list.add(entry)
    #         wait_list = self.wait_list.get()
    #         await self.send(self.announcementChannel, wait_list)

    # async def on_reaction_remove(self, reaction, user):
    #     if self.is_announcement(reaction.message):
    #         priority = get_priority(user.roles)
    #         entry = {'priority': priority, 'name': user.name}
    #         self.waitList.remove(entry)
    #         waitlist = self.waitList.get()
    #         await self.send(self.announcementChannel, waitlist)


# intents = discord.Intents.default()
# intents.message_content = True

# client = WaitListBot(intents=intents)
# client.run()
