# need to do :
import discord
from discord.ext import commands
from utils import get_content
from discord_utils import author_name, error_message
from discord_utils import hort, horts, hort_lim

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

        # Check if a bot command
        # if not cmd.startswith(f"$hort") and not cmd.startswith(f"$hart"):
        #     return

        # Debugging stuff
        name = author_name(message.author)

        try:
            await CMDS[cmd](self, message, args)
            print(f"{name} issued {cmd} command. <{args}>")
        except:
            return

        # await hort(self, message, args)

        # cur_cmd = None
        # try:
        #     length_prefix = len(prefix)
        #     suffix = cmd[length_prefix:]  # Get command suffix
        #     cur_cmd = COMMANDS[suffix]['cmd']
        #     await cur_cmd(self, message, args)
        # except Exception as error:
        #     if not cur_cmd:
        #         return await error_message(message, title=f"Unknown command '{suffix}'")

        #     ERRORS += [time.ctime() + ': ' + str(error)]
        #     cmd = cmds.format_cmd(prefix, "report")
        #     await error_message(message,
        #                         title=f"The command {suffix} failed...",
        #                         desc=f"Please use ``{cmd}`` if you think it's an unexpected behaviour")

    # async def on_reaction_add(self, reaction, user):
    #     if user.id in BOT_IDS:
    #         return

    #     # Debugging stuff
    #     print(f"{user} added a {reaction.emoji}")

    #     # Both dev ids
    #     if reaction.emoji in ['✅'] and user.id in cmds.DEV_IDS \
    #             and reaction.message.channel.id == cmds.REPORT_CHANN_ID:
    #         await reaction.message.delete()

    #     if reaction.emoji in ['❌']:
    #         await reaction.message.delete()


# db.create()
client = Client()
client.run(token)

# is_video = false
# "after" exists => usage: &after=t3_XXXXXXX
# .json?limit=100
