from langdetect import detect
import numpy as np
import matplotlib.pyplot as plt
import praw

# a class that acts as a way for the language code
# to be associated with the amount of times it
# appears in the search. Also defines lt so it can
# be used alongside sort method in list


class LangData():
    def __init__(self, langId):
        self.langId = langId
        self.instances = 1

    def __lt__(self, other):
        return self.instances > other.instances


reddit = praw.Reddit(client_id='0-cMgkolZ2QkoA',
                     client_secret='qSllj4edMdiwwmpSViOalHqmBMw',
                     username='2Grills1AshTray',
                     password='Thesillymoose9',
                     user_agent='RedditLanguages')

SUBREDDIT_NAME = 'politics'
CHECKED_THREADS = 10

langs = []
ids = []
insts = []

subreddit = reddit.subreddit(SUBREDDIT_NAME).hot(limit=CHECKED_THREADS)

for submission in subreddit:

    if not submission.stickied:
        submission.comments.replace_more(limit=0)

        for comment in submission.comments.list():
            # Failsafe incase of blank/emoji comment
            try:
                langId = detect(comment.body)

            except:
                langId = 'en'
            notFound = True

            # Ignores english from search
            if langId != 'en':
                if len(langs) is 0:
                    langs.append(LangData(langId))
                else:

                    # Adds to number of instances if language code
                    # is already counted; ads new item to list
                    # if language code is new
                    for j in range(0, len(langs)):
                        if langId is langs[j].langId:
                            langs[j].instances += 1
                            notFound = False
                    if notFound:
                        langs.append(LangData(langId))

langs.sort()

# Puts language code and instances into their own arrays for plotting
for i in range(0, len(langs)):
    ids.append(langs[i].langId)
    insts.append(langs[i].instances)


y_pos = np.arange(len(ids))

plt.bar(y_pos, insts)
plt.xticks(y_pos, ids)
plt.title('Non-English languages on ' + SUBREDDIT_NAME + ' subreddit')
plt.show()
