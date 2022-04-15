from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.filter
def inject_ads_after_paragraph(value, arg):

    # Render our adsense code placed in html file
    ad_js_code = render_to_string("users/ads/js.html")
    ad_post_code = render_to_string("users/ads/posts.html")
    ad_vid_code = render_to_string("users/ads/video.html")
    ad_vid_code2 = render_to_string(
        "users/ads/video.html").replace("adPlayerDiv", "adPlayerDiv2")
    ad_poster = render_to_string("users/ads/poster-720x90.html")

    # Break down content into paragraphs
    paragraphs = value.split("</p>")

    # Check if paragraph we want to post after exists
    if arg < len(paragraphs):

        # Append our code before the following paragraph
        paragraphs[arg] = ad_post_code + paragraphs[arg]
        paragraphs[arg-2] = ad_vid_code + paragraphs[arg-2]
        if paragraphs[arg+4]:
            paragraphs[arg+4] = ad_vid_code2 + paragraphs[arg+4]
        else:
            paragraphs[arg] = ad_poster + paragraphs[arg]
        if paragraphs[arg+4-3]:
            paragraphs[arg] = ad_poster + paragraphs[arg]

        paragraphs[arg] = ad_js_code + paragraphs[arg]
        # Assemble our text back with injected adsense code
        value = "</p>".join(paragraphs)

    return value
