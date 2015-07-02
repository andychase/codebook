from collections import namedtuple
import re
from urllib.parse import urlparse
import yaml
import pytz
from dateutil.parser import parse


www_remover = lambda _, r=re.compile("^www\."): r.sub("", _)

Info = namedtuple("Info", "title date authors")


def url_handler(url):
    if not url.startswith("http"):
        url = "http://" + url
    parsed = urlparse(url)
    output_url = parsed.geturl()
    domain = www_remover(parsed.netloc)
    domain_link = "{}://{}".format(parsed.scheme, domain)
    return domain, domain_link, output_url


def normalize_whitespace(source):
    """ Modified from Python Markdown. This simplifies processing of lines
    """
    start_of_text = '\u0002'  # Use STX ("Start of text") for start-of-placeholder
    end_of_text = '\u0003'  # Use ETX ("End of text") for end-of-placeholder
    source = source.replace(start_of_text, "").replace(end_of_text, "")
    source = source.lstrip("\n")
    source = source.replace("\r\n", "\n").replace("\r", "\n") + "\n\n"
    source = source.expandtabs(4)
    source = re.sub(r'(?<=\n) +\n', '\n', source)
    source = re.sub(r'\n\n\n+', '\n\n', source)
    return source


def handle_author_link(author):
    if "(" in author:
        author_name, link = author.split("(", 1)
        author_name = author_name.strip()
        link, rest = link.split(")", 1)
        if any(rest.strip()):
            rest = " " + handle_author_link("[&]" + rest)
        return '<a href="{}">{}</a>{}'.format(url_handler(link)[2], author_name, rest)
    else:
        return author


def process(contents):
    for i, block in enumerate(str(normalize_whitespace(contents)).split("\n\n")):
        indented = block.startswith(" " * 4)
        first_line = block.split("\n")[0] if len(block.split("\n")) > 0 else False
        has_type_block = \
            first_line and \
            len(first_line) > 4 and \
            first_line[4] == "[" and \
            first_line.lstrip().startswith("[") and \
            first_line.rstrip().endswith("]")
        type_block = None
        if has_type_block:
            type_block = first_line.split("[", 1)[1].rsplit("]", 1)[0]

        if indented and i == 0:
            stripped_lines = [l[4:] for l in block.split("\n")]
            title, authors, date = stripped_lines[0], stripped_lines[1:-1], stripped_lines[-1]
            date = pytz.timezone('US/Pacific').localize(parse(date))

            yield Info(title, date, authors), None, None

        elif indented and has_type_block:
            stripped_lines = [l[4:] for l in block.split("\n")]
            yaml_block = "\n".join(stripped_lines[1:])
            yaml_data = yaml.load(yaml_block)
            domain, domain_link, url = url_handler(yaml_data['url'])
            if 'author' in yaml_data:
                yaml_data.setdefault('authors', []).insert(0, yaml_data['author'])
            if 'authors' in yaml_data:
                yaml_data['authors'] = list(map(handle_author_link, yaml_data['authors']))
            yaml_data['domain'] = domain
            yaml_data['domain_link'] = domain_link
            yaml_data['url'] = url
            yaml_data['type'] = type_block
            yaml_data['date'] = pytz.timezone('US/Pacific').localize(parse(yaml_data['date']))

            yield None, yaml_data, None
        else:
            yield None, None, block
