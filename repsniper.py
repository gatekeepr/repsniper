#!/usr/bin/python3
import praw
import pdb
import re
import os
import time
import telegram
import configparser
import urllib2

# load configurations
config = configparser.ConfigParser()
config.read('praw.ini')
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("FashionRepsBST")
latest = "empty"
bot = telegram.Bot(token=config.get('bot1', 'telegram'))

# notifies the user with a telegram message
def send_telegram_message(title, url):
    print(title)
    print(url)
    msg = "New Listing found!\n" + title + "\n" + url
    bot.send_message(chat_id=config.get('bot1', 'groupchatid'), text=msg)


# main loop that checks for new posts containing our keywords
while 1:
    try:
        # get recent submission
        for submission in subreddit.new(limit=1):
            recent = submission.title
            url = submission.url
        # check if new post available and reset variables
        if latest not in recent:
            for submission in subreddit.new(limit=1):
                recent = submission.title
                url = submission.url
            latest = recent
            trigger = False

        # call message fn if its an european listing and hasnt been sent yet
        check = recent.upper()
        if trigger is not True and "[US]" not in check and "[USA]" not in check and "[CAN]" not in check and "[AUS]" not in check and "[ASIA]" not in check:
            trigger = True
            send_telegram_message(recent, url)
    # catch exceptions when reddit is down
    except urllib2.HTTPError, e:
        if e.code in [429, 500, 502, 503, 504]:
            print "Reddit is down (error %s), sleeping..." % e.code
            time.sleep(60)
            pass
        else:
            raise
    # catch every other exception
    except Exception, e:
        print "Not a HTTP Exception, ERROR: %s" % str(e)
        raise
    time.sleep(10)
