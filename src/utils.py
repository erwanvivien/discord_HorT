import requests


def get_content(file):
    # Read file content
    file = open(file, "r")
    s = file.read()
    file.close()
    return s


def subreddit_json(subreddit):
    r = requests.get(f"http://reddit.com/r/{subreddit}.json&limit=100")
    return r.json()
