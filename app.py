from tkinter import *
import tkinter as tk
# pip install pillow
from PIL import ImageTk,Image
import xkcd_scraper

# declaring the primary window
app = tk.Tk()

# declaring a xkcd_scraper class object
def get_xkcd_comic():
    xkcd_comic = xkcd_scraper.xkcd()
    xkcd_img_url = xkcd_comic.scrape_xkcd_webpage() # image url after scraping the xkcd webpage
    downloaded_image_path = xkcd_comic.download_xkcd_image(xkcd_img_url) # path to the downloaded xkcd image
    return downloaded_image_path

# method to get next image on button click
def next_img():
    """ Callback function to button"""
    app.img = ImageTk.PhotoImage(Image.open(get_xkcd_comic()))
    panel.config(image = app.img)

# loading the image
app.img = ImageTk.PhotoImage(Image.open(get_xkcd_comic()))

# reading the image
panel = tk.Label(app, image = app.img) 

# setting the application
panel.pack(side = "bottom", fill = "both", expand = "yes")

# declaring a button
btn = Button(app, text = "Next", command = next_img)
btn.pack(side = "right")


# running the application
app.mainloop()