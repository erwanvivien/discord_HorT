import sqlite3
from sqlite3 import Error
import os

import discord_utils


def get_content(file):
    # Read file content
    file = open(file, "r")
    s = file.read()
    file.close()
    return s


DB_PATH = "database.db"


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
        sql = f'''INSERT INTO good (id, id_discord, subreddit) VALUES (?, ?, ?)'''
        args = [None, discord_id, g]
        exec(sql, args)

    for b in bads:
        sql = f'''INSERT INTO bad (id, id_discord, subreddit) VALUES (?, ?, ?)'''
        args = [None, discord_id, b]
        exec(sql, args)


async def add(self, message, args):
    if not args or not args[0] in ["good", "bad"]:
        return await discord_utils.error_message(message, title="Wrong usage", desc="Add needs arguments\n``good/bad`` ``sub_name``")

    good_or_bad = args[0]
    discord_id = message.guild.id
    sub = args[1]

    sql = f'''SELECT subreddit FROM {good_or_bad} WHERE {good_or_bad}.id_discord = ? AND subreddit = ?'''
    if exec(sql, (discord_id, sub)):
        return await discord_utils.error_message(message, title="Wrong SubReddit", desc="SubReddit already exists")

    sql = f'''INSERT INTO {good_or_bad} (id, id_discord, subreddit) VALUES (?, ?, ?)'''
    args = (None, discord_id, sub)
    exec(sql, args)

    return await discord_utils.send_message(message, title="Success!", desc=f"SubReddit ``{sub}`` successfully added")


async def remove(self, message, args):
    if not args or not args[0] in ["good", "bad"]:
        return await discord_utils.error_message(message, title="Wrong usage", desc="Add needs arguments\n``good/bad`` ``sub_name``")

    good_or_bad = args[0]
    discord_id = message.guild.id
    sub = args[1]

    sql = f'''SELECT subreddit FROM {good_or_bad} WHERE {good_or_bad}.id_discord = ? AND subreddit = ?'''
    if not exec(sql, (discord_id, sub)):
        return await discord_utils.error_message(message, title="Wrong SubReddit", desc="SubReddit doesn't exist")

    sql = f'''DELETE FROM {good_or_bad}
              WHERE id_discord = ? AND subreddit = ?'''
    exec(sql, (discord_id, sub))

    return await discord_utils.send_message(message, title="Success!", desc=f"SubReddit ``{sub}`` successfully removed")


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
