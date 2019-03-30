#!/usr/bin/python
import praw
import pdb
import re
import os
import time
import telegram
import configparser

# create subreddit instances
config = configparser.ConfigParser()
config.read('praw.ini')
reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("FashionRepsBST")
latest = "empty"
bot = telegram.Bot(token=config.get('bot1', 'telegram'))

# what are we looking for?
keywords = ["[GER]", "[DE]", "Stone Island", "UB",
            "UltraBoost", "Ultraboost", "ultraboost"]


# notifies the user with a telegram message
def send_telegram_message(title, url):
    print(title)
    print(url)
    msg = "New Listing found!\n" + title + "\n" + url
    bot.send_message(chat_id=415531944, text=msg)

# main loop that checks for new posts containing our keywords
while 1:
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

    # do something if it contains specified keyword
    for s in keywords:
        if s in recent and trigger is not True:
            trigger = True
            #print("Success, posting comment and sending telegram message!")
            send_telegram_message(recent, url)
    # sleep for one second
    # print("Idling...")
    time.sleep(1)
