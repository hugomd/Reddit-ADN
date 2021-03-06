from appdotnet import *
import praw, time, urllib

#Set a user agent, this can be your app name or a description of your app.
r = praw.Reddit(user_agent="USERAGENT")

#Obviously, put your own access token here. If you don't have a developer account, grab a token from Dev Lite, thanks @duerig
app = appdotnet(access_token="authtoken")

already_done = set()

def duplicate_check(id):
    found = 0
    with open('posted_posts.txt', 'r') as file:
        for line in file:
            if id in line:
                found = 1
    return found

def add_id_to_file(id):
    with open('posted_posts.txt', 'a') as file:
        file.write(str(id) + "\n")

#Get the submissions and post them to App.net
while urllib.urlopen("http://reddit.com/").getcode() == 200:
    l = r.get_top(limit=1)
    submission = next(l,None)

    if not submission: 
        continue

    found = duplicate_check(submission.id)
    if found == 0:
        while submission.id in already_done and urllib.urlopen("http://reddit.com/").getcode() == 200:
            submission=next(r.get_front_page(limit=1, params={'before':"t3_"+submission.id }),None)
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
            add_id_to_file(submission.id)
    time.sleep(600)
