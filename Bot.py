import discord
from discord.ext import commands, tasks
from datetime import datetime

from Constants import BOT_CHANNEL_ID, DISCORD_TOKEN, MAX_SIGN_UP_COUNT, PRIORITY_MAP, RESET_TIME, SIB_ID, WAITLIST_PRIORITY
from Firebase import add_to_db, delete_from_db, get_list, get_lists, reset_db, signedup_ref, waitlist_ref
from Utils import priority_not_in_effect

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


def is_super(ctx, super_role='Discord Admin'):
    '''
        Checks if context user is a super_role
    '''
    if ctx.author.id == SIB_ID:
        return True
    for role in ctx.author.roles:
        # print(role, role.id, role.name)
        if role.name == super_role:
            return True
    return False


@bot.command(pass_context=True)
async def reset(ctx):
    '''
        resets waitlist if context user is a super_role or sends warning message
    '''
    # print(is_super(ctx))
    # print(ctx.author.name, ctx.author.id)
    # print(is_super(ctx))
    if is_super(ctx):
        reset_db()
        msg = 'Signup and wait lists have been reset'
        await ctx.channel.send(msg)

    else:
        msg = 'You do not have permission to reset the waitlist'
        await ctx.channel.send(msg)


@bot.command(pass_context=True)
async def signup(ctx):
    '''
        sign up user based on waitlistability
    '''
    print('sign up')
    name = ctx.author.name + str(ctx.author.id)
    msg = f'{ctx.author.name} has been signed up'
    signedup, waitlist = get_lists()
    if name in signedup.values() or name in waitlist.values():
        msg = f'{ctx.author.name} has already been signed up!'
        print(msg)
        await ctx.channel.send(msg)
        return
    if waitlistable(ctx):
        add_to_db(name, waitlist_ref)
        print(msg)
        await ctx.channel.send(msg)
    else:
        add_to_db(name, signedup_ref)
        print(msg)
        await ctx.channel.send(msg)


@bot.command(pass_context=True)
async def unsignup(ctx):
    '''
        unsignup user if user is in signedup list or waitlist
    '''
    print('unsign up')
    name = ctx.author.name + str(ctx.author.id)
    if delete_from_db(name, signedup_ref):
        today = datetime.today().weekday()
        print(today)
        msg = f'{ctx.author.name} has been removed from the signup list!'
        print(msg)
        await ctx.channel.send(msg)

        if priority_not_in_effect(today):
            # Waitlist priority not in effect on tuesdays
            print('Today is Tuesday, updating list')
            update_lists()
        return
    delete_from_db(name, waitlist_ref)
    msg = f'{ctx.author.name} has been removed from the waitlist!'
    print(msg)
    await ctx.channel.send(msg)


@bot.command(pass_context=True)
async def show(ctx):
    '''
        show sign up list
    '''
    signedup, waitlist = get_lists()
    msg = 'Signed up: \n'

    for i, key in enumerate(signedup):
        msg += f'\t{i+1}: {signedup[key]} \n'
    msg += 'Waitlisted: \n'
    for i, key in enumerate(waitlist):
        msg += f'\t{i+1}: {waitlist[key]} \n'
    print(msg)
    await ctx.channel.send(msg)


@bot.command(pass_ctx=True)
async def info(ctx):
    '''
        Msg channel list of possible bot commands
    '''

    msgCmds = 'Below are a list of commands: \n \
            \t signup: Sign up on this week\'s waitlist \n \
            \t unsignup: Un-sign up from this week\'s waitlist \n \
            \t show: show sign up list and waitlist\n \
            \t info: show possible bot commands\n '

    msgInfo = '\t SFU student priority signup are in effect until Monday night weekly, then it is free for all\n \
            \t The sign up list and wait list are both refreshed weekly on Tuesday nights\n \
            '

    if is_super(ctx):
        msgCmds += 'reset: Resets sign up and waitlist databases \n'
        print(msgCmds + msgInfo)
    await ctx.channel.send(msgCmds + msgInfo)


def waitlistable(ctx):
    '''
        Checks if ctx author is waitlistable
    '''
    priority = 100
    for role in ctx.author.roles:
        # print(role.name)
        if role.name in PRIORITY_MAP:
            prio = PRIORITY_MAP[role.name]
            priority = min(priority, prio)

    signup_list = get_list(signedup_ref)
    print(len(signup_list))
    if len(signup_list) >= MAX_SIGN_UP_COUNT:
        print('Max sign up number reached')
        return True
    if priority < WAITLIST_PRIORITY:
        print('Low Priority, waitlisted')
        return False
    today = datetime.today().weekday()
    # print(today)
    if priority_not_in_effect(today):
        print('Today is Tuesday')
        return False
    return False


@bot.listen()
async def on_ready():  # important to start the loop
    weekly_reset.start()
    weekly_list_update.start()


@tasks.loop(time=RESET_TIME)
async def weekly_reset():
    '''
        Clear db to reset weekly signup and waitlist
    '''
    if datetime.today().weekday() == 2:
        channel = bot.get_channel(BOT_CHANNEL_ID)
        msg = f'The weekly lists have been reset'
        print(msg)
        await channel.send(msg)
        reset_db()


@tasks.loop(time=RESET_TIME)
async def weekly_list_update():
    '''
        Performing weekly Monday update
    '''
    if datetime.today().weekday() == 0:
        channel = bot.get_channel(BOT_CHANNEL_ID)
        msg = f'The weekly lists have been updated with the removal of priority entries'
        print(msg)
        await channel.send(msg)
        print('Performing weekly Monday update')
        update_lists()


# @bot.command(pass_ctx=True)
async def update_lists(ctx=None):
    '''
        Pull waitlisted people to sign up list if there is room
    '''
    signup_list = get_list(signedup_ref)
    waitlist = get_list(waitlist_ref)
    signup_list_length = len(signup_list)
    waitlist_length = len(waitlist)
    if signup_list_length >= MAX_SIGN_UP_COUNT or waitlist_length == 0:
        return

    free_spots = MAX_SIGN_UP_COUNT - signup_list_length
    for key in waitlist:
        add_to_db(waitlist[key], signedup_ref)
        waitlist.pop(key)
        free_spots -= 1
        if free_spots == 0:
            waitlist_ref.set(waitlist)
            return


if __name__ == '__main__':
    bot.run(token=DISCORD_TOKEN)
