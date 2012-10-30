A simple Twitter crawler I used for collecting data for one of my other projects.

The script does a breadth first search starting from the logged api user and collects profile data, tweets and the topology collected from the users' friends.

# Instructions

1. Create a `credentials.json` file inside the `credentials` folder.
2. Run `python crawler.py`. It will create a sqlite database inside the `database` folder.
3. Pause script with `Ctrl-C` anytime and resume again from step 2. It will pick up where it left off.

# Dependencies

* tweepy
* peewee

# TODO

* Scripts to create statistics out of the database.

# License

MIT License. See attached `LICENSE` file.
