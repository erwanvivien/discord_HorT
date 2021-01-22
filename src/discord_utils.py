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


def author_name(author, discriminator=True):
    # Get nick from msg author (discord) if exists
    if not discriminator:
        return author.display_name
    return f"{author.name}#{author.discriminator}"


def create_embed(title, desc, colour=BOT_COLOR, url=HOWTO_URL):
    return discord.Embed(title=title,
                         description=desc,
                         colour=colour,
                         url=url)


async def error_message(message, title=WRONG_USAGE, desc=HELP_USAGE):
    # Sends error message to discord (red)
    try:
        return await message.channel.send(embed=create_embed(title, desc, ERROR_COLOR, HOWTO_URL))
    except Exception as error:
        utils.log("error_message", error,
                  "Could not send **error** message to discord")


async def send_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL):
    # Sends message to discord (bot_color)
    try:
        return await message.channel.send(embed=create_embed(title, desc, BOT_COLOR, HOWTO_URL))
    except Exception as error:
        utils.log("error_message", error,
                  "Could not send message to discord")


async def edit_message(message, title=WRONG_USAGE, desc=HELP_USAGE, url=HOWTO_URL):
    # Sends message to discord (bot_color)
    try:
        return await message.edit(embed=create_embed(title, desc, BOT_COLOR, HOWTO_URL))
    except Exception as error:
        utils.log("error_message", error,
                  "Could not send message to discord")


async def horts(self, message, args, subreddit_def=None):
    # Calls hort() many times
    if not args or not args[0].isnumeric():
        args = [5] + args if args else [5]

    nb = int(args[0])
    if nb > 5:
        nb = 5
    elif nb < 0:
        nb = 0

    while nb > 0:
        await hort(self, message, args, subreddit_def)
        nb -= 1


async def hort_spec(self, message, args):
    # Calls hort() or horts() with specific sub
    if len(args) > 1 and args[1].isnumeric():
        await horts(self, message, args[1:], args[0])
    else:
        await hort(self, message, args[1:], args[0])


async def hort(self, message, args, subreddit_def=None):
    # Main function
    # if subreddit_def != None, get a specific sub (from hortspec())
    # Otherwise we get a random between ["good", "bad"]
    # Then SQL request all subs in that category, and random in this list
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

    i = 0
    for i in range(1, 15):
        # While error in random
        subreddit = random.choice(
            subreddits) if subreddit_def == None else subreddit_def
        js = utils.subreddit_json(subreddit)
        if "error" in js:
            error = js["reason"]
            await error_message(message,
                                title="SubReddit error",
                                desc=f"""Subreddit `{subreddit} is currently not available, check if quanrantined, banned or private.
                                ⚠ Consider removing it from your list ! ⚠\n
                                Actual error was : `{error}`
                                """)

            if subreddit_def != None:
                return
            else:
                continue

        # Getter for sub informations
        posts, post_data = await get(message, js, args)

        if not posts:
            continue

        # print(posts)
        if ("dist" in posts and posts["dist"] == 0 or
                "error" in posts and posts["error"] != 200):
            utils.log("hort", "Subreddit not found",
                      f"SubReddit `{subreddit}` was not found")
            return await error_message(message,
                                       title="Something went wrong",
                                       desc=f"SubReddit `{subreddit}` was not found")

        if not post_data:
            continue

        break

    if i == 14:  # End of the for in the said bounds => No images were found
        return await error_message(message,
                                   title="Something went wrong",
                                   desc=f"SubReddit `{subreddit}` probably doesn't have images")

    # Prints with / without spoiler
    emoji = " " + "✅" if good_or_bad == "good" else "❌"
    if subreddit_def:
        emoji = " " + "⁉"

    sub = post_data["subreddit"] + f" {emoji} "
    if not show_subreddit:
        sub = "|| " + sub + " || from " + author_name(message.author)

    await message.channel.send(f"/r/{sub}\n" + post_data["url"])


async def get(message, js, args=None):
    # Checks if we ask to skip videos
    show_novideos = (args != None) and ("novideo" in args)

    if not "data" in js:
        return None, None

    # Try reading a .json from the sub
    try:
        nb_posts = js["data"]["dist"]
        if nb_posts == 0:
            return js["data"], None
        posts = js["data"]["children"]

        post_nb = random.randrange(nb_posts)

        post = posts[post_nb]
        post_data = post["data"]
    except Exception as error:
        utils.log("get", error, "Json was bad formatted\n++++    " + js)
        return js, error

    if show_novideos and post_data["is_video"]:
        utils.log("get", "Video Error",
                  "Got a video but it asked for images only")
        return posts, None
    if post_data["url"][-1] == '/' or "discord" in post_data["url"] or "gallery" in post_data["url"]:
        utils.log("get", "Discord link or not an image",
                  "Got something that differs from an image / video")
        return posts, None

    # Everything went well, we send the resulting post
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
