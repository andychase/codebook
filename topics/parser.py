from collections import namedtuple
import re
from urllib.parse import urlparse

ParserOutput = namedtuple("ParserOutput", "section subsection link text separator")(None, None, None, None, None)
BlockData = namedtuple("BlockData", "type title url metadata desc commentary extra")("", "", "", "", "", "", None)

www_remover = lambda _, r=re.compile("^www\."): r.sub("", _)


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


def get_type_from_block(line):
    """
    >>> get_type_from_block(" [type] ")
    'type'
    """
    if "[" in line and "]" in line:
        line = line.strip()
        line = line.split("]", 1)[0]
        return line.split("[", 1)[1].strip()
    return ""


def get_title_from_block(line):
    """
    >>> get_title_from_block(" [type] title")
    'title'
    """
    if "[" in line and "]" in line:
        return line.split("]", 1)[1].strip()
    return ""


def process(contents):
    """
    >>> list(process("# Section"))
    [ParserOutput(section='Section', subsection=None, link=None, text=None)]
    >>> list(process("## SubSection"))
    [ParserOutput(section=None, subsection='SubSection', link=None, text=None)]
    >>> import yaml
    >>> out_print = lambda _: print(yaml.safe_dump(dict(list(_)[0].link._asdict()), default_flow_style=False))
    >>> out_print(process('''[type] title
    ... http://example.org
    ... metadata
    ... | desc
    ... > com '''))
    commentary: com
    desc: desc
    metadata: metadata
    title: title
    type: type
    url:
    - example.org
    - http://example.org
    - http://example.org
    <BLANKLINE>
    """
    for i, block in enumerate(str(normalize_whitespace(contents)).split("\n\n")):
        is_section = block.startswith("# ")
        is_subsection = block.startswith("## ")
        is_link_block = len(block) > 1 and block[0] == "["

        if is_section:
            yield ParserOutput._replace(section=block.lstrip("#").strip())
        elif is_subsection:
            yield ParserOutput._replace(subsection=block.lstrip("##").strip())

        elif is_link_block:
            lines = block.split("\n")
            block_data = BlockData
            if len(lines) > 2:
                block_data = block_data._replace(type=get_type_from_block(lines[0]))
                block_data = block_data._replace(title=get_title_from_block(lines[0]))
                block_data = block_data._replace(url=url_handler(lines[1]))
                block_data = block_data._replace(metadata=lines[2].strip())
            if len(lines) > 3:
                for line in lines[2:]:
                    if len(line) >= 2 and line[:2] == "| ":
                        block_data = block_data._replace(desc=block_data.desc + "\n" + line[2:])
                    if len(line) >= 2 and line[:2] == ": ":
                        block_data = block_data._replace(commentary=block_data.commentary + "\n" + line[2:])
                block_data = block_data._replace(commentary=block_data.commentary.strip())
                block_data = block_data._replace(desc=block_data.desc.strip())

            if block_data.url:
                yield ParserOutput._replace(link=block_data)
        elif any(block.strip()):
            yield ParserOutput._replace(text=block)
