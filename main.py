#!/user/bin/env python
# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import json
import sys
import MeCab
import random
import re
 
while True:
    search_words = raw_input(u"words: ")
 
    C_KEY = "*************************************"
    C_SECRET = "*************************************"
    A_KEY = "*************************************"
    A_SECRET = "*************************************"
 
    def Search_words():
        url = "https://api.twitter.com/1.1/search/tweets.json?"
        params = {
                "q": unicode(search_words, "utf-8"),
                "lang": "ja",
                "result_type": "recent",
                "count": "100"
                }
        tw = OAuth1Session(C_KEY,C_SECRET,A_KEY,A_SECRET)
        req = tw.get(url, params = params)
        tweets = json.loads(req.text)
        for tweet in tweets["statuses"]:
            f = open("tweet.txt" , "aw")
            lists = (tweet["text"].encode("utf-8"))
            if "http" in lists:
                lists = lists.split("http", 1)[0]
                lists = lists.split("@")[0]
                lists = lists.split("RT")[0]
 
                f.write(lists)
                f.flush()
                f.close()
 
 
    def Mecab_file():   
        f = open("tweet.txt","rb")
        data = f.read()
        f.close()
 
        mt = MeCab.Tagger("-Owakati")
 
        wordlist = mt.parse(data)
        wordlist = wordlist.rstrip(" \n").split(" ")
 
        markov = {}
        w = ""
 
        for x in wordlist:
            if w:
                if markov.has_key(w):
                    new_list = markov[w]
                else:
                    new_list =[]
 
                new_list.append(x)
                markov[w] = new_list
            w = x
 
        choice_words = wordlist[0]
        sentence = ""
        count = 0
 
        while count < 90:
            sentence += choice_words
            choice_words = random.choice(markov[choice_words])
            count += 1
 
            sentence = sentence.split(" ", 1)[0]
            p = re.compile("[!-/:-@[-`{-~]")
            sus = p.sub("", sentence)
 
        words = re.sub(re.compile("[!-~]"),"",sus)
        twits = words + " 【tweet from twmarkov】"
 
        url = "https://api.twitter.com/1.1/statuses/update.json"
        params = {"status": twits,"lang": "ja"}
        tw = OAuth1Session(C_KEY,C_SECRET,A_KEY,A_SECRET)
        req = tw.post(url, params = params)
        if req.status_code == 200:
            print "Success! Your Tweet"
        else:
            print req.status_code
 
 
    if search_words:
        Search_words()
        Mecab_file()
    else:
        break
