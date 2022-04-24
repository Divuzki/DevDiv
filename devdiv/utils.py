import re
import string
import random
from pathlib import Path
from PIL import Image
from io import BytesIO
from django.core.files import File


def truncate_string(value, max_length=45, suffix="devdiv"):
    string_value = str(value)
    string_truncated = string_value[:min(
        len(string_value), (max_length - len(suffix)))]
    suffix = (suffix if len(string_value) > max_length else '')
    return suffix+string_truncated


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# ROT13 ENCRYPTION
rot13trans = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                           'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm')


# Function to translate plain text
def rot13_encrypt(text):
    return text.translate(rot13trans)


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        text = instance.author.username
        if instance.content and not text:
            text = instance.description
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4))

        return unique_slug_generator(instance, new_slug=new_slug)
    return rot13_encrypt(truncate_string(slug)).upper()


image_types = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def image_resize(image, width, height):
    # Open the image using Pillow
    img = Image.open(image)
    # check if either the width or height is greater than the max
    if img.width > width or img.height > height:
        output_size = (width, height)
        # Create a new resized “thumbnail” version of the image with Pillow
        img.thumbnail(output_size)
        # Find the file name of the image
        img_filename = Path(image.file.name).name
        # Spilt the filename on “.” to get the file extension only
        img_suffix = Path(image.file.name).name.split(".")[-1]
        # Use the file extension to determine the file type from the image_types dictionary
        img_format = image_types[img_suffix]
        # Save the resized image into the buffer, noting the correct file type
        buffer = BytesIO()
        img.save(buffer, format=img_format)
        # Wrap the buffer in File object
        file_object = File(buffer)
        # Save the new resized file as usual, which will save to S3 using django-storages
        image.save(img_filename, file_object)


def check_for_tag(content, HashTag):
    arr = re.findall(r"#(\w+)", content)
    for hsh in arr:
        if len(hsh) < 80:
            full_hash = '#' + hsh
            if HashTag.objects.filter(name__iexact=hsh):
                content = content.replace(
                    full_hash, f'<a href="/hashtag/{hsh}/?new=no">#{hsh}</a>')
            else:
                content = content.replace(
                    full_hash, f'<a href="https://whamuthygle.com/bR3.Vb0FPY3/plvLbWm/V/JDZPDJ0w0iMRzNkT2GM/TSka5/LAT/Q_z/OpTHYUy/MYDLAf">#{hsh}</a>')
                # content = content.replace(full_hash, f'<a href="/hashtag/{hsh}/?new=yes">#{hsh}</a>')
    return content


def add_comma_to_number(n):
    res = str(n)
    res = res[::-1]

    ans = ""
    for i in range(len(res)):
        if i % 3 == 0 and i != 0:
            ans += ','
        ans += res[i]

    ans = ans[::-1]

    return ans


def num_sum(num):
    magnitude = 0
    if abs(num) >= 1000:
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000
        # add more suffixes if you need them
        num = '%.2f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])
    return num


# Getting Image Current Average Color
def get_image_color(url, link=False):
    import requests
    import io

    image_bytes = None
    if link == True:
            response = requests.get(f"{url}")
            image_bytes = io.BytesIO(response.content)

    if image_bytes == None:
        img = Image.open(url)
    else:
        img = Image.open(image_bytes)
    colors = img.getpixel((320, 240))
    color = f"rgb{colors}"
    img.close()
    return color
