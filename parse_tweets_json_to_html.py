import datetime
import json
import os
import requests

class ParseTweetsJSONtoHTML():
    def __init__(self):
        self._output_html_directory = None
        self._tweets_as_json = None

        with open("config.json") as json_data_file:
            config_data = json.load(json_data_file)
            self.output_json_file_path = config_data.get('OUTPUT_JSON_FILE_PATH')
            self.download_images = config_data.get('DOWNLOAD_IMAGES')

    def write_tweets_to_html(self):
        with open(self.output_index_path, 'w') as output_html:
            output_html.write('<html><head><title>Liked Tweets Export</title>')
            output_html.write('<link rel="stylesheet" href="styles.css"></head>')
            output_html.write('<body><h1>Liked Tweets</h1><div class="tweet_list">')
            for tweet_data in self.tweets_as_json:
                tweet_html = self.create_tweet_html(tweet_data)
                output_html.write(tweet_html)
            output_html.write('</div></body></html>')

    def create_tweet_html(self, tweet_data):
        output_html = '<div class="tweet_wrapper">'

        if self.download_images:
            user_image_src = f'images/avatars/{tweet_data["user_id"]}.jpg'
            full_path = f"{self.output_html_directory}/{user_image_src}"
            self.save_remote_image(tweet_data["user_avatar_url"], full_path)
        else:
            user_image_src = tweet_data["user_avatar_url"]
        
        output_html += '<div class="tweet_author_wrapper">'
        output_html += f"<div class='tweet_author_image'><img loading='lazy' src='{user_image_src}'></div>"
        output_html += "<div class='author_context'><div class='tweet_author_handle'>"
        output_html += f"<a href='https://www.twitter.com/{tweet_data['user_handle']}/' target='_blank'>"
        output_html += f"@{self.parse_text_for_html(tweet_data['user_handle'])}</a></div>"
        output_html += f"<div class='tweet_author_name'>{self.parse_text_for_html(tweet_data['user_name'])}</div>"
        output_html += '</div></div>\n'

        output_html += f"<div class='tweet_content'>{self.parse_text_for_html(tweet_data['tweet_content'])}</div>"

        if tweet_data["tweet_media_urls"]:
            output_html += "<div class='tweet_images_wrapper'>"
            for media_url in tweet_data["tweet_media_urls"]:
                if self.download_images:
                    media_name = media_url.split("/")[-1]
                    user_image_path = f'images/tweets/{media_name}'
                    full_path = f"{self.output_html_directory}/{user_image_path}"
                    self.save_remote_image(media_url, full_path)
                else:
                    user_image_path = media_url
                output_html += f"<div class='tweet_image'><a href='{user_image_path}' target='_blank'><img loading='lazy' src='{user_image_path}'></a></div>"
            output_html += "</div>\n"


        parsed_datetime = datetime.datetime.strptime(tweet_data['tweet_created_at'], "%a %b %d %H:%M:%S +0000 %Y")
        output_html += f"<div class='tweet_created_at'>{parsed_datetime.strftime('%m/%d/%Y %I:%M%p')}</div>"
        output_html += "<div class='twitter_link'>"
        output_html += f"<a href='https://www.twitter.com/{tweet_data['user_handle']}/status/{tweet_data['tweet_id']}/' target='_blank'>Original tweet &#8599;</a> &#8226; "
        individual_tweet_file_path = f"{self.output_html_directory}/tweets/{tweet_data['tweet_id']}.html"
        output_html += f"<a href='tweets/{tweet_data['tweet_id']}.html' target='_blank'>Local version</a>"
        output_html += "</div>"

        output_html += "</div>\n\n"

        
        with open(individual_tweet_file_path, 'w') as individual_tweet_file:
            individual_tweet_file.write('<html><head><title>Liked Tweets Export</title>')
            individual_tweet_file.write('<link rel="stylesheet" href="../styles.css"></head>')
            individual_tweet_file.write('<body><div class="tweet_list">')
            adjusted_html = output_html.replace("images/avatars", "../images/avatars")
            adjusted_html = adjusted_html.replace("images/tweets", "../images/tweets")
            individual_tweet_file.write(adjusted_html)
            individual_tweet_file.write('</div></body></html>')

        return output_html

    def save_remote_image(self, remote_url, local_path):
        if os.path.exists(local_path):
            return
        print(f"Downloading image {remote_url}...")
        img_data = requests.get(remote_url).content
        with open(local_path, 'wb') as handler:
            handler.write(img_data)

    def parse_text_for_html(self,input_text):
        return input_text.encode('ascii', 'xmlcharrefreplace').decode()

    @property
    def output_index_path(self):
        return f'{self.output_html_directory}/index.html'

    @property
    def output_html_directory(self):
        if not self._output_html_directory:
            script_dir = os.path.dirname(__file__)
            self._output_html_directory = os.path.join(script_dir, 'tweet_likes_html')
        return self._output_html_directory

    @property
    def tweets_as_json(self):
        if not self._tweets_as_json:
            with open(self.output_json_file_path, 'rb') as json_file:
                lines = json_file.readlines()
                self._tweets_as_json = json.loads(lines[0])

        return self._tweets_as_json

if __name__ == "__main__":
    parser = ParseTweetsJSONtoHTML()
    print(f"Saving tweets to {parser.output_index_path}...")
    parser.write_tweets_to_html()
    print(f"Done. Output file located at {parser.output_index_path}")

