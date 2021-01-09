import requests
import uuid
import os
import getpass
import tempfile
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

class xkcd:
    def __init__(self):
        self.url = "https://c.xkcd.com/random/comic/"  # link fetches a random comic strip from xkcd page
        self.directory = "/home/" + getpass.getuser() + "/comic-images/xkcd" # getpass.getuser() helps in returning the current terminal username
        self.filepath = None

    def get_xkcd_image(self):
        """grabs the image from the webpage"""
        soup = bs(requests.get(self.url).content, "lxml")
        img = soup.find_all("img")
        comic_img = img[2]
        xkcd_comic_img_url = comic_img.attrs.get("src")
        xkcd_comic_img_url = xkcd_comic_img_url[2:]
        xkcd_comic_img_url = "http://" + xkcd_comic_img_url
        return xkcd_comic_img_url 

    def download_xkcd_image(self, img_url):
        """ Downloads xkcd comic images from the image url"""
        response = requests.get(img_url, stream=True)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        filename = str(uuid.uuid4()) # creating a random file name of hex format
        with open(self.directory + '/' + filename + '.png', "wb") as handler:
            handler.write(response.content)
        return self.directory + '/' + filename + '.png'
    
    def delete_xkcd_image(self, saved_image_path):
        """ Delete the downloaded image"""
        os.system("rm " + saved_image_path)

    def show_xkcd_image(self):
        """ Show the xkcd comic image"""
        img_url = self.get_xkcd_image()
        saved_image_path = self.download_xkcd_image(img_url)
        os.system("feh " + saved_image_path)
        self.delete_xkcd_image(saved_image_path) # delete the dowloaded image
    
    
if __name__ == "__main__":
    xkcd_comic = xkcd()
    xkcd_comic.show_xkcd_image()

    