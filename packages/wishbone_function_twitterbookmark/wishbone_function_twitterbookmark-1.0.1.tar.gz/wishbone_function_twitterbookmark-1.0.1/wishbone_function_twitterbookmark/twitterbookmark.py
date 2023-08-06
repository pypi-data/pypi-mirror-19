#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  twitterbookmark.py
#
#  Copyright 2016 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone import Actor
from nltk.tokenize import TweetTokenizer
from nltk import download
from nltk.corpus import stopwords
import validators
import re


class TwitterBookmark(Actor):

    '''**Creates URL bookmarks from Twitter favorite events.**

    The module takes a Twitter favorite event and extracts the URLs, tags and
    keywords.

    This module distinguishes between 2 types of favorites:


    With URL (type bookmark)

        Bookmark event:

        @tmp.<name>.type            Has value "bookmark"
        @tmp.<name>.url             The extracted URL. (1 event per URL)
        @tmp.<name>.summary         An array of meaningfull words.
        @tmp.<name>.tags            An array of hashtags
        @tmp.<name>.screen_name     The name of the author.
        @tmp.<name>.created_at      The timestamp of the tweet.

    Without URL (type text)

        @tmp.<name>.type            Has value "text"
        @tmp.<name>.text            The complete tweet.
        @tmp.<name>.tags            An array of tags
        @tmp.<name>.screen_name     The name of the tweet author.
        @tmp.<name>.created_at      The timestamp of the tweet.


    Events of type bookmark containing multiple urls will result into multiple
    events.


    Parameters:

        - blacklist(array)([])
           |  A list of keywords to drop from the tweet to form the summary.


    Queues:

        - inbox
           |  Incoming events

        - outbox
           |  Outgoing events

    '''

    def __init__(self, actor_config, blacklist=[]):
        Actor.__init__(self, actor_config)

        self.pool.createQueue("inbox")
        self.pool.createQueue("outbox")
        self.registerConsumer(self.consume, "inbox")
        self.tknzr = TweetTokenizer()

    def preHook(self):
        download(info_or_id="stopwords", quiet=True)

    def consume(self, event):

        urls = event.get("@data.target_object.entities.urls")
        tags = [tag["text"].lower() for tag in event.get("@data.target_object.entities.hashtags")]

        if len(urls) > 0:
            text = event.get("@data.target_object.text")
            tokenized_text = self.tknzr.tokenize(text)
            summary = self.cleanup(tokenized_text)

            for url in urls:
                e = event.clone()
                e.set("bookmark", "@tmp.%s.type" % (self.name))
                e.set(url["expanded_url"], "@tmp.%s.url" % (self.name))
                e.set(summary, "@tmp.%s.summary" % (self.name))
                e.set(tags, "@tmp.%s.tags" % (self.name))
                e.copy("@data.target.screen_name", "@tmp.%s.user" % (self.name))
                e.copy("@data.target.created_at", "@tmp.%s.date" % (self.name))
                self.submit(e, self.pool.queue.outbox)
        else:
                e = event.clone()
                e.set("text", "@tmp.%s.type" % (self.name))
                e.copy("@data.target_object.text", "@tmp.%s.text" % (self.name))
                e.set(tags, "@tmp.%s.tags" % (self.name))
                e.copy("@data.target.screen_name", "@tmp.%s.user" % (self.name))
                e.copy("@data.target.created_at", "@tmp.%s.date" % (self.name))
                self.submit(e, self.pool.queue.outbox)

    def cleanup(self, tokens):

        def validate(word):

            conditions = [
                word not in stopwords.words('english'),
                not validators.url(word),
                word.isalnum(),
                word.lower() not in self.kwargs.blacklist,
                word.lower() not in ["i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "it", "us"],
                word.lower() not in ["the", "a"],
                not re.match('^\d*$', word.lower()),
                len(word.lower()) > 1
            ]

            return all(conditions)

        result = []

        for word in set(tokens):
            if validate(word):
                result.append(word.lower())
        return result

