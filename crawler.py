import sys
import time
sys.path.append('./twycrawler')
import twycrawler as twc
import tweepy
from collections import deque
from tweepy.error import TweepError

# misc settings
retry_timeout = 960 # 16 min (more than the twitter's 15 min window)

# authenticate
credentials = twc.read_credentials('credentials/credentials.json')
auth = tweepy.OAuthHandler(credentials['consumer-key'], credentials['consumer-secret'])
auth.set_access_token(credentials['access-token'], credentials['access-token-secret'])
api = tweepy.API(auth_handler=auth, api_root='/1.1')

me = api.me()
print 'Logged in as: %s' % me.name

# do breadth first search to crawl Twitter
queue, visited = twc.load_queue()
if queue and visited:
    queue = deque(queue)
else:
    queue = deque([int(me.id)])
    visited = set([int(me.id)])
while queue:
    try:
        current_id = queue.popleft()
        friends_ids = []
        current_user = None
        try:
            current_user = api.get_user(current_id)
            print "current id: %d" % current_id
            # get neighbors (friends)
            friends_ids = api.friends_ids(current_id)
            # get user's most recent tweets
            tweets = api.user_timeline(current_id)
        except TweepError as e:
            if e.response.status != 401:
                # if user timeline is private skip it
                # otherwise wait some time before retry
                time.sleep(retry_timeout)
                # retry later
                queue.appendleft(current_id)
            continue

        # discard any user that already exists
        if not twc.user_exists(current_id):
            # store data from user in db
            twc.save_user_profile(current_user, tweets, friends_ids)
        for friend in friends_ids:
            if not friend in visited:
                visited.add(friend)
                queue.append(friend)

        time.sleep(70) # wait a bit till next call (~15 calls per 15 min)
    except KeyboardInterrupt:
        # save current queue
        twc.save_queue(queue, visited)
        raise
