import requests
import uuid
import os
import getpass
import tempfile
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

class reddit:
    def __init__(self):
        self.url = "https://old.reddit.com/r/webcomics/top"  # url for old webcomics subreddit from which comics will be scraped
        self.directory = "/home/" + getpass.getuser() + "/comic-images/reddit/webcomics" # directory where downloaded pics will be stored
        self.REQUEST_AGENT = "Mozilla/5.0 Chrome/47.0.2526.106 Safari/537.36"

    def get_posts_url(self):
        posts = []
        resultPage = bs(requests.get(self.url, headers={'user-agent':self.REQUEST_AGENT}).content, "lxml")
        thumbnail = resultPage.find_all('a', {'data-event-action':'thumbnail', 'class':['thumbnail', 'may-blank', 'loggedin']})
        for tag in thumbnail:
            posts.append(tag.attrs.get("href"))
        i = 0
        while (i < len(posts)):
            if posts[i][:2] == '/r':
                posts[i] = 'https://old.reddit.com' + posts[i]
            else:
                posts.pop(i)
                i -= 1
            i += 1
        return posts
    
    def get_pics_url(self, posts):
        pics, tags = [], []
        for url in posts:
            resultPage = bs(requests.get(url, headers={'user-agent':self.REQUEST_AGENT}).content, "lxml")
            tag_link = resultPage.find_all('a', {'class':['thumbnail', 'may-blank'], 'data-event-action':'thumbnail'})
            tags.append(tag_link)
        for item in tags:
            # item is a list of various tags
            # first tag gives us the link to images
            pics.append(item[0].attrs.get("href"))
        return pics
    
    def download_pics(self, pics_link):
        """Download pics using the list of links"""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        for url in pics_link:
            try:
                response = requests.get(url, stream=True)
            except requests.exceptions.RequestException as e:
                continue
            filename = url[18:]
            print(filename)
            with open(self.directory + '/' + filename, "wb") as handler:
                handler.write(response.content)
    
if __name__=="__main__":
    reddit_comics = reddit()
    posts = reddit_comics.get_posts_url()
    pics_url = reddit_comics.get_pics_url(posts)
    print(pics_url)
    reddit_comics.download_pics(pics_url)
