import json
import urllib2
from bs4 import BeautifulSoup
import time


def get_messages(symbol):
    url = 'https://api.stocktwits.com/api/2/streams/symbol/' + symbol + '.json?filter=top&max'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url, headers=hdr)
    html = urllib2.urlopen(req).read()
    while True:
        try:
            js = json.loads(str(html))
        except:
            js = None
        if js is not None:
            msgs = js["messages"]
            for msg in msgs:
                keys = msg.keys()
                body = msg["body"] # message information

                context = ""
                if "links" in keys:     # links mentioned, can be used as context
                    links = msg["links"]
                    for link in links:
                        if "title" in link.keys():
                            context += link["title"]
                        elif "description" in link.keys():
                            context += link["description"]

                sentiment = msg["entities"]["sentiment"]    # author's sentiment
                if sentiment is not None:
                    sentiment = sentiment["basic"]
                else:
                    sentiment = ""

                created_time = msg["created_at"]   # msg created time
                mentioned_users = msg["mentioned_users"]      # mentioned users
                mentioned_symbols = msg["symbols"]   # mentioned symbols
                msg_id = msg["id"]    # msg id

                if "likes" in keys:
                    likes = msg["likes"]
                    likes_id = likes["user_ids"]
                    likes_count = likes["total"]

                # user information
                user = msg["user"]
                username = user["username"]
                name = user["name"]
                classification = user["classification"]     # list: [], ["suggested"], ["suggested", "official"]
                official = user["official"]
                like_count = user["like_count"] # likes received in total
                ideas = user["ideas"]
                following = user["following"]
                join_date = user["join_date"]
                follower = user["follower"]
                watchlist_stocks_count = user["watchlist_stocks_count"]
                user_id = user["id"]
                identity = user["identity"]     # User, Official

            url = 'https://api.stocktwits.com/api/2/streams/symbol/' + symbol + '.json?filter=top&max=' + msg_id
            try:
                req = urllib2.Request(url, headers=hdr)
                html = urllib2.urlopen(req).read()
            except:
                time.sleep(3)
                try:
                    req = urllib2.Request(url, headers=hdr)
                    html = urllib2.urlopen(req).read()
                except:
                    pass