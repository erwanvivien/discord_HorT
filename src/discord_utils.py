import discord
import random
from utils import subreddit_json

WRONG_USAGE = "Something went wrong"
HELP_USAGE = "Please see $horthelp"
HOWTO_URL = "https://github.com/erwanvivien/discord-HorT"

BOT_COLOR = discord.Colour(0x8b8349)
ERROR_COLOR = discord.Colour(0xff0000)
WARN_COLOR = discord.Colour(0xebdb34)
VALID_COLOR = discord.Colour(0x55da50)

BAD_REDDIT = ["trashy", "poop", "UnderTail", "cursedimages", "FearMe",
              "creepy", "WTF", "MakeMeSuffer", "buttsharpies",
              "dragonfuckingcars", "SubwayCreatures"]

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


async def hort(self, message, args):
    try:
        nb = int(args[0])
    except:
        nb = 1

    show_subreddit = (args != None) and ("show" in args)
    show_videos = (args != None) and ("video" in args)

    while nb > 0:
        post_data = None
        good_or_bad = random.choice(REDDIT)

        while True:
            subreddit = random.choice(good_or_bad)
            js = subreddit_json(subreddit)

            nb_posts = js["data"]["dist"]
            posts = js["data"]["children"]

            post_nb = random.randrange(nb_posts)

            post = posts[post_nb]
            post_data = post["data"]
            print(post)

            if not show_videos and post_data["is_video"]:
                continue

            break

        if show_subreddit:
            await message.channel.send(post_data["subreddit"])
        await message.channel.send(post_data["url"])

        nb -= 1
