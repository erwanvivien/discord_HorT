import sqlite3
from sqlite3 import Error
import os

import discord_utils
import utils


def get_content(file):
    # Read file content
    file = open(file, "r")
    s = file.read()
    file.close()
    return s


DB_PATH = "db/database.db"


def create():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.close()

    sql_create_discord = """CREATE TABLE IF NOT EXISTS discords
    (
        id INTEGER NOT NULL PRIMARY KEY
    );
    """
    exec(sql_create_discord)

    sql_create_good = """CREATE TABLE IF NOT EXISTS good
    (
        id integer PRIMARY KEY AUTOINCREMENT,
        id_discord INTEGER,
        subreddit TEXT NOT NULL,
        FOREIGN KEY(id_discord) REFERENCES discords(id)
    );
    """
    exec(sql_create_good)

    sql_create_bad = """CREATE TABLE IF NOT EXISTS bad
    (
        id integer PRIMARY KEY AUTOINCREMENT,
        id_discord INTEGER,
        subreddit TEXT NOT NULL,
        FOREIGN KEY(id_discord) REFERENCES discords(id)
    );
    """
    exec(sql_create_bad)


def exists(discord_id):
    sql = f'''SELECT * FROM discords WHERE id = {discord_id}'''
    db = exec(sql)

    for row in db:
        if discord_id == row[0]:
            return row

    return None


def add_guild(discord_id):
    sql = f'''INSERT INTO discords (id) VALUES (?)'''
    args = [discord_id]
    exec(sql, args)

    goods = get_content("good").split('\n')
    bads = get_content("bad").split('\n')

    for g in goods:
        if not g:
            continue

        sql = f'''INSERT INTO good (id, id_discord, subreddit) VALUES (?, ?, ?)'''
        args = [None, discord_id, g]
        exec(sql, args)

    for b in bads:
        if not b:
            continue

        sql = f'''INSERT INTO bad (id, id_discord, subreddit) VALUES (?, ?, ?)'''
        args = [None, discord_id, b]
        exec(sql, args)


async def add(self, message, args):
    if not args or not args[0] in ["good", "bad"] or len(args) < 2:
        return await discord_utils.error_message(message, title="Wrong usage", desc="Add needs arguments\n``good/bad`` ``sub_name``")

    good_or_bad = args[0]
    discord_id = message.guild.id

    content = ""
    msg = await discord_utils.send_message(
        message, title="Adding...", desc=content)

    for sub in args[1:]:
        await discord_utils.edit_message(msg, title="Adding...", desc=content)
        # If an empty arg was passed
        if not sub:
            continue

        # Check if sub exists / is accessible
        if "error" in utils.subreddit_json(sub):
            await discord_utils.error_message(message, title="Wrong SubReddit",
                                              desc=f"SubReddit `{sub}` is not accessible\n" +
                                              f"Check https://reddit.com/r/{sub}/.json\n" +
                                              f"Error was `" + utils.subreddit_json(sub)["reason"] + '`')

        sql = f'''SELECT subreddit FROM {good_or_bad} WHERE {good_or_bad}.id_discord = ? AND subreddit LIKE ?'''
        if exec(sql, (discord_id, sub)):
            content += f"❌ `/r/{sub}` already present\n"
            continue

        sql = f'''INSERT INTO {good_or_bad} (id, id_discord, subreddit) VALUES (?, ?, ?)'''
        content += f"✅ `/r/{sub}` successfully added\n"

        exec(sql, (None, discord_id, sub))

    await discord_utils.edit_message(msg, title="Done", desc=content)


async def remove(self, message, args):
    if not args or not args[0] in ["good", "bad"] or len(args) < 2:
        return await discord_utils.error_message(message, title="Wrong usage", desc="Add needs arguments\n``good/bad`` ``sub_name``")

    good_or_bad = args[0]
    discord_id = message.guild.id

    subs_ok = []
    subs_ko = []
    for sub in args[1:]:
        sql = f'''SELECT subreddit FROM {good_or_bad} WHERE {good_or_bad}.id_discord = ? AND subreddit LIKE ?'''
        if not exec(sql, (discord_id, sub)):
            subs_ko += [f"``{sub}``"]
            continue

        sql = f'''DELETE FROM {good_or_bad} WHERE id_discord = ? AND subreddit = ?'''
        subs_ok += [f"``{sub}``"]
        exec(sql, (discord_id, sub))

    subs_ok = " ".join(subs_ok)
    subs_ko = " ".join(subs_ko)

    if (subs_ko):
        await discord_utils.error_message(message, title="Wrong SubReddit", desc=f"SubReddit {subs_ko} already exists")
    if (subs_ok):
        await discord_utils.send_message(message, title="Success!", desc=f"SubReddit(s) {subs_ok} successfully added")


async def list(self, message, args):
    if not args or not args[0] in ["bad", "good"]:
        return await discord_utils.error_message(message, title="Wrong usage", desc="Add needs arguments\n``good/bad`` ``sub_name``")

    sql = f"SELECT subreddit FROM {args[0]} WHERE id_discord = {message.guild.id}"
    l = exec(sql)
    s = ""
    for e in l:
        s += "- /r/" + e[0] + "\n"

    await discord_utils.send_message(
        message,
        title=f"({len(l)}) {args[0]}'s list",
        desc=s,
        url=f"https://github.com/erwanvivien/discord-HorT/blob/main/{args[0]}")


def exec(sql, args=None):
    conn = sqlite3.connect('database.db')
    if not conn:
        return None
    cur = conn.cursor()

    if args:
        res = cur.execute(sql, args).fetchall()
    else:
        res = cur.execute(sql).fetchall()

    conn.commit()
    conn.close()

    return res
