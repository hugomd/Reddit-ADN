from appdotnet import *
import praw, time

#Set a user agent, this can be your app name or a description of your app.
r = praw.Reddit(user_agent='USERAGENT')

#Obviously, put your own access token here. If you don't have a developer account, grab a token from Dev Lite, thanks @duerig
app = appdotnet(access_token="token")

already_done = set()

#Get the submissions and post them to App.net
while True:
    l = r.get_top(limit=1)
    submission = next(l,None)

    if not submission: 
        continue

    while submission.id in already_done:
        submission=next(r.get_front_page(limit=1, params={'after':"t3_"+submission.id }),None)
        if not submission:
            break
    if submission:
        id = submission.id
        title = submission.title
        url = submission.short_link
        
        if title.count > 100:
            title = title[0:100] + ".."

        post = title + " | " + url
        app.createPost(post)

        save_state = (id)
        already_done.add(submission.id)
    time.sleep(600)
