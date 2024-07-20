from selectolax.parser import HTMLParser

import re
import os
import sys

import httpx
import img2pdf


HOME = os.path.expanduser("~")
BASE_DIR = os.path.join(HOME, "slidesave")
IMG_DIR = "img"
HTML_DIR = "html"
PDF_DIR = "pdf"

IMG_PATH = os.path.join(BASE_DIR, IMG_DIR)
HTML_PATH = os.path.join(BASE_DIR, HTML_DIR)
PDF_PATH = os.path.join(BASE_DIR, PDF_DIR)


def init():
    if not os.path.exists(IMG_PATH):
        os.makedirs(IMG_PATH)
    if not os.path.exists(HTML_PATH):
        os.makedirs(HTML_PATH)
    if not os.path.exists(PDF_PATH):
        os.makedirs(PDF_PATH)


def get(url):
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
    }
    return httpx.get(url, headers=headers)


def save_img(url, name):
    if os.path.isfile(name):
        print(f"{name} already exists")
        return

    content = get(url).content
    with open(name, "wb") as f:
        f.write(content)
    print(f"{name} downloaded")


def get_html(url, name):
    html_name = os.path.join(HTML_PATH, name + ".html")
    if os.path.isfile(html_name):
        with open(html_name, "r") as f:
            html = f.read()
        print(f"{html_name} fetched from cache")
        return html
    html = get(url).text
    with open(html_name, "w") as f:
        f.write(html)
    print(f"{html_name} fetched from network")
    return html


def parse_slides(html, name, pdf):
    tree = HTMLParser(html)
    folder = os.path.join(IMG_PATH, name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    page_number = tree.css_first("[data-cy='page-number']")
    page_count = int(page_number.text().split("of")[1].strip())
    first_slide = tree.css_first("#slide-image-0")
    srcset = first_slide.attributes.get("srcset")

    base_img_url = srcset.split(",")[-1].strip().split(" ")[0]
    img_width = srcset.strip().split(" ")[-1].replace("w", "")

    imgs = []

    for i in range(1, page_count + 1):
        img_name = os.path.join(folder, f"slide-{i:03d}.jpg")
        img_url = base_img_url.replace(f"-1-{img_width}.jpg", f"-{i}-{img_width}.jpg")
        save_img(img_url, img_name)
        imgs.append(img_name)

    if pdf:
        pdf_name = os.path.join(PDF_PATH, f"{name}.pdf")
        if os.path.isfile(pdf_name):
            print(f"{pdf_name} already exists")
            return
        with open(pdf_name, "wb") as f:
            f.write(img2pdf.convert(imgs))
        print(f"{pdf_name} generated")


def save_slides(url, pdf=True):
    init()
    try:
        url = url.split("?")[0].strip()
        match = re.match(r"https://www.slideshare.net/[a-zA-Z0-9-._]+/(?P<name>.*)", url)
        if match is None:
            return -1
        name = match.group("name").replace("/", "-")
        html = get_html(url, name)
        parse_slides(html, name, pdf)
    except:
        return False
    return True


def handle_cli():
    if len(sys.argv) < 2:
        print("the app requires 'url' as the parameter")
    else:
        url = sys.argv[1].split("?")[0].strip()
        pdf = True
        if len(sys.argv) == 3:
            pdf = False
        status_code = save_slides(url, pdf)
        if status_code == -1:
            print("url not supported")


if __name__ == "__main__":
    handle_cli()
