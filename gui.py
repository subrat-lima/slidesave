from tkinter import *
from tkinter import messagebox

import app


def download_slides():
    url = url_input.get()
    if len(url.strip()) == 0:
        messagebox.showinfo("error", "enter an url")
        return False
    response = app.save_slides(url)
    if response == True:
        messagebox.showinfo("success", "pdf file has been downloaded")
    else:
        messagebox.showinfo("error", "pdf file has not been downloaded")
    url_input.delete(0, END)
    return True


root = Tk()

root.title("download slides")
root.geometry("1200x720")

url_label = Label(root, text="enter slideshare url you want to download")
url_label.pack(pady=(20, 50))

url_input = Entry(root, width=50)
url_input.pack(ipady=5, ipadx=2, pady=(1, 15))

download_btn = Button(
    root, text="download", bg="white", fg="black", command=download_slides
)
download_btn.pack(pady=(10, 20))

root.mainloop()
