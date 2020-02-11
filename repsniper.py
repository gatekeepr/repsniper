#!/usr/bin/python3
import praw
import pdb
import re
import os
import time
import telegram
import configparser
import urllib.error

# load configurations
config = configparser.ConfigParser()
config.read('praw.ini')
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("FashionRepsBST")
latest = "empty"
bot = telegram.Bot(token=config.get('bot1', 'telegram'))
filterwords = ["[US]", "[USA]", "[CAN]", "[ASIA]", "[AUS]"]
triggerwords = ["NUPTSE", "TNF"]

# notifies the user with a telegram message
def send_telegram_message(title, url, isRare):
    msg = "New Listing found!\n" + title + "\n" + url
    try:
        if(isRare):
            bot.send_message(chat_id=config.get('bot1', 'chatid'), text=msg)
        else:
            bot.send_message(chat_id=config.get('bot1', 'groupchatid'), text=msg)
    except:
        print("Failed to send message")


# main loop that checks for new posts containing our keywords
while 1:
    try:
        # get recent submission
        for submission in subreddit.new(limit=1):
            recent = submission.title
            url = submission.url
    except:
        print("Reddit down/Rate limited!")

    # check if new post available and reset variables
    if latest not in recent:
        try:
            for submission in subreddit.new(limit=1):
                recent = submission.title
                url = submission.url
            latest = recent
            trigger = False
            relevant = True
        except:
            print("Reddit down/Rate limited!")


    # do some filtering to see if the listing is relevant
    check = recent.upper()
    for word in filterwords:
        if word in check:
            relevant = False
            break
    if relevant and not trigger:
        for word in triggerwords:
            if word in check:
                send_telegram_message(recent, url, True)
                trigger = True
                break
        send_telegram_message(recent,url, False)
        trigger = True
    time.sleep(10)
