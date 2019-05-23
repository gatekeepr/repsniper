#!/usr/bin/python
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

        # check if new post available and reset variables
        if latest not in recent:
            for submission in subreddit.new(limit=1):
                recent = submission.title
                url = submission.url
            latest = recent
            trigger = False

        # call message fn if its an european listing and hasnt been sent yet
        if trigger is not True and "US" not in recent and "CAN" not in recent and "AUS" not in recent:
            trigger = True
            send_telegram_message(recent, url)

    except praw.requests.exceptions.HTTPError as e:
        msg = "HTTPError(" + str(e.errno) + "): " + str(e.strerror)
        print(msg)
        pass
        
    time.sleep(10)
