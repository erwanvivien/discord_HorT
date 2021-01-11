# need to do :
import discord
from discord.ext import commands
from utils import get_content
from discord_utils import author_name, error_message
from discord_utils import hort, horts, hort_lim, hort_spec

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
token = get_content("token")

CMDS = {
    "$hart": hort,
    "$hort": hort,

    "$harts": horts,
    "$horts": horts,

    "$hortlim": hort_lim,
    "$hartlim": hort_lim,

    "$hartspec": hort_spec,
    "$hartspec": hort_spec,
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

        name = author_name(message.author)

        if cmd in CMDS:
            print(f"{name} issued {cmd} command. <{args}>")
            await CMDS[cmd](self, message, args)


client = Client()
client.run(token)
