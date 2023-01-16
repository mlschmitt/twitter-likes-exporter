# Twitter Likes Exporter

Hacky Python scripts for downloading your Twitter likes and converting to HTML. Includes support for downloading user avatars and image media in tweets. Uses the GraphQL API powering Twitter.com, the equivalent of you scrolling through all your likes in your web browser.

Note only currently supports grabbing the liked tweet. So if it was a quote tweet, does not download the RT'd tweet. If it's a reply or part of a thread, does not download the other tweets.

Meant to jumpstart you to at least getting your tweets offline from Twitter, if not building something much better!

## Setup

Intended for use with Python 3.7. First install requirements:

```bash
pip install -r requirements.txt
```

(It's just `requests`). Next you'll need to populate the `config.json` file with credentials needed to match how your web browser gets your likes from Twitter.com:

1. Open up your web browser and ensure the Network web debugging tab is open so you can inspect network requests
2. Navigate to `https://twitter.com/<your_user_handle>/likes`
3. Look for a network request to an `api.twitter.com` domain path ending in `/Likes`
4. From the request headers:
    a. Copy the `Authorization` value and save as `HEADER_AUTHORIZATION` in `config.json`
    b. Copy the `Cookies` value and save as `HEADER_COOKIES` in `config.json`
    c. Copy the `x-csrf-token` value and save as `HEADER_CSRF` in `config.json`
5. Find your Twitter user ID (available in the `/Likes` request params, or elsewhere) and save as `USER_ID` in `config.json`


### Download Likes to JSON

By default, liked tweets will be saved to a file `liked_tweets.json` in this repo's folder path. If you'd like to override this, set new path as `OUTPUT_JSON_FILE_PATH` in `config.json`.

Run as follows:

```bash
python download_tweets.py
```


### Convert JSON Likes to HTML

WIP
