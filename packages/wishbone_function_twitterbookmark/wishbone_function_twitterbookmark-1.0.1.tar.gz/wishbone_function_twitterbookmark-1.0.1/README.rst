::

              __       __    __
    .--.--.--|__.-----|  |--|  |--.-----.-----.-----.
    |  |  |  |  |__ --|     |  _  |  _  |     |  -__|
    |________|__|_____|__|__|_____|_____|__|__|_____|
                                       version 2.2.0

    Build composable event pipeline servers with minimal effort.



    =================================
    wishbone.function.twitterbookmark
    =================================

    Version: 1.0.0

    Creates URL bookmarks from Twitter favorite events
    --------------------------------------------------


        The module takes a Twitter favorite event and extracts the URLs, tags and
        keywords.

        Bookmark event:

        @tmp.<name>.type            Can be either "text" or "bookmark"
        @tmp.<name>.url             The extracted URL. (1 event per URL)
        @tmp.<name>.summary         An array of the meaningfull words of the tweet.
                                    uninteresting words.
        @tmp.<name>.tags            An array of tags
        @tmp.<name>.screen_name     The name of the tweet author.
        @tmp.<name>.created_at      The timestamp of the tweet.


        Parameters:

            - blacklist(array)([])
               |  A list of keywords to drop from the tweet to form the summary.


        Queues:

            - inbox
               |  Incoming events

            - outbox
               |  Outgoing events



