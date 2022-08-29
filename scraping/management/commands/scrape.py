from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from users.models import Post
from django.utils.text import slugify

USER_1 = User.objects.get(pk=1)
class Command(BaseCommand):
    # define logic of command
    def handle(self, *args, **options):
        # collect html
        html = requests.get('https://nairametrics.com/')
        # convert to soup
        soup = BeautifulSoup(html.content, 'html.parser')
        # grab all postings
        postings = soup.find_all("div", class_="jeg_posts")
        # post_list = []
        for p in postings:
            post = p.find("h3", {"class":"jeg_post_title"})
            url = post.find('a')['href']
            title = post.text.strip()
            qs = Post.objects.filter(title=title).first()
            if not qs is None:
                html = requests.get(url)
                soup = BeautifulSoup(html.content, 'html.parser')
                # post = soup.find_all("div", class_="jeg_inner_content")
                descs = soup.find_all("div", class_="entry-header")
                img = soup.find_all("div", class_="jeg_featured")
                # getting the content
                content = soup.find_all("div", class_="content-inner")
                # getting the hashtags
                tags = soup.find_all("div", class_="jeg_breadcrumbs")
                desc_list = []
                img_list = []
                unwanted_list = []
                content_list = []
                tags_list = []
                try:
                    for d in descs:
                        desc_list.append(d.find('h2').text)  # getting the discription

                    # Looking for post image link
                    for img_url in img:
                        img_list.append(img_url.find('a')['href'])  # getting the image_url

                    # Looking for Unwanted Tags
                    for p in content:
                        unwanted_list.append(p.find('div'))

                    # Looking for Content Tags
                    for p in content:
                        pr = p.find_all('p')
                        unwanted = p.find('div')
                        unwanted.extract()
                        for pr in pr:
                            content_list.append(pr)
                    for tag in tags:
                        tag = tag.find_all("span")
                        for t in tag:
                            tags = t.find_all('a')
                            for tag in tags:
                                tags_list.append(tag.text)

                # print(content_list)
                except:
                    desc_list = None
                    img_list = None
                    unwanted_list = None
                    tags_list = None

                # Getting the finished looped post details data
                try:
                    discription = ' '.join([str(x) for x in desc_list])
                    image_url = ' '.join([str(x) for x in img_list])
                    content = '\n'.join([str(x) for x in content_list])
                    tags_list = tags_list[1:]
                    hashtags = tags_list[1:]
                    # hashtags = ','.join([slugify(str(tag)) for tag in tags_list])
                    # print(hashtags)
                    # content = '\n'.join([str(x) for x in content])

                    qs = Post.objects.filter(title=title).first()
                    if qs is None:
                        qs = Post.objects.create(
                            title=title, 
                            description=discription,
                            content=content, 
                            author=USER_1,
                            # hashtags=hashtags,
                            image_url=image_url,
                            scraped=True
                            )
                        for tag in hashtags:
                            qs.hashtags.add(slugify(tag))
                        qs.save()
                        
                        print('%s added' % (title,))
                    else:
                        print('%s already exists' % (title,))
                except:
                    print('%s can`t be posted' % (title,))
            else:
                print('%s => exists' % (title,))
        self.stdout.write( 'Scraped Sucessful ✅' )