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
    return www_remover(parsed.netloc), parsed.geturl()


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


def process(contents):
    for i, block in enumerate(str(normalize_whitespace(contents)).split("\n\n")):
        indented = block.startswith(" " * 4)
        first_line = block.split("\n")[0] if len(block.split("\n")) > 0 else False
        has_type_block = first_line and first_line.lstrip().startswith("[") and first_line.rstrip().endswith("]")
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
            domain, url = url_handler(yaml_data['url'])
            yaml_data['domain'] = domain
            yaml_data['url'] = url
            yaml_data['type'] = type_block
            yaml_data['date'] = pytz.timezone('US/Pacific').localize(parse(yaml_data['date']))

            yield None, yaml_data, None
        else:
            yield None, None, block
