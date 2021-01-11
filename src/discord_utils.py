import discord
import random

WRONG_USAGE = "Something went wrong"
HELP_USAGE = "Please see $horthelp"
HOWTO_URL = "https://github.com/erwanvivien/discord-HorT"

BOT_COLOR = discord.Colour(0x8b8349)
ERROR_COLOR = discord.Colour(0xff0000)
WARN_COLOR = discord.Colour(0xebdb34)
VALID_COLOR = discord.Colour(0x55da50)

BAD_REDDIT = ["trashy", "poop", "UnderTail", "cursedimages", "FearMe",
              "creepy", "WTF", "MakeMeSuffer"]

GOD_REDDIT = ["lovepics", "aww", "nocontextpics", "AnimalsBeingBros",
              "NatureIsFuckingLit", "wholesomememes", "photoshopbattles"]

REDDIT = [BAD_REDDIT, GOD_REDDIT]


def author_name(author):
    # Get nick from msg author (discord) if exists
    name = None
    try:
        name = author.nick
    except:
        name = author.name

    if not name:
        return author.name
    return name


async def error_message(message, title=WRONG_USAGE, desc=HELP_USAGE):
    embed = discord.Embed(title=title,
                          description=desc,
                          colour=ERROR_COLOR,
                          url=HOWTO_URL)
    await message.channel.send(embed=embed)
