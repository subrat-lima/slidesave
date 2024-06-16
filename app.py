from selectolax.parser import HTMLParser

import httpx
import os
import sys


BASE_DIR = "data"
IMG_DIR = "img"
HTML_DIR = "html"

IMG_PATH = os.path.join(BASE_DIR, IMG_DIR)
HTML_PATH = os.path.join(BASE_DIR, HTML_DIR)


def init():
    if not os.path.exists(IMG_PATH):
        os.makedirs(IMG_PATH)
    if not os.path.exists(HTML_PATH):
        os.makedirs(HTML_PATH)


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


def parse_slides(html, name):
    tree = HTMLParser(html)
    folder = os.path.join(IMG_PATH, name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    page_number = tree.css_first("[data-cy='page-number']")
    page_count = int(page_number.text().split("of")[1].strip())
    first_slide = tree.css_first("#slide-image-0")
    srcset = first_slide.attributes.get("srcset")

    base_img_url = srcset.split(",")[-1].strip().split(" ")[0]
    print(base_img_url)

    for i in range(1, page_count + 1):
        img_name = os.path.join(folder, f"slide-{i:03d}.jpg")
        img_url = base_img_url.replace("-1-", f"-{i}-")
        save_img(img_url, img_name)


def save_slides(url):
    name = url.split("/slideshow/")[1].replace("/", "-")
    html = get_html(url, name)
    parse_slides(html, name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("the app requires 'url' as the parameter")
    else:
        init()
        url = sys.argv[1]
        save_slides(url)
