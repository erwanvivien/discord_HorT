import requests
import json


def get_content(file):
    # Read file content
    file = open(file, "r")
    s = file.read()
    file.close()
    return s


def subreddit_json(subreddit):
    headers = {"User-Agent": "discord:798130116491345971:v1 (by /u/Xiaojiba)"}
    r = requests.get(
        f"http://reddit.com/r/{subreddit}/.json", headers=headers)
    return r.json()
