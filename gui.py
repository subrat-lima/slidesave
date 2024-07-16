import re

import app

from tkinter import *
from tkinter import ttk


def download_slides(*args):
    commentlbl["text"] = "pdf file download in process..."
    commentlbl["foreground"] = "blue"
    url_value = url.get()
    response = app.save_slides(url_value)
    if response == True:
        commentlbl["text"] = "pdf file has been downloaded"
        commentlbl["foreground"] = "green"
    else:
        commentlbl["text"] = "error downloading pdf file"
        commentlbl["foreground"] = "red"
    url.delete(0, END)
    return True


def validate_url(value):
    pattern = r"https:\/\/www.slideshare.net\/slideshow\/.*"
    if re.match(pattern, value) is None:
        return False
    show_message()
    return True

def on_invalid():
    show_message("invalid url", "red")

def show_message(error = "", color="black"):
    errorlbl["text"] = error
    url["foreground"] = color

root = Tk()
root.title("slideshare downloader")

content = ttk.Frame(root)

urllbl = ttk.Label(content, text="enter slideshare url")
url = ttk.Entry(content)
download = ttk.Button(content, text="download", command=download_slides)
errorlbl = ttk.Label(content)
commentlbl = ttk.Label(content)

vcmd = (root.register(validate_url), "%P")
ivcmd = (root.register(on_invalid),)
    
content.grid(column=0, row=0, padx=4, pady=4)
urllbl.grid(column=0, row=0, padx=4, pady=4)
url.grid(column=0, row=1, padx=4, pady=4, sticky=(E, W))
download.grid(column=0, row=2, padx=4, pady=4)
errorlbl.grid(column=0, row=3, padx=4, pady=4)
commentlbl.grid(column=0, row=4, padx=4, pady=4)

url.config(validate="focusout", validatecommand=vcmd, invalidcommand=ivcmd)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1, minsize=200)
content.columnconfigure(0, weight=1, minsize=800)
content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=1)
content.rowconfigure(2, weight=1)
content.rowconfigure(3, weight=1)
content.rowconfigure(4, weight=1)


root.mainloop()
