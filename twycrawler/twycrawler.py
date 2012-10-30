import peewee as pw
import tweepy as tpy

# database stuff
twitter_db = pw.SqliteDatabase('database/twitter.db')

class TwitterModel(pw.Model):
    class Meta:
        database = twitter_db

class User(TwitterModel):
    id = pw.PrimaryKeyField()
    created_at = pw.DateTimeField()
    followers = pw.IntegerField()
    friends = pw.IntegerField()
    screen_name = pw.CharField()
    name = pw.TextField()
    twitter_id = pw.IntegerField()

class Tweet(TwitterModel):
    id = pw.PrimaryKeyField()
    twitter_id = pw.IntegerField()
    text = pw.TextField()
    user = pw.ForeignKeyField(User)
    reply_to = pw.IntegerField(null=True)
    retweet_count = pw.IntegerField()
    created_at = pw.DateTimeField()

class Hashtag(TwitterModel):
    id = pw.PrimaryKeyField()
    text = pw.CharField()
    tweet = pw.ForeignKeyField(Tweet)

class Url(TwitterModel):
    id = pw.PrimaryKeyField()
    url = pw.TextField()
    expanded_url = pw.TextField()
    tweet = pw.ForeignKeyField(Tweet)

class TwitterLink(TwitterModel):
    id = pw.PrimaryKeyField()
    follower_id = pw.IntegerField()
    followee_id = pw.IntegerField()

def save_user_profile(twitter_user, tweets, friends):
    """ receives a user, tweets list and friends ids to save its attributes onto the db """
    user  = User.create(
            twitter_id=twitter_user.id,
            created_at=twitter_user.created_at,
            followers=twitter_user.followers_count,
            friends=twitter_user.friends_count,
            screen_name=twitter_user.screen_name,
            name=twitter_user.name)
    for tweet in tweets:
        newtweet = Tweet.create(
                twitter_id=tweet.id,
                text=tweet.text,
                user=user,
                reply_to=tweet.in_reply_to_user_id,
                retweet_count=tweet.retweet_count,
                created_at=tweet.created_at)
        for hashtag in tweet.entities['hashtags']:
            newht = Hashtag.create(text=hashtag['text'], tweet=newtweet)
        for theurl in tweet.entities['urls']:
            newurl = Url.create(url=theurl['url'], expanded_url=theurl['expanded_url'],
                    tweet=newtweet)
    for friend in friends:
        link = TwitterLink.create(follower_id=twitter_user.id, followee_id=friend)


def user_exists(twitter_id):
    """ receives a twitter id to search in the User table """
    return User.select().where(User.twitter_id == twitter_id).exists()

def last_twitter_id():
    # not used
    """ gets the twitter id of the last inserted user or None if it doesn't exist """
    result = User.select(User.twitter_id).order_by(User.id.desc()).limit(1)
    for user in result:
        return user.twitter_id
    return None

def create_tables():
    if not (User.table_exists() and Tweet.table_exists() and Hashtag.table_exists() 
            and Url.table_exists() and TwitterLink.table_exists()):
        print 'creating tables...'
        User.create_table()
        Tweet.create_table()
        Hashtag.create_table()
        Url.create_table()
        TwitterLink.create_table()

create_tables()
