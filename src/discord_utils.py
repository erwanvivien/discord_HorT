import discord
import random
# from utils import subreddit_json, get_content
import utils
import database as db

WRONG_USAGE = "Something went wrong"
HELP_USAGE = "Please see $horthelp"
HOWTO_URL = "https://github.com/erwanvivien/discord-HorT"

BOT_COLOR = discord.Colour(0x8b8349)
ERROR_COLOR = discord.Colour(0xff0000)
WARN_COLOR = discord.Colour(0xebdb34)
VALID_COLOR = discord.Colour(0x55da50)

REDDIT = ["good", "bad"]


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


async def send_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL):
    embed = discord.Embed(title=title,
                          description=desc,
                          colour=BOT_COLOR,
                          url=url)

    await message.channel.send(embed=embed)


async def horts(self, message, args, subreddit_def=None):
    try:
        nb = int(args[0])
        if nb > 5:
            nb = 5
        elif nb < 0:
            nb = 0
    except:
        return await error_message(message, title="Wrong usage", desc="1st argument must be an integer")

    while nb > 0:
        await hort(self, message, args, subreddit_def)
        nb -= 1


async def hort_spec(self, message, args):
    if len(args) > 1 and args[1].isnumeric():
        await horts(self, message, args[1:], args[0])
    else:
        await hort(self, message, args[1:], args[0])


async def hort(self, message, args, subreddit_def=None):
    show_subreddit = (args != None) and ("show" in args)

    is_bad = (args != None) and ("bad" in args)
    is_good = (args != None) and ("good" in args)

    post_data = None

    good_or_bad = random.choice(REDDIT)
    if is_bad:
        good_or_bad = "bad"
    elif is_good:
        good_or_bad = "good"

    sql = f'SELECT subreddit FROM {good_or_bad} WHERE id_discord = {message.guild.id}'
    subreddits = db.exec(sql)
    subreddits = [e[0] for e in subreddits]

    while True:
        subreddit = random.choice(
            subreddits) if subreddit_def == None else subreddit_def
        js = utils.subreddit_json(subreddit)
        if "error" in js:
            error = js["reason"]
            await error_message(message,
                                title="SubReddit error",
                                desc=f"""Subreddit ``{subreddit}`` is currently not available, check if quanrantined, banned or private.
                                ⚠ Consider removing it from your list ! ⚠\n
                                Actual error was : ``{error}``
                                """)
            if subreddit_def != None:
                return
            else:
                continue

        posts, post_data = await get(message, js, args)
        # print(posts)

        if not posts:
            continue

        # print(posts)
        if ("dist" in posts and posts["dist"] == 0 or
                "error" in posts and posts["error"] != 200):
            return await error_message(message,
                                       title="Something went wrong",
                                       desc=f"SubReddit '{subreddit}' was not found")
        if not post_data:
            continue

        break

    emoji = " ✅" if good_or_bad == "good" else " ❌"
    if show_subreddit:
        sub = post_data["subreddit"] + emoji
    else:
        sub = "||" + post_data["subreddit"] + emoji + "||"

    await message.channel.send(f"/r/{sub}\n" + post_data["url"])


async def get(message, js, args=None):
    show_novideos = (args != None) and ("novideo" in args)

    if not "data" in js:
        return None, None

    try:
        nb_posts = js["data"]["dist"]
        if nb_posts == 0:
            return js["data"], None
        posts = js["data"]["children"]

        post_nb = random.randrange(nb_posts)

        post = posts[post_nb]
        post_data = post["data"]
    except Exception as error:
        print(js)
        return js, error

    # print(post)
    if show_novideos and post_data["is_video"]:
        return posts, None
    if post_data["url"][-1] == '/' or "discord" in post_data["url"]:
        return posts, None

    return js["data"], post_data


async def help(self, message, args):
    s = """
```
- $hart
- $harts nb                         # with (1 <= nb <= 5)
- $hartspec sub_name [nb]           # with (1 <= nb <= 5)
- $hartadd good/bad sub_name

Optional params for all functions:
- show
- novideo
- bad / good
```
    """

    await send_message(message, title="Usage", desc=s,
                       url="https://github.com/erwanvivien/discord-HorT#usages")
