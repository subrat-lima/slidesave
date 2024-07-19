import re

from slidesave import app

from tkinter import *
from tkinter import ttk

class GUI:
    def __init__(self):
        self.initialize()

    def download_slides(self, *args):
        self.commentlbl["text"] = "pdf file download in process..."
        self.commentlbl["foreground"] = "blue"
        url_value = self.url.get()
        response = app.save_slides(url_value)
        if response == True:
            self.commentlbl["text"] = "pdf file has been downloaded"
            self.commentlbl["foreground"] = "green"
        else:
            self.commentlbl["text"] = "error downloading pdf file"
            self.commentlbl["foreground"] = "red"
        self.url.delete(0, END)
        return True


    def validate_url(self, value):
        pattern = r"https:\/\/www.slideshare.net\/slideshow\/.*"
        if re.match(pattern, value) is None:
            return False
        self.show_message()
        return True

    def on_invalid(self):
        self.show_message("invalid url", "red")

    def show_message(self, error = "", color="black"):
        self.errorlbl["text"] = error
        self.url["foreground"] = color


    def initialize(self):
        self.root = Tk()
        self.root.title("slideshare downloader")
        self.content = ttk.Frame(self.root)
        self.urllbl = ttk.Label(self.content, text="enter slideshare url")
        self.url = ttk.Entry(self.content)
        self.download = ttk.Button(self.content, text="download", command=self.download_slides)
        self.errorlbl = ttk.Label(self.content)
        self.commentlbl = ttk.Label(self.content)

        self.vcmd = (self.root.register(self.validate_url), "%P")
        self.ivcmd = (self.root.register(self.on_invalid),)
    
        self.content.grid(column=0, row=0, padx=4, pady=4)
        self.urllbl.grid(column=0, row=0, padx=4, pady=4)
        self.url.grid(column=0, row=1, padx=4, pady=4, sticky=(E, W))
        self.download.grid(column=0, row=2, padx=4, pady=4)
        self.errorlbl.grid(column=0, row=3, padx=4, pady=4)
        self.commentlbl.grid(column=0, row=4, padx=4, pady=4)

        self.url.config(validate="focusout", validatecommand=self.vcmd, invalidcommand=self.ivcmd)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1, minsize=200)
        self.content.columnconfigure(0, weight=1, minsize=800)
        self.content.rowconfigure(0, weight=1)
        self.content.rowconfigure(1, weight=1)
        self.content.rowconfigure(2, weight=1)
        self.content.rowconfigure(3, weight=1)
        self.content.rowconfigure(4, weight=1)

        self.root.mainloop()

def start_gui():
    gui = GUI()
