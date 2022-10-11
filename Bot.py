import discord
from discord.ext import commands, tasks
from datetime import datetime

from Constants import DISCORD_TOKEN, MAX_SIGN_UP_COUNT, PRIORITY_MAP, WAITLIST_PRIORITY, tuesday_resets, monday_night_update_lists
from Firebase import add_to_db, delete_from_db, get_list, get_lists, reset_db, signedup_ref, waitlist_ref

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


def is_super(ctx, super_role='Discord Admin'):
    for role in ctx.author.roles:
        # print(role, role.id, role.name)
        if role.name == super_role:
            return True
    return False


@bot.command(pass_context=True)
async def reset(ctx):
    '''
        reset waitlist
    '''
    # print(is_super(ctx))
    if is_super(ctx):
        reset_db()

    else:
        msg = 'You do not have permission to reset the waitlist'
        ctx.channel.send(msg)


@bot.command(pass_context=True)
async def signup(ctx):
    '''
        sign up user
    '''
    print('sign up')
    name = ctx.author.name + ctx.author.id
    if waitlistable(ctx):
        add_to_db(name, waitlist_ref)
    else:
        add_to_db(name, signedup_ref)


@bot.command(pass_context=True)
async def unsignup(ctx):
    '''
        unsignup user
    '''
    print('unsign up')
    name = ctx.author.name + ctx.author.id
    if delete_from_db(name, signedup_ref):
        today = datetime.today().weekday()
        print(today)
        if today == 1:
            # Waitlist priority not in effect on tuesdays
            print('Today is Tuesday, updating list')
            update_lists()
        return
    delete_from_db(name, waitlist_ref)


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
    msg = 'Below are a list of commands: \n \
            \t signup: Sign up on this week\'s waitlist \n \
            \t unsignup: Un-sign up from this week\'s waitlist \n \
            \t show: show sign up list and waitlist\n \
            \t info: show possible bot commands\n \
            \t SFU student priority signup are in effect until Monday night weekly, then it is free for all\n \
            \t The sign up list and wait list are both refreshed weekly on Tuesday nights\n \
            '

    print(msg)
    await ctx.channel.send(msg)


def waitlistable(ctx):
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
    print(today)
    if today == 1:
        # Waitlist priority not in effect on tuesdays
        print('Today is Tuesday')
        return False
    return False


# @tasks.loop(time=tuesday_resets)
async def weekly_reset():
    print('Performing weekly Tuesday reset')
    reset_db()


# @tasks.loop(time=monday_night_update_lists)
async def weekly_list_update():
    print('Performing weekly Monday update')
    update_lists()


# @bot.command(pass_ctx=True)
async def update_lists(ctx=None):
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