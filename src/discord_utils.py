import discord
import random
# from utils import subreddit_json, get_content
import utils

WRONG_USAGE = "Something went wrong"
HELP_USAGE = "Please see $horthelp"
HOWTO_URL = "https://github.com/erwanvivien/discord-HorT"

BOT_COLOR = discord.Colour(0x8b8349)
ERROR_COLOR = discord.Colour(0xff0000)
WARN_COLOR = discord.Colour(0xebdb34)
VALID_COLOR = discord.Colour(0x55da50)


GOD_REDDIT = utils.get_content("good").split('\n')
BAD_REDDIT = utils.get_content("bad").split('\n')


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


async def send_message(message, title=WRONG_USAGE, desc=HELP_USAGE):
    embed = discord.Embed(title=title,
                          description=desc,
                          colour=BOT_COLOR,
                          url=HOWTO_URL)

    await message.channel.send(embed=embed)


async def horts(self, message, args):
    try:
        nb = int(args[0])
        if nb > 10:
            nb = 10
        elif nb < 0:
            nb = 0
    except:
        return await error_message(message, title="Wrong usage", desc="1st argument must be an integer")

    while nb > 0:
        await hort(self, message, args)
        nb -= 1


async def hort_lim(self, message, args):
    try:
        await hort(self, message, args, int(args[0]))
    except:
        return await error_message(message, title="Wrong usage", desc="1st argument must be an integer")


async def hort_spec(self, message, args):
    try:
        return await hort(self, message, args, int(args[1]), args[0])
    except:
        try:
            return await hort(self, message, args, int(args[0]), args[1])
        except:
            return await hort(self, message, args, 30, args[0])


async def hort(self, message, args, limit=30, subreddit=None):
    show_subreddit = (args != None) and ("show" in args)

    is_bad = (args != None) and ("bad" in args)
    is_good = (args != None) and ("good" in args)

    post_data = None
    good_or_bad = random.choice(REDDIT)

    if is_bad:
        good_or_bad = BAD_REDDIT
    elif is_good:
        good_or_bad = GOD_REDDIT

    while True:
        subreddit = random.choice(
            good_or_bad) if subreddit == None else subreddit
        js = utils.subreddit_json(subreddit)

        posts, post_data = await get(js, args)

        # print(posts)
        if not posts or ("dist" in posts and posts["dist"] == 0 or
                         "error" in posts and posts["error"] != 200):
            return await error_message(message,
                                       title="Something went wrong",
                                       desc=f"SubReddit '{subreddit}' was not found")
        if not post_data:
            continue

        break

    if show_subreddit:
        await message.channel.send(post_data["subreddit"])
    await message.channel.send(post_data["url"])


async def get(js, args=None):
    show_novideos = (args != None) and ("novideo" in args)

    try:
        nb_posts = js["data"]["dist"]
        if nb_posts == 0:
            return js["data"], None
        posts = js["data"]["children"]

        post_nb = random.randrange(nb_posts)

        post = posts[post_nb]
        post_data = post["data"]
    except:
        print(js)
        return js["data"], None

    # print(post)
    if show_novideos and post_data["is_video"]:
        return posts, None
    if post_data["url"][-1] == '/' or "discord" in post_data["url"]:
        return posts, None

    return js["data"], post_data
