import re
import requests
from urllib.parse import urlparse, urljoin
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time;from time import *


print("""
 _____   ___ ___ __ __  __  ___
| __\ \_/ / | __|  V  |/  \| _,\
| _| > , <| | _|| \_/ | /\ | v_/
|___/_/ \_\_|_| |_|||_|_||_|_|
                      |
                      |
                      |
                    ^.-.^
                   '^\+/^`
                   '/`"'\`
""")


base_url = input(" URL (ex. https://example.com)> ")
print("\n")
url = base_url
visited_urls = set()

time = strftime("%H:%M:%S", gmtime())
print("["+time+"]","Now Crawling",url)


def crawl(url):

    i = 1
    response = requests.get(url)
    image_urls = re.findall('img .*?src="(.*?)"', response.text)
    for image_url in image_urls:

        parsed_url = urlparse(image_url)
        if not parsed_url.scheme:
            image_url = urljoin(base_url, image_url)

        image_response = requests.get(image_url)

        try:
            with open("temp.jpg", "wb") as f:
                f.write(image_response.content)
        except:
            pass
        try:
            with Image.open("temp.jpg") as img:
                try:
                    exif_data = img._getexif()
                    if exif_data:
                        exif_dict = {TAGS.get(tag_id, tag_id): value for tag_id, value in exif_data.items()}

                        if "GPSInfo" in exif_dict:
                            time = strftime("%H:%M:%S", gmtime())
                            print("["+time+"]","[GPS data]",image_url)

                        if "Make" in exif_dict or "Model" in exif_dict:
                            make = exif_dict.get("Make", "")
                            model = exif_dict.get("Model", "")
                            print("["+time+"]","[Device data]",image_url)
                    else:
                        i = i + 1

                        try:
                            time = strftime("%H:%M:%S", gmtime())

                            os.remove("temp.jpg")
                        except Exception as E:

                            pass
                        pass
                except AttributeError:

                    pass
        except Exception as E:
            pass

    link_urls = re.findall('a .*?href="(.*?)"', response.text)
    for link_url in link_urls:
        parsed_url = urlparse(link_url)
        if parsed_url.scheme and parsed_url.netloc == urlparse(base_url).netloc:

            if link_url not in visited_urls:
                visited_urls.add(link_url)
                time = strftime("%H:%M:%S", gmtime())
                print("["+time+"]","Now Crawling",link_url)
                crawl(link_url)
        elif not parsed_url.scheme:
            link_url = urljoin(base_url, link_url)
            if link_url not in visited_urls:
                visited_urls.add(link_url)
                time = strftime("%H:%M:%S", gmtime())
                print("["+time+"]","Now Crawling",link_url)
                crawl(link_url)

visited_urls.add(base_url)
crawl(base_url)
crawl(url)
