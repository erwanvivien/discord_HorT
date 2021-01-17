import requests
import json
# from discord_utils import error_message
import discord_utils
import os
import datetime
import database as db
import shutil


LOG_FILE = "db/log"

if not os.path.exists("db"):
    os.mkdir("db")
    log("DB folder", "DB folder did not exist", "Creating DB folder")


def get_content(file):
    # Read file content
    try:
        file = open(file, "r")
        s = file.read()
        file.close()
    except Exception as error:
        log("get_content", error, f"error reading file {file}")
        return ""

    return s


def remove_old_saves():
    # Remove old saves from save folder
    now = datetime.datetime.now()
    halfhour = int(int(now.strftime("%H")) / 2)

    foldername = now.strftime("%Y-%m-%d_") + str(halfhour) + "h"
    if not os.path.exists(f"subreddit_saves"):
        os.mkdir("subreddit_saves")
    if not os.path.exists(f"subreddit_saves/{foldername}"):
        shutil.rmtree("subreddit_saves")
        os.mkdir("subreddit_saves")


def subreddit_json(subreddit):
    # Get a subreddit from a curl request
    now = datetime.datetime.now()
    halfhour = int(int(now.strftime("%H")) / 2)

    # This is all folder naming for fast removal once deprecated
    foldername = now.strftime("%Y-%m-%d_") + str(halfhour) + "h"
    if not os.path.exists(f"subreddit_saves/{foldername}"):
        remove_old_saves()
        os.mkdir(f"subreddit_saves/{foldername}")

    path = f"subreddit_saves/{foldername}/{subreddit}.json"

    # If subreddit was already asked in the 2h period, we just return the save
    if os.path.exists(path):
        return json.loads(get_content(path))

    # If it doesn't exist, we request it
    log("subreddit_json", "Created new file", path)
    headers = {
        "User-Agent": "discord:798130116491345971:v1.1 (by /u/Xiaojiba)"}
    r = requests.get(
        f"http://reddit.com/r/{subreddit}/.json?limit=100",
        headers=headers,
        timeout=5)

    # and save it
    f = open(path, "w")
    f.write(r.text)
    f.close()

    return r.json()


def log(fctname, error, message):
    now = datetime.datetime.now()
    log = f"[{now}]: " + \
        str(error) + '\n' + ('+' * 4) + (' ' * 4) + \
        fctname + (" " * (20-len(fctname))) + \
        ': ' + message + '\n'

    print(log)
    f = open(LOG_FILE, "a+")
    f.write(log)
    f.close()
