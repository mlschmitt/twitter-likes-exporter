class TweetParser():
    def __init__(self, raw_tweet_json):
        self.is_valid_tweet = True
        self.raw_tweet_json = raw_tweet_json
        self._media_urls = None

        if not raw_tweet_json["content"].get("itemContent", None):
            self.is_valid_tweet = False
            return

        self.key_data = raw_tweet_json["content"]["itemContent"]["tweet_results"]["result"]
        if not self.key_data.get("legacy", None):
            self.is_valid_tweet = False

    def tweet_as_json(self):
        print(self.tweet_created_at)
        return {
            "tweet_id": self.tweet_id,
            "user_id": self.user_id,
            "user_handle": self.user_handle,
            "user_name": self.user_name,
            "user_avatar_url": self.user_avatar_url,
            "tweet_content": self.tweet_content,
            "tweet_media_urls": self.media_urls,
            "tweet_created_at": self.tweet_created_at
        }

    @property
    def tweet_id(self):
        return self.key_data["legacy"]["id_str"]

    @property
    def tweet_content(self):
        return self.key_data["legacy"]["full_text"]

    @property
    def tweet_created_at(self):
        return self.key_data["legacy"]["created_at"]

    @property
    def user_id(self):
        return self.key_data["legacy"]["user_id_str"]

    @property
    def user_handle(self):
        return self.user_data["screen_name"]

    @property
    def user_name(self):
        return self.user_data["name"]

    @property
    def user_avatar_url(self):
        return self.user_data["profile_image_url_https"]

    @property
    def user_data(self):
        return self.key_data["core"]["user_results"]["result"]["legacy"]

    @property
    def media_urls(self):
        if self._media_urls is None:
            self._media_urls = []
            media_entries = self.key_data["legacy"]["entities"].get("media", [])
            for entry in media_entries:
                self._media_urls.append(entry["media_url_https"])
        return self._media_urls
