from collections import namedtuple
import re
from urllib.parse import urlparse
import yaml
import pytz
from dateutil.parser import parse


www_remover = lambda _, r=re.compile("^www\."): r.sub("", _)

Info = namedtuple("Info", "title date authors summary")


def strip_indentation(lines):
    """
    >>> list(strip_indentation('''    a
    ... b
    ... c'''))
    ['a', 'b', 'c']
    """
    for line in lines.split('\n'):
        if line.startswith(" " * 4):
            yield line.split(" " * 4, 1)[1]
        else:
            yield line


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


def process_link_block(block_text):
    link_data = yaml.load(block_text)
    domain, domain_link, url = url_handler(link_data['url'])
    if 'author' in link_data:
        link_data.setdefault('authors', []).insert(0, link_data['author'])
    if 'authors' in link_data:
        link_data['authors'] = list(map(handle_author_link, link_data['authors']))
    link_data['domain'] = domain
    link_data['domain_link'] = domain_link
    link_data['url'] = url
    link_data['date'] = pytz.timezone('US/Pacific').localize(parse(link_data['date']))
    return link_data


def process_first_line(block):
    first_line = block.split("\n")[0] if len(block.split("\n")) > 0 else False
    has_type_block = \
        first_line and \
        len(first_line) > 4 and \
        first_line[4] == "[" and \
        first_line.lstrip().startswith("[") and \
        first_line.rstrip().endswith("]")
    if has_type_block:
        return has_type_block, first_line.split("[", 1)[1].rsplit("]", 1)[0]
    return has_type_block, ""


def process(contents):
    last_block_link_block = ""
    blocks = []

    def add_to_block(info=None, link_data=None, text_block=None):
        blocks.append((info, link_data, text_block))

    for i, block in enumerate(str(normalize_whitespace(contents)).split("\n\n")):
        indented = block.startswith(" " * 4)
        has_type_block, type_value = process_first_line(block)

        if indented:
            stripped_lines = list(strip_indentation(block))
            if has_type_block and any(last_block_link_block):
                add_to_block(link_data=process_link_block(last_block_link_block))
                last_block_link_block = ""
            if i == 0:
                title, authors, date = stripped_lines[0], stripped_lines[1:-1], stripped_lines[-1]
                date = pytz.timezone('US/Pacific').localize(parse(date))
                add_to_block(info=Info(title, date, authors, ""))
            elif i == 1:
                blocks[-1][0] = blocks[-1][0].copy(summary=stripped_lines)
            elif has_type_block:
                type_value_data = ["type: {}".format(type_value)]
                yaml_block = "\n".join(type_value_data + stripped_lines[1:])
                last_block_link_block += yaml_block
            elif any(last_block_link_block):
                yaml_block = "\n".join(stripped_lines)
                last_block_link_block += "\n\n\n" + yaml_block
            else:
                add_to_block(text_block=block)
        else:
            if any(last_block_link_block):
                # Clear our last_block_link_block queue
                add_to_block(link_data=process_link_block(last_block_link_block))
                last_block_link_block = ""
            add_to_block(text_block=block)

    return blocks
