import random;
import sys;
import time;
from twython import Twython
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.cfg")
config.sections()
APP_KEY = config.get("twitter", "app_key")
APP_SECRET = config.get("twitter", "app_secret")
OAUTH_TOKEN = config.get("twitter", "oauth_token")
OAUTH_TOKEN_SECRET = config.get("twitter", "oauth_token_secret")

stopword = "\n" # Since we split on whitespace, this can never be a word
stopsentence = (".", "!", "?",) # Cause a "new sentence" if found at the end of a word
sentencesep  = "\n" #String used to separate sentences


# GENERATE TABLE
w1 = stopword
w2 = stopword
table = {}

twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

with open("source.txt") as f:
    for line in f:
        for word in line.split():
            if word[-1] in stopsentence:
                table.setdefault( (w1, w2), [] ).append(word[0:-1])
                w1, w2 = w2, word[0:-1]
                word = word[-1]
            table.setdefault( (w1, w2), [] ).append(word)
            w1, w2 = w2, word
table.setdefault( (w1, w2), [] ).append(stopword)

MAXSENTENCES = 5

w1 = stopword
w2 = stopword

def generate_sentences():
    global w1, w2
    sentence = []
    sentences = []

    while len(sentences) < MAXSENTENCES:
        newword = random.choice(table[(w1, w2)])
        if newword == stopword: sys.exit()
        if newword in stopsentence:
            sentences.append(" ".join(sentence) + newword)
            sentence = []
        else:
            sentence.append(newword)
        w1, w2 = w2, newword

    print "tweeting..."
    status = random.choice(sentences)
    twitter.update_status(status=status)

while True:
    generate_sentences()
    time.sleep(3600)