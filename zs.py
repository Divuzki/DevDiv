import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify
# collect html
html = requests.get("https://nairametrics.com/2022/04/23/worlds-richest-billionaire-elon-musk-accuses-bill-gates-of-shorting-tesla/")
soup = BeautifulSoup(html.content, 'html.parser')
# post = soup.find_all("div", class_="jeg_inner_content")
descs = soup.find_all("div", class_="entry-header")
img = soup.find_all("div", class_="jeg_featured")
# getting the hashtags
tags = soup.find_all("div", class_="jeg_breadcrumbs")
tags_list = []
for tag in tags:
    tag = tag.find_all("span")
    for t in tag:
        tags = t.find_all('a')
        for tag in tags:
            tags_list.append(tag.text)
tags_list = tags_list[1:]
hashtags = ','.join([slugify(str(tag)) for tag in tags_list])
hashtags = hashtags.split(",")
print(hashtags)
