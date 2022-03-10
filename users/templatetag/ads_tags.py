from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def inject_ads_after_paragraph(value, arg):

    # Render our adsense code placed in html file
    ad_code = render_to_string("users/ads.html")

    # Break down content into paragraphs
    paragraphs = value.split("</p>")

    # Check if paragraph we want to post after exists
    if arg < len(paragraphs):

        # Append our code before the following paragraph
        paragraphs[arg] = ad_code + paragraphs[arg]

        # Assemble our text back with injected adsense code
        value = "</p>".join(paragraphs)

    return value
