import sys
import time
sys.path.append('./twycrawler')
import twycrawler as twc
import tweepy
from collections import deque

# misc settings
retry_timeout = 10

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
            name = current_user.name
            print "current id %d, name: %s" % (current_id, name)
            # get neighbors (friends)
            friends_ids = api.friends_ids(current_id)
            # get user's most recent tweets
            tweets = api.user_timeline(current_id)
        except tweepy.error.TweepError:
            # wait a few seconds
            time.sleep(retry_timeout)
            # retry later
            queue.appendleft(current_id)

        # discard any user that already exists
        if not twc.user_exists(current_id):
            # store data from user in db
            twc.save_user_profile(current_user, tweets, friends_ids)
        for friend in friends_ids:
            if not friend in visited:
                visited.add(friend)
                queue.append(friend)
    except KeyboardInterrupt:
        # save current queue
        twc.save_queue(queue, visited)
        raise
