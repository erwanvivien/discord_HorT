# need to do :
import discord
import os
from discord.ext import commands

# from utils import get_content
# from discord_utils import author_name, error_message

# from discord_utils import hort, horts, hort_lim, hort_spec
# from utils import add


import discord_utils
import utils

# from discord_utils import hort

# All the bot ids (dev and current)
BOT_IDS = []
# The dev id (Xiaojiba#1407)
DEV_IDS = [289145021922279425]
# Error log
ERRORS = []
# Invite link
DISC_LNK = 'https://discord.com/api/oauth2/authorize?client_id=798130116491345971&permissions=2048&scope=bot'


# The prefix used to trigger the bot
prefix = "$hort"

# Discord bot token
token = utils.get_content("token")

if not os.path.isdir("subreddit_saves"):
    os.mkdir("subreddit_saves")

CMDS = {
    "$hart": discord_utils.hort,
    "$hort": discord_utils.hort,

    "$harts": discord_utils.horts,
    "$horts": discord_utils.horts,

    "$hortlim": discord_utils.hort_lim,
    "$hartlim": discord_utils.hort_lim,

    "$hartspec": discord_utils.hort_spec,
    "$hortspec": discord_utils.hort_spec,

    "$hartadd": utils.add,
    "$hortadd": utils.add,
    "$hartremove": utils.remove,
    "$hortremove": utils.remove,
    "$hartlist": utils.list,
    "$hortlist": utils.list,

    "$horthelp": discord_utils.help,
    "$harthelp": discord_utils.help,
}


class Client(discord.Client):
    async def on_ready(self):
        print(f'[HorT] Logged on as {self.user}')
        print(f"invite link: ↓\n{DISC_LNK}")
        print('================================================================================================')
        print()

        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                name="Reddit",
                type=discord.ActivityType.watching))

    async def on_message(self, message):
        if message.author.id in BOT_IDS:
            return

        split = message.content.split(' ', 1)  # separate mom?[cmd] from args
        cmd = split[0].lower()
        args = split[1].split(' ') if len(split) > 1 else None

        name = discord_utils.author_name(message.author)

        if cmd in CMDS:
            print(f"{name} issued {cmd} command. <{args}>")
            await CMDS[cmd](self, message, args)


client = Client()
client.run(token)
