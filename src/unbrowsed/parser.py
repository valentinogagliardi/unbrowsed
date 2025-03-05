from selectolax.parser import HTMLParser


def parse_html(html: str) -> HTMLParser:
    return HTMLParser(html)
