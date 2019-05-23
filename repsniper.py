#!/usr/bin/python3
import praw
import pdb
import re
import os
import time
import telegram
import configparser

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
    # get recent submission
    try:
        for submission in subreddit.new(limit=1):
            recent = submission.title
            url = submission.url

        # call message fn if its an european listing and hasnt been sent yet
        check = recent.upper()
        if trigger is not True and "[US]" not in check and "[USA]" not in check and "[CAN]" not in check and "[AUS]" not in check and "[ASIA]" not in check:
            trigger = True
            send_telegram_message(recent, url)
    except HTTPError as e:
        msg = "HTTPError(" + str(e.errno) + "): " + str(e.strerror)
        print(msg)
        pass
    time.sleep(10)
