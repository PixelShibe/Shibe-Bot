import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3

'''USER CONFIGURATION'''

USERNAME  = "Shibe-Bot"
PASSWORD  = "robin1"
USERAGENT = "PixelShibe's Giveaway bot!"
SUBREDDIT = "Dogecoin"
TITLESTRING = ["Giveaway"]
REPLYSTRING = "It looks like you're having a giveaway! Let me help!  +/u/dogetipbot 10 doge"
MAXPOSTS = 1
WAIT = 10800



'''All done!'''




WAITS = str(WAIT)
try:
    import #This is a file in my python library which contains my Bot's username and password. I can push code to Git without showing credentials
    USERNAME = bot.getuG()
    PASSWORD = bot.getpG()
    USERAGENT = bot.getaG()
except ImportError:
    pass

sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
print('Loaded Completed table')

sql.commit()

r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD) 

def scanSub():
    print('Searching '+ SUBREDDIT + '.')
    subreddit = r.get_subreddit(SUBREDDIT)
    posts = subreddit.get_new(limit=MAXPOSTS)
    for post in posts:
        pid = post.id
        try:
            pauthor = post.author.name
        except AttributeError:
            pauthor = '[DELETED]'
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [pid])
        if not cur.fetchone():
            cur.execute('INSERT INTO oldposts VALUES(?)', [pid])
            pbody = post.selftext.lower()
            pbody += ' ' + post.title.lower()
            if any(key.lower() in pbody for key in TITLESTRING):
                print('Replying to ' + pid + ' by ' + pauthor)
                post.add_comment(REPLYSTRING)
    sql.commit()


while True:
    try:
        scanSub()
    except Exception as e:
        print('An error has occured:', e)
    print('Running again in ' + WAITS + ' seconds \n')
    sql.commit()
    time.sleep(WAIT)
