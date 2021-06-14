import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'


def getIdFromUsername(username):
    req = requests.get(
        'https://api.roblox.com/users/get-by-username',
        headers={
            'User-Agent': USER_AGENT
        },

        data={
            'username': username
        }
    )

    return req


def getUserFollowers(userId):
    followerReq = requests.get(
        'https://friends.roblox.com/v1/users/%s/followers/count' % userId,
        headers={
            'User-Agent': USER_AGENT
        }
    )

    return followerReq


def getFriends(userId):
    friendReq = requests.get(
        'https://friends.roblox.com/v1/users/%s/friends' % userId,
        headers={
            'User-Agent': USER_AGENT
        }
    )

    return friendReq


def getStatus(userId):
    statusReq = requests.get(
        'https://users.roblox.com/v1/users/%s' % userId,
        headers={
            'User-Agent': USER_AGENT
        }
    )

    return statusReq


def getWikipediaArticle():
    wikiReq = requests.get(
        'https://en.wikipedia.org/api/rest_v1/page/random/summary',
        headers={
            'User-Agent': USER_AGENT
        }
    )

    return wikiReq.json()


