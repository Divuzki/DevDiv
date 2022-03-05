from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from users.models import Post

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
            title = post.text
            qs = Post.objects.filter(title__iexact=title).first()
            print(qs)
            if qs is None:
                html = requests.get(url)
                soup = BeautifulSoup(html.content, 'html.parser')
                # post = soup.find_all("div", class_="jeg_inner_content")
                descs = soup.find_all("div", class_="entry-header")
                img = soup.find_all("div", class_="jeg_featured")
                # getting the content
                content = soup.find_all("div", class_="content-inner")
                desc_list = []
                img_list = []
                unwanted_list = []
                content_list = []
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

                # print(content_list)
                except:
                    desc_list = None
                    img_list = None
                    unwanted_list = None

                # Getting the finished looped post details data
                try:
                    discription = ' '.join([str(x) for x in desc_list])
                    image_url = ' '.join([str(x) for x in img_list])
                    content = '\n'.join([str(x) for x in content_list])
                    # content = '\n'.join([str(x) for x in content])

                    qs = Post.objects.filter(title=title)
                    if not qs.exists():
                        Post.objects.create(
                            title=title, 
                            description=discription,
                            content=content, 
                            author=USER_1,
                            image_url=image_url,
                            scraped=True
                            )
                        print('%s added' % (title,))
                    else:
                        print('%s already exists' % (title,))
                except:
                    print('%s can`t be posted' % (title,))
            else:
                print('%s => exists' % (title,))
        self.stdout.write( 'Scraped Sucessful ✅' )