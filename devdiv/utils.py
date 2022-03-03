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
                content = content.replace(full_hash, f'<a href="/hashtag/{hsh}/?new=no">#{hsh}</a>')
            else:
                content = content.replace(full_hash, f'<a href="https://biptolyla.com/bJ3/V.0JPg3tp_vpbim/V_JqZ/Dy0H0/M/zvkL1iOjTucTxWLETsQ/z/O/TGUx5aNdznI-">#{hsh}</a>')
                # content = content.replace(full_hash, f'<a href="/hashtag/{hsh}/?new=yes">#{hsh}</a>')
    return content

def num_sum(num):
    if num >= 1000:
        num = str(f"{num}")
        if not num[1] == "0":
            num = f"{num[0]}.{num[1]}k"
        else:
            num = f"{num[0]}k"
    elif num >= 1000000:
        num = str(f"{num}")
        if len(num) >= 2:
            num = f"{num[0]+num[1]}M"
        else:
            num = f"{num[0]}M"