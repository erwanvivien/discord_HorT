import sqlite3
from sqlite3 import Error
import os

import utils


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


def add(discord_id, good_or_bad, subreddit):
    if not good_or_bad in ["good", "bad"]:
        return

    sql = f'''INSERT INTO {good_or_bad} (id, id_discord, subreddit) VALUES (?, ?, ?) WHERE id_discord = {discord_id}'''
    args = (None, discord_id, subreddit)
    return exec(sql, args)


def remove(discord_id, good_or_bad, subreddit):
    if not good_or_bad in ["good", "bad"]:
        return

    sql = f'''DELETE FROM {good_or_bad} WHERE id_discord = {discord_id} AND subreddit = {subreddit}'''
    return exec(sql)


def exec(sql, args=None):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    if args:
        res = cur.execute(sql, args).fetchall()
    else:
        res = cur.execute(sql).fetchall()

    conn.commit()
    if conn:
        conn.close()

    return res
