from bs4 import BeautifulSoup


def remove_tags(html, tags):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(tags):
        # Remove tags
        data.decompose()

    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)
