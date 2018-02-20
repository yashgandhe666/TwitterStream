# TwitterStream

Collecting and storing streamed tweets in MongoDB using the tweepy package and using flask as a micro-web framework.

## Instructions:

Install [python-3](https://www.python.org/downloads/)

### Dependencies for API 1:
`pip install pymongo`

`pip install tweepy`

### Dependencies for API 2:
`pip install flask`

### API 1:
Set up Mongo server on localhost and start it.
Run `python streaming_API.py` to collect the tweets and store it using MongoDB.
Database: twitterdb
Collection: twitter_search

### API 2:
`python flask_html.py` to start the server.
http://127.0.0.1:5000/ for the home page
