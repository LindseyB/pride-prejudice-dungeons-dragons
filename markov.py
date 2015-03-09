import random
import sys
import time
import PIL
import textwrap
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
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
    margin = offset = 10
    font = ImageFont.truetype("Lora-Regular.ttf", 16)
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
    try:
        if len(status) > 100:
            # create the image to tweet with
            img = Image.new("RGBA", (400,400),(255,255,255))
            draw = ImageDraw.Draw(img)
            for line in textwrap.wrap(status, width=50):
                draw.text((margin, offset), line, (0,0,0), font=font)
                offset += font.getsize(line)[1]
            draw = ImageDraw.Draw(img)

            status = (status[:100] + '...')
            twitter.update_status_with_media(status=status, media=draw.getdata())
        else:
            twitter.update_status(status=status)
    except:
        print "some sort of error... don't really care..."

while True:
    generate_sentences()
    print "sleeping..."
    time.sleep(3600)