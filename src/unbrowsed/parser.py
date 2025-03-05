from selectolax.lexbor import LexborHTMLParser


def parse_html(html: str) -> LexborHTMLParser:
    return LexborHTMLParser(html)
