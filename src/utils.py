import requests
import json
# from discord_utils import error_message
import discord_utils


def get_content(file):
    # Read file content
    file = open(file, "r")
    s = file.read()
    file.close()
    return s


def subreddit_json(subreddit, limit=30):
    headers = {"User-Agent": "discord:798130116491345971:v1 (by /u/Xiaojiba)"}
    r = requests.get(
        f"http://reddit.com/r/{subreddit}/.json?limit={limit}",
        headers=headers,
        timeout=5)
    return r.json()


async def add(self, message, args):
    if not args or not args[0] in ["bad", "good"]:
        return await discord_utils.error_message(message, title="Wrong usage", desc="add needs arguments\n``good/bad`` ``sub_name``")

    js = subreddit_json(args[1], 5)
    try:
        if js["data"]["dist"] == 0:
            raise Exception()
    except:
        return await discord_utils.error_message(message, title="Wrong SubReddit", desc="This SubReddit doesn't exist")

    l = get_content(args[0]).split('\n')
    if args[1] in l:
        return await discord_utils.error_message(message, title="Wrong SubReddit", desc="This SubReddit already exists")

    file = open(args[0], "a+")
    file.write("\n" + args[1])
    file.close()

    await discord_utils.send_message(
        message, title="Success", desc=f"This SubReddit was succesfully added to the {args[0]} list")


async def remove(self, message, args):
    if not args or not args[0] in ["bad", "good"]:
        return await discord_utils.error_message(message, title="Wrong usage", desc="add needs arguments\n``good/bad`` ``sub_name``")

    l = get_content(args[0]).split('\n')
    if not args[1] in l:
        return await discord_utils.error_message(message, title="Wrong SubReddit", desc="This SubReddit was not in the list")

    l.remove(args[1])

    file = open(args[0], "w")
    file.write(l[0])
    for sub in l[1:]:
        file.write('\n' + sub)
    file.close()

    await discord_utils.send_message(
        message, title="Success", desc=f"This SubReddit was succesfully removed to the {args[0]} list")
